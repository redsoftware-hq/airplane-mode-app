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
    print("FETCH LEAD DATA....")
    url = f"https://graph.facebook.com/v11.0/{leadgen_id}"
    params = {"access_token": os.environ.get('ACCESS_TOKEN')}
    response = requests.get(url, params=params)
    print("RESPONSE", response)
    if response.status_code == 200:
        lead_data = response.json()
        process_lead_data(lead_data)

def process_lead_data(lead_data):
    print("Process Lead Data..")
    field_data = lead_data.get("field_data", [])
    lead_info = {field["name"]: field["values"][0] for field in field_data}
    print(lead_info)
    frappe.get_doc({
        "doctype": "Facebook Lead",
        "lead_name": lead_info.get("full_name"),
        "email_id": lead_info.get("email"),
        "mobile_no": lead_info.get("phone_number")
    }).insert()
