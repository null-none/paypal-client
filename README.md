## paypal-client


```bash
pip install paypal-rest-api
```

#### Example

```python
from paypal_client.api import PayPal

paypal = PayPal(APP_CLIENT_ID, APP_SECRET)

product = paypal.create_product(name="Video Streaming Service", description="Video Streaming Service basic plan", type="SERVICE")
plan = paypal.create_plan(product_id=product["id"], name="Video Streaming Service Plan", description="Video Streaming Service basic plan", frequency="MONTH", price=10)
subscription = paypal.create_subscription(plan_id=plan["id"])
print(paypal.show_subscription_details(subscription["id"]))
```

