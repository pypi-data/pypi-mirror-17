import re
import json
import requests
import urlparse
import logging

from datetime import datetime, timedelta
from lxml.builder import E, ElementMaker
from lxml import etree

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import six

from nodeconductor.core.utils import hours_in_month
from nodeconductor.cost_tracking.models import DefaultPriceListItem

from . import __version__

UNIT_PREFIX = 'minute-of-'

logger = logging.getLogger(__name__)


class KillBillError(Exception):
    pass


class NotFoundKillBillError(KillBillError):
    pass


class KillBillBackend(object):
    """ Killbill backend -- http://killbill.io/api/
        Test settings:

        NODECONDUCTOR_KILLBILL['BACKEND'] = {
            'api_url': 'http://killbill.example.com:8080/1.0/kb/',
            'username': 'admin',
            'password': 'password',
            'api_key': 'bob',
            'api_secret': 'lazar',
        }
    """

    def __init__(self, customer=None):
        config = settings.NODECONDUCTOR_KILLBILL.get('BACKEND', {})
        self.api = KillBillAPI(**config)
        self.api_url = config.get('api_url', ':unknown:')
        self.customer = customer

    def __getattr__(self, name):
        try:
            return getattr(self.api, name)
        except AttributeError:
            raise KillBillError(
                "Method '%s' is not implemented for class '%s'" % (name, self.api.__class__.__name__))

    def __repr__(self):
        return 'Billing backend %s' % self.api_url

    def get_or_create_client(self):
        try:
            client = self.api.get_client_by_uuid(self.customer.uuid.hex)
            if self.customer.billing_backend_id != client['accountId']:
                self.customer.billing_backend_id = client['accountId']
                self.customer.save(update_fields=['billing_backend_id'])
        except NotFoundKillBillError:
            self.customer.billing_backend_id = self.api.add_client(
                email="%s@example.com" % self.customer.uuid,  # XXX: a fake email address unique to a customer
                name=self.customer.name,
                uuid=self.customer.uuid.hex)
            self.customer.save(update_fields=['billing_backend_id'])

        return self.customer.billing_backend_id

    def sync_customer(self):
        backend_id = self.get_or_create_client()
        client_details = self.api.get_client_details(backend_id)

        self.customer.balance = client_details['balance']
        self.customer.save(update_fields=['balance'])

    def sync_invoices(self):
        client_id = self.get_or_create_client()

        # Update or create invoices from backend
        cur_invoices = {i.backend_id: i for i in self.customer.killbill_invoices.all()}
        for invoice in self.api.get_invoices(client_id):
            cur_invoice = cur_invoices.pop(invoice['backend_id'], None)
            if cur_invoice:
                cur_invoice.date = invoice['date']
                cur_invoice.amount = invoice['amount']
                cur_invoice.save(update_fields=['date', 'amount'])
            else:
                cur_invoice = self.customer.killbill_invoices.create(
                    backend_id=invoice['backend_id'],
                    date=invoice['date'],
                    amount=invoice['amount'])

            cur_invoice.generate_pdf(invoice)
            cur_invoice.generate_usage_pdf(invoice)

        # Remove stale invoices
        map(lambda i: i.delete(), cur_invoices.values())

    def subscribe(self, resource):
        """ Return True if resource was not subscribed before """
        client_id = self.get_or_create_client()
        billing_backend_id = self.api.add_subscription(client_id, resource)
        if resource.billing_backend_id != billing_backend_id:
            resource.billing_backend_id = billing_backend_id
            resource.save(update_fields=['billing_backend_id'])
            return True
        return False

    def terminate(self, resource):
        self.api.del_subscription(resource.billing_backend_id)
        resource_model = resource.__class__
        if resource_model.objects.filter(pk=resource.pk).exists():
            resource.billing_backend_id = ''
            resource.save(update_fields=['billing_backend_id'])

    def add_usage_data(self, resource, usage_data):
        self.api.add_usage(resource.billing_backend_id, usage_data)

    def get_invoice_estimate(self, resource):
        client_id = self.get_or_create_client()
        return self.api.get_dry_invoice(client_id, resource.billing_backend_id)


class KillBillAPI(object):

    def __init__(self, api_url=None, username=None, password=None, api_key=None, api_secret=None, **kwargs):
        if not all((api_url, api_key, api_secret)):
            raise KillBillError(
                "Missed billing credentials. They must be supplied explicitly "
                "or defined within settings.NODECONDUCTOR_KILLBILL.BACKEND")

        self.currency = kwargs.get('currency', 'USD')
        self.credentials = dict(
            api_url=api_url,
            api_key=api_key,
            api_secret=api_secret,
            auth=(username, password))

        self.accounts = KillBill.Account(self.credentials)
        self.bundles = KillBill.Bundle(self.credentials)
        self.catalog = KillBill.Catalog(self.credentials)
        self.invoices = KillBill.Invoice(self.credentials)
        self.subscriptions = KillBill.Subscription(self.credentials)
        self.usages = KillBill.Usage(self.credentials)
        self.test = KillBill.Test(self.credentials)

    def _parse_invoice_data(self, raw_invoice):
        target_date = self._parse_date(raw_invoice['targetDate'])
        invoice = dict(
            backend_id=raw_invoice['invoiceId'],
            date=self._parse_date(raw_invoice['invoiceDate']),
            due_date=target_date + timedelta(hours=hours_in_month()),
            end_date=target_date,
            start_date=target_date - timedelta(hours=hours_in_month()),
            invoice_number=raw_invoice['invoiceNumber'],
            currency=raw_invoice['currency'],
            amount=raw_invoice['amount'],
            items=[],
        )

        for item in raw_invoice['items']:
            if item['amount']:
                fields = self.get_subscription_fields(item['subscriptionId'])
                if not fields:
                    logger.warn('Missing metadata, skipping invoice item %s' % item['invoiceItemId'])
                    continue
                invoice['items'].append(dict(
                    backend_id=item['invoiceItemId'],
                    name=item['usageName'] or item['description'],
                    service=fields['service_name'],
                    project=fields['project_name'],
                    resource=fields['resource_name'],
                    currency=item['currency'],
                    amount=item['amount'],
                ))

        return invoice

    def _parse_date(self, date):
        try:
            return datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError as e:
            raise KillBillError("Can't parse date %s: %s" % (date, e))

    def _get_plan_name_for_content_type(self, content_type):
        return "{}-{}".format(content_type.app_label, content_type.model)

    def _get_product_name_for_content_type(self, content_type):
        return self._get_plan_name_for_content_type(content_type).title().replace('-', '')

    def add_client(self, email=None, name=None, uuid=None, **kwargs):
        account = self.accounts.create(
            name=name, email=email, externalKey=uuid, currency=self.currency)
        return account['accountId']

    def get_client_details(self, client_id):
        account = self.accounts.get(client_id)
        return {'balance': account['accountBalance']}

    def get_client_by_uuid(self, uuid):
        return self.accounts.list(externalKey=uuid)

    def add_subscription(self, client_id, resource):
        # initial invoice is generated on subscribe (even with zero amount)
        # http://docs.killbill.io/0.15/userguide_subscription.html#five-minutes-create-subscription
        #
        # further invoices will be generated on monthly basis
        # one could use time shift to force it for testing purpose
        # example:
        #   backend = BillingBackend()
        #   backend.api.test.move_days(31)
        #
        # killbill server must be run in test mode for these tricks
        # -Dorg.killbill.server.test.mode=true

        try:
            subscriptions = self.bundles.list(externalKey=resource.uuid.hex)['subscriptions']
            subscription_id = subscriptions[0]['subscriptionId']
            self.update_subscription_fields(
                subscription_id,
                resource_name=resource.full_name,
                project_name=resource.project.full_name,
                service_name=resource.service_project_link.service.full_name)
            return subscription_id
        except NotFoundKillBillError:
            pass

        content_type = ContentType.objects.get_for_model(resource)
        product_name = self._get_product_name_for_content_type(content_type)
        subscription = self.subscriptions.create(
            productName=product_name,
            productCategory='STANDALONE',
            accountId=client_id,
            externalKey=resource.uuid.hex,
            billingPeriod='MONTHLY',
            priceList='DEFAULT')

        self.set_subscription_fields(
            subscription['subscriptionId'],
            resource_name=resource.full_name,
            project_name=resource.project.full_name,
            service_name=resource.service_project_link.service.full_name)

        return subscription['subscriptionId']

    def del_subscription(self, subscription_id):
        self.subscriptions.delete(subscription_id)

    def add_usage(self, subscription_id, usage_data):
        # Push hourly usage to backend
        # http://docs.killbill.io/0.14/consumable_in_arrear.html#_usage_and_metering
        today = self.test.list()['localDate'] or datetime.utcnow().date().strftime('%Y-%m-%d')
        self.usages.create(
            subscriptionId=subscription_id,
            unitUsageRecords=[{
                'unitType': unit,
                'usageRecords': [{
                    'recordDate': today,
                    'amount': str(amount),
                }],
            } for unit, amount in usage_data.items()])

    def get_dry_invoice(self, client_id, subscription_id):
        subscription = self.subscriptions.get(subscription_id)
        data = self.invoices.request(
            'invoices/dryRun',
            method='POST',
            accountId=client_id,
            targetDate=subscription['chargedThroughDate'])

        total = 0
        items = []
        for item in data['items']:
            if item['amount'] and item['subscriptionId'] == subscription_id:
                total += item['amount']
                items.append({
                    'name': item['description'].replace(' (usage item)', ''),
                    'amount': item['amount'],
                })

        return {
            'amount': total,
            'end_date': self._parse_date(data['targetDate']),
            'start_date': self._parse_date(subscription['billingStartDate']),
            'items': items}

    def get_invoices(self, client_id):
        invoices = self.accounts.get(client_id, 'invoices', withItems=True)
        return [self._parse_invoice_data(invoice) for invoice in invoices if invoice['amount']]

    def get_invoice(self, invoice_id):
        invoice = self.invoices.get(invoice_id, withItems=True)
        return self._parse_invoice_data(invoice)

    def get_invoice_items(self, invoice_id):
        return self.get_invoice(invoice_id)['items']

    def get_subscription_fields(self, subscription_id):
        fields = self.subscriptions.get(subscription_id, 'customFields')
        return {f['name']: f['value'] for f in fields}

    def set_subscription_fields(self, subscription_id, **data):
        fields = [{'name': key, 'value': val} for key, val in data.items()]
        self.subscriptions._object_query(
            subscription_id, 'customFields', method='POST',
            data=json.dumps(fields))

    def update_subscription_fields(self, subscription_id, **data):
        try:
            fields = self.subscriptions.get(subscription_id, 'customFields')
        except NotFoundKillBillError:
            pass
        else:
            flist = ','.join(f['customFieldId'] for f in fields if f['name'] in data)
            self.subscriptions._object_query(
                subscription_id, 'customFields', method='DELETE', customFieldList=flist)

        self.set_subscription_fields(subscription_id, **data)

    def propagate_pricelist(self):
        # Generate catalog and push it to backend
        # http://killbill.github.io/killbill-docs/0.15/userguide_subscription.html#components-catalog

        plans = E.plans()
        prods = E.products()
        units = set()
        plannames = []

        priceitems = DefaultPriceListItem.objects.values_list('resource_content_type', flat=True).distinct()
        for cid in priceitems:
            content_type = ContentType.objects.get_for_id(cid)
            plan_name = self._get_plan_name_for_content_type(content_type)
            product_name = self._get_product_name_for_content_type(content_type)

            usages = E.usages()
            for priceitem in DefaultPriceListItem.objects.filter(resource_content_type=cid):
                usage_name = re.sub(r'[\s:;,+%&$@/]+', '', "{}-{}-{}".format(priceitem.item_type, priceitem.key, cid))
                unit_name = UNIT_PREFIX + usage_name
                usage = E.usage(
                    E.billingPeriod('MONTHLY'),
                    E.tiers(E.tier(E.blocks(E.tieredBlock(
                        E.unit(unit_name),
                        E.size('1'),
                        E.prices(E.price(
                            E.currency(self.currency),
                            E.value(str(priceitem.value / 60)),  # compute minutely rate
                        )),
                        E.max('44640'),  # max minutes in a month
                    )))),
                    name=usage_name,
                    billingMode='IN_ARREAR',
                    usageType='CONSUMABLE')

                usages.append(usage)
                units.add(unit_name)

                priceitem.units = unit_name
                priceitem.save(update_fields=['units'])

            plan = E.plan(
                E.product(product_name),
                E.finalPhase(
                    E.duration(E.unit('UNLIMITED')),
                    E.recurring(  # recurring must be defined event if it's not used
                        E.billingPeriod('MONTHLY'),
                        E.recurringPrice(E.price(
                            E.currency(self.currency),
                            E.value('0'),
                        )),
                    ),
                    usages,
                    type='EVERGREEN'),
                name=plan_name)

            prods.append(E.product(E.category('STANDALONE'), name=product_name))

            plans.append(plan)
            plannames.append(plan_name)

        xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        catalog = ElementMaker(nsmap={'xsi': xsi}).catalog(
            E.effectiveDate(datetime.utcnow().isoformat("T")),
            E.catalogName('NodeConductor'),
            E.recurringBillingMode('IN_ADVANCE'),
            E.currencies(E.currency(self.currency)),
            E.units(*[E.unit(name=u) for u in units]),
            prods,
            E.rules(
                E.changePolicy(E.changePolicyCase(E.policy('END_OF_TERM'))),
                E.changeAlignment(E.changeAlignmentCase(E.alignment('START_OF_SUBSCRIPTION'))),
                E.cancelPolicy(
                    E.cancelPolicyCase(E.productCategory('STANDALONE'), E.policy('IMMEDIATE')),
                    E.cancelPolicyCase(E.policy('END_OF_TERM')),
                ),
                E.createAlignment(E.createAlignmentCase(E.alignment('START_OF_SUBSCRIPTION'))),
                E.billingAlignment(E.billingAlignmentCase(E.alignment('ACCOUNT'))),
                E.priceList(E.priceListCase(E.toPriceList('DEFAULT'))),
            ),
            plans,
            E.priceLists(E.defaultPriceList(E.plans(*[E.plan(n) for n in plannames]), name='DEFAULT')),
            **{'{{{}}}schemaLocation'.format(xsi): 'CatalogSchema.xsd'})

        xml = etree.tostring(
            catalog, xml_declaration=True, pretty_print=True, standalone=False, encoding='UTF-8')

        self.catalog.create(xml)


class KillBill(object):

    class BaseResource(object):
        path = NotImplemented
        type = 'application/json'

        def __init__(self, credentials):
            self.__dict__ = credentials

        def __repr__(self):
            return self.api_url + self.path

        def _object_query(self, uuid, entity=None, method='GET', data=None, **kwargs):
            return self.request(
                '/'.join([self.path, uuid, entity or '']), method=method, data=data, **kwargs)

        def list(self, **kwargs):
            return self.request(self.path, method='GET', **kwargs)

        def get(self, uuid, entity=None, **kwargs):
            return self._object_query(uuid, entity, **kwargs)

        def create(self, raw_data=None, **kwargs):
            data = raw_data or json.dumps(kwargs)
            return self.request(self.path, method='POST', data=data)

        def delete(self, uuid):
            return self.request('/'.join([self.path, uuid]), method='DELETE')

        def request(self, url, method='GET', data=None, verify=False, **kwargs):
            response_types = {'application/json': 'json', 'application/xml': 'xml'}
            headers = {'User-Agent': 'NodeConductor/%s' % __version__,
                       'Accept': 'application/json',
                       'X-Killbill-ApiKey': self.api_key,
                       'X-Killbill-ApiSecret': self.api_secret}

            if method.upper() in ('POST', 'DELETE'):
                headers['Content-Type'] = self.type
                headers['X-Killbill-CreatedBy'] = 'NodeConductor'

            if not urlparse.urlparse(url).netloc:
                url = self.api_url + url

            try:
                response = getattr(requests, method.lower())(
                    url, params=kwargs, data=data, auth=self.auth, headers=headers, verify=verify)
            except requests.ConnectionError as e:
                six.reraise(KillBillError, e)

            codes = requests.status_codes.codes
            response_type = response_types.get(response.headers.get('content-type'), '')

            if response.status_code == codes.created:
                location = response.headers.get('location')
                if location:
                    return self.request(location)

            elif response.status_code != codes.ok:
                reason = response.reason
                if response_type == 'json':
                    try:
                        reason = response.json()['message']
                    except ValueError:
                        pass
                elif response.status_code == codes.server_error:
                    try:
                        txt = etree.fromstring(response.text)
                        reason = txt.xpath('.//pre/text()')[1].split('\n')[2]
                    except ValueError:
                        pass

                error_message = "%s. Request to Killbill backend failed: %s" % (response.status_code, reason)
                if response.status_code == codes.not_found:
                    raise NotFoundKillBillError(error_message)
                raise KillBillError(error_message)

            try:
                if response_type == 'xml':
                    data = etree.fromstring(
                        response.text.encode('utf-8'),
                        etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8'))

                elif response_type == 'json' and response.text:
                    data = response.json()

                else:
                    data = response.text

            except ValueError as e:
                raise KillBillError(
                    "Incorrect response from Killbill backend %s: %s" % (url, e))

            return data

    class Account(BaseResource):
        path = 'accounts'

    class Bundle(BaseResource):
        path = 'bundles'

    class Catalog(BaseResource):
        path = 'catalog'
        type = 'application/xml'

    class Invoice(BaseResource):
        path = 'invoices'

    class Subscription(BaseResource):
        path = 'subscriptions'

    class Test(BaseResource):
        path = 'test/clock'

        def move_days(self, days=1):
            return self.request(self.path, method='PUT', days=days)

    class Usage(BaseResource):
        path = 'usages'
