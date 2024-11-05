"""
exteral delivery id
locale: location
order fullfilment method: order type
order_facility_id: merchant warehouse id
pickup_address
business name
phone number
instructions
reference tag

"""
import json
from datetime import datetime, timedelta
import jwt
import time
import math
import asyncio
import aiohttp
import django
from django.http import JsonResponse
from django.shortcuts import render
import requests
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doordrive.settings')
django.setup()


def ErrorHandler(code):
    match code:
        case 200:
            print("success!")
        case 400:
            print("missing params")
        case 401:
            print("auth error!, check jwt")
        case 403:
            print("auth error!")
        case 404:
            print("Link or delivery not found")
        case 409:
            print("try to cancel delivery which not exist/duplicate delivery id.")
        case 422:
            print("requested delivery outside coverage area.")
        case 429:
            print("too many req! try again later.")


BASE = "https://openapi.doordash.com/"

def jwt_token():
    cred = {
    "developer_id": "3722b49b-f38a-4472-9b75-19671cce4cd2",
    "key_id": "0d1fc2e2-b7e8-4a96-bb9c-c680dbbfbd2b",
    "signing_secret": "U2uXCd5-z1KK6k1od1RG5a-Jm-o9dkINrW-G3tS0yiw"
    }
    token = jwt.encode(
        {
            "aud": "doordash",
            "iss": cred["developer_id"],
            "kid": cred["key_id"],
            "exp": str(math.floor(time.time() + 300)),
            "iat": str(math.floor(time.time())),
        },
        jwt.utils.base64url_decode(cred["signing_secret"]),
        algorithm="HS256",
        headers={"dd-ver": "DD-JWT-V1"})
    return token

token = jwt_token()

import httpx
class helper:
    def __init__(self, header):
        self.header = header

    async def req(self, req_to_send, endpoint, type="POST"):
        delivery_info = {}
        async with httpx.AsyncClient() as client:
            if type == "POST":
                response = await client.post(BASE+endpoint, json=req_to_send, headers=self.header)

                return response
                
            elif type == "GET":
            #print("hI")
                response = await client.get(BASE+endpoint, headers=self.header) 
                return response 




import random

class API_Requests:
    def __init__(self, business_name=None,  pickup_addr=None, phone_number=None, p_instruction=None ,reference_tag=None, dropoff_addr=None, dropoff_phone=None, dropoff_inst=None, dfirst_name=None, dlast_name=None):
        #pickup info
        self.delivery_id = f"D-{random.randint(10000, 99999)}"
        self.locale = "en-US" #language to use
        self.order_fulfillment_method = "catering"
        self.pickup_addr = pickup_addr
        self.origin_facility_id = "merchant"
        self.p_instruction = p_instruction
        self.business_name = business_name
        self.phone_no = phone_number
        self.reference_tag = reference_tag #like order number
        
        #delviery info
        self.dropoff_addr = dropoff_addr
        self.droppoff_phone = dropoff_phone
        self.dfirst_name = dfirst_name
        self.actions_undelivered = "return_to_pickup"
        self.dropoff_inst = dropoff_inst
        self.dlast_name = dlast_name
        #time
        self.pickup_time = (datetime.now() + timedelta(minutes=10)).isoformat()
    
        self.headers = {"Accept-Encoding": "application/json",
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
                "dd-ver": "DD-JWT-V1"}
        self.help = helper(self.headers)
        

    async def create_quote(self):
        
        endpoint = "drive/v2/quotes"
        
        data = {
        "external_delivery_id": self.delivery_id,
        "locale": "en-US",
        "order_fulfillment_method": self.order_fulfillment_method,
        "pickup_address": self.pickup_addr,
        "pickup_phone_number": self.phone_no,
        "pickup_instructions": self.p_instruction,
        "pickup_reference_tag": self.reference_tag,
        
        
        "dropoff_address": self.dropoff_addr,
        "dropoff_phone_number": self.droppoff_phone,
        "dropoff_instructions": self.dropoff_inst,
        "dropoff_contact_given_name": self.dfirst_name,
        "dropoff_contact_family_name": self.dlast_name,
        "dropoff_contact_send_notifications": "true",
        #"pickup_time": self.pickup_time,
        "contactless_dropoff": "false",
        "action_if_undeliverable": self.actions_undelivered,
        "order_contains": {
            "alcohol": "false",
            "pharmacy_items": "false",
            "age_restricted_pharmacy_items": "false",
            "tobacco": "false",
            "hemp": "false",
            "otc": "false"
        },
        "dropoff_requires_signature": "false",
        }
        ret = await self.help.req(data, endpoint)

        return ret


    async def accept_quote(self, del_id):
        endpoint = f"drive/v2/quotes/{del_id}/accept"
        ret = await self.help.req({"external_delivery_id": del_id},endpoint)    
        return ret
    async def get_update(self, del_id):
        endpoint = f"drive/v2/deliveries/{del_id}"
        ret = await self.help.req({"external_delivery_id": del_id}, endpoint, "GET")
        return ret
    def get_quote(self, res):
        res = json.loads(res.text)
        tracking_url = res["tracking_url"]
        fee = res["fee"]
        currency = res["currency"]

        return tracking_url, fee, currency, res["dasher_id"]
    
    def get_dasher_details(self, res):
        res = json.loads(res.text)
        print(res)
        ret = {"id":res["dasher_id"],
               "name": res["dasher_name"],
               "dropoff_phone_number": res["dasher_dropoff_phone_number"],"pickup_phone_number": res["dahser_pickup_phone_number"],
               "location": res["dasher_location"],
               "vehicle_make":res["dasher_vehicle_make"],
               "vehicle_model": res["dasher_vehicle_model"],
               "vehicle_year": res["dasher_vehicle_year"],}
        return ret
cq = API_Requests("Wells Fargo SF Downtown",  "901 Market Street 6th Floor San Francisco, CA 94103","+16505555555", "Go to the bar for pick up.", "Order number 61", "901 Market Street 6th Floor San Francisco, CA 94103", "+16505555555",  "Enter gate code 1234 on the callbox.", "John", "Doe")

#response = asyncio.run(cq.create_quote())
#response = asyncio.run(cq.accept_quote("D-41527"))