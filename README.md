## paypal-client


```bash
pip install paypal-client
```

#### Example

```python
from paypal_client.api import PayPal

paypal = PayPal(APP_CLIENT_ID, APP_SECRET)

#paypal.create_product(name="Video Streaming Service", description="Video Streaming Service basic plan", type="SERVICE")
#paypal.create_plan(product_id="PROD-38B051282T0523342", name="Video Streaming Service Plan", description="Video Streaming Service basic plan", frequency="MONTH", price=10)
#subscription = paypal.create_subscription(plan_id="P-9SD64338HJ091711ENBJQYDI")  # Replace with your actual plan ID
print(paypal.show_subscription_details("I-FBNA66EU390B"))
print(paypal.show_plan_details("P-9SD64338HJ091711ENBJQYDI"))
```

