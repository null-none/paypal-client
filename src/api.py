import requests


class PayPal:
    def __init__(self, client_id, app_secret, sandbox=True):
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

    def catalogs(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.access_token),
        }
        return requests.get(
            url="{}/v1/catalogs/".format(self.PAYPAL_URL), headers=headers
        )
