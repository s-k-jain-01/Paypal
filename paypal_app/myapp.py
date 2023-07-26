{
    "id":"24D29317947314458",
    "amount":{
        "currency_code":"USD",
        "value":"5.00"
    },
    "final_capture":True,
    "seller_protection":{
        "status":"ELIGIBLE",
        "dispute_categories":[
            "ITEM_NOT_RECEIVED",
            "UNAUTHORIZED_TRANSACTION"
        ]
    },
    "seller_receivable_breakdown":{
        "gross_amount":{
            "currency_code":"USD",
            "value":"5.00"
        },
        "paypal_fee":{
            "currency_code":"USD",
            "value":"0.66"
        },
        "net_amount":{
            "currency_code":"USD",
            "value":"4.34"
        }
    },
    "status":"COMPLETED",
    "supplementary_data":{
        "related_ids":{
            "order_id":"7FT35626H99391441"
        }
    },
    "payee":{
        "email_address":"sb-1zfq726182938@business.example.com",
        "merchant_id":"YJU4JSS3NAYWL"
    },
    "create_time":"2023-07-19T06:09:26Z",
    "update_time":"2023-07-19T06:09:26Z",
    "links":[
        {
            "href":"https://api.sandbox.paypal.com/v2/payments/captures/24D29317947314458",
            "rel":"self",
            "method":"GET"
        },
        {
            "href":"https://api.sandbox.paypal.com/v2/payments/captures/24D29317947314458/refund",
            "rel":"refund",
            "method":"POST"
        },
        {
            "href":"https://api.sandbox.paypal.com/v2/checkout/orders/7FT35626H99391441",
            "rel":"up",
            "method":"GET"
        }
    ]
}