import requests
import json

url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"

payload = json.dumps({
  "intent": "CAPTURE",
  "purchase_units": [
    {
      "items": [
        {
          "name": "T-Shirt",
          "description": "Green XL",
          "quantity": "1",
          "unit_amount": {
            "currency_code": "USD",
            "value": "100.00"
          }
        }
      ],
      "amount": {
        "currency_code": "USD",
        "value": "100.00",
        "breakdown": {
          "item_total": {
            "currency_code": "USD",
            "value": "100.00"
          }
        }
      }
    }
  ],
  "application_context": {
    "return_url": "https://example.com/return",
    "cancel_url": "https://example.com/cancel"
  }
})
headers = {
  'Content-Type': 'application/json',
  'Prefer': 'return=representation',
  'PayPal-Request-Id': '809f03e0-127b-4c43-87ef-fa0fdc4182fa',
  'Authorization': 'Bearer A21AALpyd_GovQiBdIdK1WNrfr41Ar2guBPDuHqsXqYkmMohi9I-ylTkE6rm_X4zVUEAmBvI14ey-Bjei-_XDE7MWAWzup0qA'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)