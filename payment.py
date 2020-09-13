import requests
from requests.auth import HTTPBasicAuth
import json
import uuid


def process_payment(merchant_email, amount, details):
    details_dict = {
        'email': details[0][0],
        'clientId': details[0][1],
        'secret': details[0][2],
        'ref': details[0][3]
    }
    # Generate unique UUID's for sender_batch_id
    batch_id = uuid.uuid4()
    # Parameters for making API requests
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    payload = 'grant_type=client_credentials'
    headers = {'Accept': 'application/json'}

    auth_header = {'Username': details_dict['clientId'],
                   'Password': details_dict['secret']}
    # POST request to get access token
    response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(
        auth_header['Username'], auth_header['Password']))

    access_token = response.json()['access_token']
    print(f'ACCESS TOKEN {access_token}')

    # Use the access token from response to create a batch payout
    url = "https://api.sandbox.paypal.com/v1/payments/payouts"

    payload = {
        "sender_batch_header": {
            "sender_batch_id": "Payouts_2020_"+str(batch_id),
            "email_subject": "You have a payout!",
            "email_message": "You have received a payout! Thanks for using our service!"
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": amount,
                    "currency": "USD"
                },
                "note": "Thanks for your patronage!",
                "sender_item_id": "201403140001",
                "receiver": merchant_email,
                "alternate_notification_method": {
                    "phone": {
                        "country_code": "91",
                        "national_number": "9999988888"
                    }
                }
            }
        ]
    }

    payload_json = json.dumps(payload)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    # POST request to make a payout

    response = requests.post(url, headers=headers, data=payload_json)

    print(f'PAYOUT {response.json()}')
    print(response.status_code)
    return response.status_code
