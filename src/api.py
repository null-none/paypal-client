import requests

from .exceptions import ValidationError, AuthorizationError, FailedRequest


class PayPal:
    def __init__(
        self, client_id, app_secret, sandbox=True, website="https://example.com"
    ):
        self.client_id = client_id
        self.secret = app_secret

        self.api_url = "https://api-m.paypal.com"
        if sandbox:
            self.api_url = "https://api-m.sandbox.paypal.com"

        access_token = self.get_access_token()

        api = requests.Session()
        api.headers.update({"Authorization": f"Bearer {access_token}"})
        self.api = api
        self.website = website

        self.resources = {
            "products": self.url("/catalogs/products"),
            "plans": self.url("/billing/plans"),
            "plans": self.url("/billing/plans"),
            "orders": self.url("/checkout/orders", 2),
        }

    def url(self, path, version=1):
        if version == 2:
            return self.api_url + "/v2" + path
        else:
            return self.api_url + "/v1" + path

    def get_access_token(self):
        url = self.url("/oauth2/token")
        auth = (self.client_id, self.secret)
        result = requests.post(
            url,
            data={"grant_type": "client_credentials"},
            auth=auth,
            headers={"Accept": "application/json", "Accept-Language": "en_US"},
        )
        if result.status_code == 200:
            return result.json()["access_token"]
        else:
            return None

    def handle_response(self, response):
        status_code = response.status_code
        data = response.json()
        if status_code >= 200 and status_code < 300:
            return data
        else:
            if status_code == 401:
                message = data["error"]
                payload = data["error_description"]
                raise AuthorizationError(message, payload)
            message = data["message"]
            payload = data["details"]
            if status_code == 400:
                raise ValidationError(message, payload)
            raise FailedRequest(message, status_code, payload)

    def list_products(self):
        url = self.resources["products"]
        response = self.api.get(url)
        data = response.json()
        return self.handle_response(response)

    def list_plans(self):
        url = self.resources["plans"]
        response = self.api.get(url)
        return self.handle_response(response)

    def show_plan_details(self, id):
        url = self.resources["plans"] + f"/{id}"
        response = self.api.get(url)
        return self.handle_response(response)

    def show_subscription_details(self, id):
        url = self.resources["subscriptions"] + f"/{id}"
        response = self.api.get(url)
        return self.handle_response(response)

    def list_transactions_for_subscription(self, id):
        url = self.resources["subscriptions"] + f"/{id}/transactions"
        response = self.api.get(url)
        return self.handle_response(response)

    def create_subscription(self, plan_id):
        url = self.resources["subscriptions"]
        response = self.api.post(url, json={"plan_id": plan_id})
        return self.handle_response(response)

    def cancel_subscription(self, id, reason):
        url = self.resources["subscriptions"] + f"/{id}/cancel"
        response = self.api.post(url, json={"reason": reason})
        return self.handle_response(response)

    def activate_subscription(self, id, reason):
        url = self.resources["subscriptions"] + f"/{id}/activate"
        response = self.api.post(url, json={"reason": reason})
        return self.handle_response(response)

    def create_subscription(self, plan_id):
        url = self.resources["subscriptions"]
        response = self.api.post(url, json={"plan_id": plan_id})
        return self.handle_response(response)

    def create_order(self, reference_id, value, name):
        url = self.resources["orders"]
        json = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": str(reference_id),
                    "amount": {"currency_code": "USD", "value": value},
                }
            ],
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                        "payment_method_selected": "PAYPAL",
                        "brand_name": "BRAND INC",
                        "locale": "en-US",
                        "landing_page": "LOGIN",
                        "shipping_preference": "SET_PROVIDED_ADDRESS",
                        "user_action": "PAY_NOW",
                        "return_url": f"{self.website}/return",
                        "cancel_url": f"{self.website}/cancel",
                    }
                }
            },
        }
        response = self.api.post(
            url, json=json, headers={"PayPal-Request-Id": str(reference_id)}
        )
        return self.handle_response(response)
