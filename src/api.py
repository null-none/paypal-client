import requests
from schema import Schema

from . import exceptions


class PayPal:
    def __init__(
        self, client_id, app_secret, website="https://example.com/", sandbox=True
    ):
        self.website = website
        if sandbox:
            self.PAYPAL_URL = "https://api-m.sandbox.paypal.com"
        else:
            self.PAYPAL_URL = "https://api-m.paypal.com"
        APP_CLIENT_ID = client_id
        APP_SECRET = app_secret

        oauth_url = "{}/v1/oauth2/token".format(self.PAYPAL_URL)

        oauth_response = requests.post(
            oauth_url,
            headers={"Accept": "application/json", "Accept-Language": "en_US"},
            auth=(APP_CLIENT_ID, APP_SECRET),
            data={"grant_type": "client_credentials"},
        )
        oauth_body_json = oauth_response.json()
        self.access_token = oauth_body_json["access_token"]

    def products(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.access_token),
        }
        return requests.get(
            url="{}/v1/catalogs/products".format(self.PAYPAL_URL), headers=headers
        )

    def create_order(self, reference_id, value):
        schema = Schema({"reference_id": str, "value": int})
        data = {"reference_id": reference_id, "value": value}
        if schema.is_valid(data):
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.access_token),
            }
            data = {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "reference_id": reference_id,
                        "amount": {"currency_code": "USD", "value": value},
                    }
                ],
                "payment_source": {
                    "paypal": {
                        "experience_context": {
                            "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                            "payment_method_selected": "PAYPAL",
                            "brand_name": "EXAMPLE INC",
                            "locale": "en-US",
                            "landing_page": "LOGIN",
                            "shipping_preference": "SET_PROVIDED_ADDRESS",
                            "user_action": "PAY_NOW",
                            "return_url": "{}returnUrl".format(self.website),
                            "cancel_url": "{}cancelUrl".format(self.website),
                        }
                    }
                },
            }
            response = requests.post(
                url="{}/v2/checkout/orders".format(self.PAYPAL_URL),
                data=data,
                headers=headers,
            )
            if response.status_code != 201:
                raise exceptions.Error(response.body)
            return response
        else:
            return schema.validate(data)
