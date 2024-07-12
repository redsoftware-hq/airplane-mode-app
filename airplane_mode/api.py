# airplane_mode/api.py

import os
import frappe # type: ignore
import requests
from frappe import _ # type: ignore

@frappe.whitelist(allow_guest=True)
def handle_facebook_webhook():
    print("Entry....")
    try:
        data = frappe.request.json
        if "entry" in data:
            for entry in data["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        if change["field"] == "leadgen":
                            leadgen_id = change["value"]["leadgen_id"]
                            access_token = "your-page-access-token"
                            fetch_lead_data(leadgen_id, access_token)
        return {"status": "success"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Facebook Webhook Error"))
        return {"status": "error", "message": str(e)}

def fetch_lead_data(leadgen_id, access_token):
    conf = frappe.get_conf()
    print("FETCH LEAD DATA....")
    url = f"https://graph.facebook.com/v11.0/{leadgen_id}"
    params = {"access_token": conf.access_token}
    response = requests.get(url, params=params)
    print("RESPONSE", response)
    if response.status_code == 200:
        lead_data = response.json()
        process_lead_data(lead_data , conf.api_key, conf.api_secret)

def process_lead_data(lead_data, api_key, api_secret):
    field_data = lead_data.get("field_data", [])
    lead_info = {field["name"]: field["values"][0] for field in field_data}
    
    # Format phone number if it contains a country code
    phone_number = lead_info.get("phone_number")
    if phone_number and phone_number.startswith("+"):
        phone_number = phone_number.replace(" ", "").replace("-", "")
        formatted_phone_number = f"{phone_number[:3]}-{phone_number[3:]}"
    else:
        formatted_phone_number = phone_number

    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
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

