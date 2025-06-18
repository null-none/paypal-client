## paypal-client


```bash
pip install paypal-client
```

#### Example

```python
from paypal_client.api import PayPal

APP_CLIENT_ID = (
    "..FsDR4_spBk1yOzXQsVFOtTPHZOjo6Yd75h07SGnIu1ppx"..
)
APP_SECRET = (
    "..J4IxLsVOmtmCKp6QxdN-6CpYCVuZ.."
)
paypal = PayPal(APP_CLIENT_ID, APP_SECRET)
print(paypal.list_products())
print(paypal.list_plans())

```

