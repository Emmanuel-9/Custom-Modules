import logging

import requests

from .auth import MpesaBase

_logger = logging.getLogger(__name__)


class C2B(MpesaBase):
    def __init__(
        self,
        env="sandbox",
        app_key=None,
        app_secret=None,
        sandbox_url="https://sandbox.safaricom.co.ke",
        live_url="https://api.safaricom.co.ke",
    ):
        MpesaBase.__init__(self, env, app_key, app_secret, sandbox_url, live_url)
        self.authentication_token = self.authenticate()

    def register(
        self,
        shortcode=None,
        response_type=None,
        confirmation_url=None,
        validation_url=None,
    ):
        """This method uses Mpesa's C2B API to register validation and confirmation URLs on M-Pesa.

        **Args:**

        - `shortcode` (int): The short code of the organization.
        - `response_type` (str): Default response type for timeout. Incase a transaction times out,
        Mpesa will by default Complete or Cancel the transaction.
        - `confirmation_url` (str): Confirmation URL for the client.
        - `validation_url` (str): Validation URL for the client.

        **Returns:**

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.
        - `ConversationID` (str): The unique request ID returned by mpesa for each request made
        - `ResponseDescription` (str): Response Description message
        """
        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        _logger.debug(payload)
        _logger.debug(headers)
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v2/registerurl")
        try:
            r = requests.post(saf_url, headers=headers, json=payload, timeout=30)
        except Exception as e:
            _logger.error(e)
            r = requests.post(
                saf_url, headers=headers, json=payload, verify=False, timeout=30
            )
        return r.json()

    def simulate(
        self,
        shortcode=None,
        command_id=None,
        amount=None,
        msisdn=None,
        bill_ref_number=None,
    ):
        """This method uses Mpesa's C2B API to simulate a C2B transaction.
        **Args:**

        - `shortcode` (int): The short code of the organization.
        - `command_id` (str): Unique command for each transaction type. - CustomerPayBillOnline - CustomerBuyGoodsOnline.
        - `amount` (int): The amount being transacted
        - `msisdn` (int): Phone number (msisdn) initiating the transaction MSISDN(12 digits)
        - `bill_ref_number`: Optional

        **Returns:**

        - `OriginatorConverstionID` (str): The unique request ID for tracking a transaction.
        - `ConversationID` (str): The unique request ID returned by mpesa for each request made
        - `ResponseDescription` (str): Response Description message
        """
        payload = {
            "ShortCode": shortcode,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number,
        }
        headers = {
            "Authorization": "Bearer {0}".format(self.authentication_token),
            "Content-Type": "application/json",
        }
        if self.env == "production":
            base_safaricom_url = self.live_url
        else:
            base_safaricom_url = self.sandbox_url
        saf_url = "{0}{1}".format(base_safaricom_url, "/mpesa/c2b/v1/simulate")
        try:
            r = requests.post(saf_url, headers=headers, json=payload, timeout=30)
        except Exception as e:
            _logger.error(e)
            r = requests.post(
                saf_url, headers=headers, json=payload, verify=False, timeout=30
            )
        return r.json()
