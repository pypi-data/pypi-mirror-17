# -*- coding: utf-8 -*-
'''
diacamma.invoice test_tools package

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2015 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals
from re import match
try:
    from urllib.parse import urlsplit, parse_qsl
except:
    from urlparse import urlsplit, parse_qsl
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from django.utils import six
from django.conf import settings

from lucterios.framework.test import LucteriosTest

from diacamma.accounting.test_tools import create_account
from diacamma.accounting.models import FiscalYear
from diacamma.payoff.models import BankAccount, PaymentMethod
from diacamma.payoff.views_deposit import BankTransactionList,\
    BankTransactionShow
from diacamma.payoff.views import ValidationPaymentPaypal


def default_bankaccount():
    create_account(['581'], 0, FiscalYear.get_current())
    BankAccount.objects.create(
        designation="My bank", reference="0123 456789 321654 12", account_code="512")
    BankAccount.objects.create(
        designation="PayPal", reference="paypal@moi.com", account_code="581")


def default_paymentmethod():
    PaymentMethod.objects.create(
        paytype=0, bank_account_id=1, extra_data='123456789\nAABBCCDD')
    PaymentMethod.objects.create(
        paytype=1, bank_account_id=1, extra_data='Truc\n1 rue de la Paix{[newline]}99000 LA-BAS')
    PaymentMethod.objects.create(
        paytype=2, bank_account_id=2, extra_data='monney@truc.org')


class PaymentTest(LucteriosTest):

    def check_email_msg(self, msg, itemid, title, amount='100.0', tax='0.0'):
        from lucterios.mailing.tests import decode_b64
        email_content = decode_b64(msg.get_payload())
        self.assertTrue('<html>this is a bill.<hr/>' in email_content, email_content)
        self.assertTrue(email_content.find('<u><i>IBAN</i></u>') != -1, email_content)
        self.assertTrue(email_content.find('123456789') != -1, email_content)
        self.assertTrue(email_content.find('<u><i>libellé à</i></u>') != -1, email_content)
        self.assertTrue(email_content.find('<u><i>adresse</i></u>') != -1, email_content)
        self.assertTrue(email_content.find('Truc') != -1, email_content)
        self.assertTrue(email_content.find('1 rue de la Paix<newline>99000 LA-BAS') != -1, email_content)
        self.check_paypal_msg(email_content, itemid, title, amount, tax)

    def check_paypal_msg(self, html_content, itemid, title, amount='100.0', tax='0.0'):
        paypal_href = match(".*<a href='(.*)' target='_blank'>.*", html_content)
        paypal_params = dict(parse_qsl(urlsplit(paypal_href.group(1)).query))
        self.assertEqual(paypal_params['currency_code'], 'EUR', paypal_params)
        self.assertEqual(paypal_params['lc'], 'fr', paypal_params)
        self.assertEqual(paypal_params['return'], 'http://testserver', paypal_params)
        self.assertEqual(paypal_params['cancel_return'], 'http://testserver', paypal_params)
        self.assertEqual(paypal_params['notify_url'], 'http://testserver/diacamma.payoff/validationPaymentPaypal', paypal_params)
        self.assertEqual(paypal_params['business'], 'monney@truc.org', paypal_params)
        self.assertEqual(paypal_params['item_name'], title, paypal_params)
        self.assertEqual(paypal_params['custom'], six.text_type(itemid), paypal_params)
        self.assertEqual(paypal_params['amount'], amount, paypal_params)
        self.assertEqual(paypal_params['tax'], tax, paypal_params)

    def check_payment(self, itemid, title, amount='100.0', tax='0.0'):
        self.assert_xml_equal(
            'COMPONENTS/LABELFORM[@name="lb_paymeth_1"]', '{[b]}virement{[/b]}')
        txt_value = self.get_first_xpath(
            'COMPONENTS/LABELFORM[@name="paymeth_1"]').text
        self.assertTrue(
            txt_value.find('{[u]}{[i]}IBAN{[/i]}{[/u]}') != -1, txt_value)
        self.assertTrue(txt_value.find('123456789') != -1, txt_value)

        self.assert_xml_equal(
            'COMPONENTS/LABELFORM[@name="lb_paymeth_2"]', '{[b]}chèque{[/b]}')
        txt_value = self.get_first_xpath(
            'COMPONENTS/LABELFORM[@name="paymeth_2"]').text
        self.assertTrue(
            txt_value.find('{[u]}{[i]}libellé à{[/i]}{[/u]}') != -1, txt_value)
        self.assertTrue(
            txt_value.find('{[u]}{[i]}adresse{[/i]}{[/u]}') != -1, txt_value)
        self.assertTrue(txt_value.find('Truc') != -1, txt_value)
        self.assertTrue(
            txt_value.find('1 rue de la Paix{[newline]}99000 LA-BAS') != -1, txt_value)

        self.assert_xml_equal(
            'COMPONENTS/LABELFORM[@name="lb_paymeth_3"]', '{[b]}PayPal{[/b]}')
        txt_value = self.get_first_xpath(
            'COMPONENTS/LABELFORM[@name="paymeth_3"]').text
        self.check_paypal_msg(txt_value.replace('{[', '<').replace(']}', '>'), itemid, title, amount, tax)
        return txt_value

    def check_payment_paypal(self, itemid, title, success=True, amount=100.0):
        paypal_validation_fields = {"txn_id": "2X7444647R1155525", "residence_country": "FR",
                                    "payer_status": "verified", "protection_eligibility": "Ineligible",
                                    "mc_gross": "%.2f" % amount, "charset": "windows-1252",
                                    "test_ipn": "1", "first_name": "test",
                                    "payment_date": "13:52:34 Apr 03, 2015 PDT", "transaction_subject": "",
                                    "ipn_track_id": "dda0f18cb9279", "shipping": "0.00",
                                    "item_number": "", "payment_type": "instant",
                                    "txn_type": "web_accept", "mc_fee": "3.67",
                                    "payer_email": "test-buy@gmail.com", "payment_status": "Completed",
                                    "payment_fee": "", "payment_gross": "",
                                    "business": "monney@truc.org", "tax": "0.00",
                                    "handling_amount": "0.00", "item_name": title,
                                    "notify_version": "3.8", "last_name": "buyer",
                                    "custom": "%d" % itemid, "verify_sign": "A7lgc2.jwEO6kvL1E5vEX03Q2la0A8TLpWtV5daGrDAvTm8c8AewCHR3",
                                    "mc_currency": "EUR", "payer_id": "BGZCL28GZVFHE",
                                    "receiver_id": "4P9LXTHC9TRYS", "quantity": "1",
                                    "receiver_email": "monney@truc.org", }

        self.factory.xfer = BankTransactionList()
        self.call('/diacamma.payoff/bankTransactionList', {}, False)
        self.assert_observer(
            'core.custom', 'diacamma.payoff', 'bankTransactionList')
        self.assert_count_equal(
            'COMPONENTS/GRID[@name="banktransaction"]/RECORD', 0)
        self.assert_count_equal(
            'COMPONENTS/GRID[@name="banktransaction"]/HEADER', 4)
        setattr(
            settings, "DIACAMMA_PAYOFF_PAYPAL_URL", "http://localhost:9100")
        httpd = TestHTTPServer(('localhost', 9100))
        httpd.start()
        try:
            self.factory.xfer = ValidationPaymentPaypal()
            self.call('/diacamma.payoff/validationPaymentPaypal',
                      paypal_validation_fields, False)
            self.assert_observer(
                'PayPal', 'diacamma.payoff', 'validationPaymentPaypal')
        finally:
            httpd.shutdown()

        self.factory.xfer = BankTransactionShow()
        self.call('/diacamma.payoff/bankTransactionShow',
                  {'banktransaction': 1}, False)
        self.assert_observer(
            'core.custom', 'diacamma.payoff', 'bankTransactionShow')
        self.assert_xml_equal(
            'COMPONENTS/LABELFORM[@name="date"]', "3 avril 2015 20:52")
        contains = self.get_first_xpath(
            'COMPONENTS/LABELFORM[@name="contains"]').text
        if success:
            self.assertEqual(
                len(contains), 1101 + len(title) + len("%.2f" % amount), contains)
        self.assertTrue("item_name = %s" % title in contains, contains)
        self.assertTrue("custom = %d" % itemid in contains, contains)
        self.assertTrue("business = monney@truc.org" in contains, contains)
        if success:
            self.assert_xml_equal(
                'COMPONENTS/LABELFORM[@name="status"]', "succès")
        else:
            self.assert_xml_equal(
                'COMPONENTS/LABELFORM[@name="status"]', "échec")
        self.assert_xml_equal(
            'COMPONENTS/LABELFORM[@name="payer"]', "test buyer")
        self.assert_xml_equal(
            'COMPONENTS/LABELFORM[@name="amount"]', "%.3f" % amount)

        self.factory.xfer = BankTransactionList()
        self.call('/diacamma.payoff/bankTransactionList', {}, False)
        self.assert_observer(
            'core.custom', 'diacamma.payoff', 'bankTransactionList')
        self.assert_count_equal(
            'COMPONENTS/GRID[@name="banktransaction"]/RECORD', 1)
        self.assert_count_equal(
            'COMPONENTS/GRID[@name="banktransaction"]/HEADER', 4)
        self.assert_xml_equal(
            'COMPONENTS/GRID[@name="banktransaction"]/RECORD[1]/VALUE[@name="date"]', '3 avril 2015 20:52')
        if success:
            self.assert_xml_equal(
                'COMPONENTS/GRID[@name="banktransaction"]/RECORD[1]/VALUE[@name="status"]', six.text_type('succès'))
        else:
            self.assert_xml_equal(
                'COMPONENTS/GRID[@name="banktransaction"]/RECORD[1]/VALUE[@name="status"]', six.text_type('échec'))
        self.assert_xml_equal(
            'COMPONENTS/GRID[@name="banktransaction"]/RECORD[1]/VALUE[@name="payer"]', 'test buyer')
        self.assert_xml_equal(
            'COMPONENTS/GRID[@name="banktransaction"]/RECORD[1]/VALUE[@name="amount"]', "%.3f" % amount)


class TestHTTPServer(HTTPServer, BaseHTTPRequestHandler, Thread):

    def __init__(self, server_address):
        HTTPServer.__init__(self, server_address, TestHandle)
        Thread.__init__(self, target=self.serve_forever)


class TestHandle(BaseHTTPRequestHandler):

    result = 'VERIFIED'

    def do_POST(self):
        """Respond to a POST request."""
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(self.result.encode())
