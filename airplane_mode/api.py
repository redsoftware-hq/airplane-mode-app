import frappe # type: ignore
import json
import requests
from werkzeug.wrappers import Response # type: ignore
from frappe import _ # type: ignore
from hashlib import sha1
import hmac

@frappe.whitelist(allow_guest=True)
def handle_facebook_webhook():
    print("Entry....")
    if frappe.request.method == "GET":
        if (frappe.request.args.get("hub.mode") == "subscribe" and
            frappe.request.args.get("hub.verify_token") == '123456'):
            return Response(frappe.request.args.get("hub.challenge"), status=200, content_type='text/plain')
        else:
            return "Verification token mismatch", 403

    elif frappe.request.method == "POST":
        print("POST...")
        calculated_signature = calculate_signature(frappe.request.get_data())
        print("Calculated Signature: sha1=" + calculated_signature)

        if not verify_signature(frappe.request, "sha1=" + calculated_signature):
            return "Invalid signature", 401

        data = frappe.request.json
        frappe.logger().info("Facebook request body: {}".format(json.dumps(data)))
        process_facebook_updates(data)
        return {"status": "success"}

def calculate_signature(payload):
    print(payload)
    app_secret = "729e529f0981ce3323298a0ae36aae2b"
    mac = hmac.new(bytes(app_secret, 'utf-8'), msg=payload, digestmod=sha1)
    return mac.hexdigest()

def verify_signature(request, calculated_signature):
    signature = calculated_signature
    print(signature)
    if not signature:
        return False

    sha_name, signature = signature.split('=')
    mac = hmac.new(bytes('729e529f0981ce3323298a0ae36aae2b', 'utf-8'), msg=request.get_data(), digestmod=sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)

def process_facebook_updates(data):
    if "entry" in data:
        for entry in data["entry"]:
            if "changes" in entry:
                for change in entry["changes"]:
                    if change["field"] == "leadgen":
                        leadgen_id = change["value"]["leadgen_id"]
                        fetch_lead_data(leadgen_id)

def fetch_lead_data(leadgen_id):
    conf = frappe.get_conf()
    print("FETCH LEAD DATA....")
    url = f"https://graph.facebook.com/v11.0/{leadgen_id}"
    params = {"access_token": 'EAAfxEMSUu2YBO745OMMu4QSqeibeshzqFv0a8B8K2ReD8tbjVaU9n3W5aqIlszB5B7gMIAnH9Tqa0WauqQMBgyebzlSIGwjUGXGaYDgZClHM8Eb9NrAw9K4UeeV5cvUq1XrR3uVjFbsoZAWwe4sdRDay7Ng9ChC3ZBdW9gix2itCuxmgGI3dZCalLcgSS54ZD'}
    response = requests.get(url, params=params)
    print("RESPONSE", response)
    if response.status_code == 200: 
        lead_data = response.json()
        process_lead_data(lead_data , '8e515dca3e51fca', '600c0fd4bd83415')

def process_lead_data(lead_data, api_key, api_secret):
    print("Process Lead Data")
    field_data = lead_data.get("field_data", [])
    lead_info = {field["name"]: field["values"][0] for field in field_data}
    print(lead_info)
    
    # Format phone number if it contains a country code
    phone_number = lead_info.get("phone_number")
    if phone_number and phone_number.startswith("+"):
        phone_number = phone_number.replace(" ", "").replace("-", "")
        formatted_phone_number = f"{phone_number[:3]}-{phone_number[3:]}"
    else:
        formatted_phone_number = phone_number

    headers = {
        'Authorization': f'token 8e515dca3e51fca:600c0fd4bd83415',
        'Content-Type': 'application/json'
    }
    data = {
        "doctype": "Facebook Lead",
        "lead_name": lead_info.get("full_name"),
        "email_id": lead_info.get("email"),
        "mobile_no": formatted_phone_number
    }
    response = requests.post(f"https://demo-redsoft.frappe.cloud/api/resource/Facebook Lead", headers=headers, json=data)
    if response.status_code == 200:
        print("Lead created successfully")
    else:
        print(f"Failed to create lead: {response.text}")

def my_backgroun_job():
    print("Hey Background")
    frappe.logger().info(f"Running background task with")
    frappe.sleep(1)
    return "Task Completed"

frappe.enqueue("airplane_mode.api.my_backgroun_job")