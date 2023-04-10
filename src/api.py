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
            "subscriptions": self.url("/billing/subscriptions"),
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
        return data

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
        print(response.__dict__)
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
        }
        response = self.api.post(url, json=json)
        return self.handle_response(response)

    def create_plan(self, product_id, name, description, frequency, price):
        url = self.resources["plans"]
        json = {
            "product_id": product_id,
            "name": name,
            "description": description,
            "status": "ACTIVE",
            "billing_cycles": [
                {
                    "frequency": {"interval_unit": "MONTH", "interval_count": 1},
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 12,
                    "pricing_scheme": {
                        "fixed_price": {"value": price, "currency_code": "USD"}
                    },
                },
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee": {"value": price, "currency_code": "USD"},
                "setup_fee_failure_action": "CONTINUE",
                "payment_failure_threshold": 3,
            },
            "taxes": {"percentage": "10", "inclusive": False},
        }
        response = self.api.post(url, json=json)
        return self.handle_response(response)

    def create_product(
        self, name, type="DIGITAL", category="SOFTWARE", description
    ):
        url = self.resources["products"]
        json = {
            "name": name,
            "type": type,
            "category": category,
            "description": description,
        }
        response = self.api.post(url, json=json)
        return self.handle_response(response)
