# your_app/api.py

import frappe # type: ignore
import requests

@frappe.whitelist(allow_guest=True)
def handle_facebook_webhook():
    if frappe.request.method == "GET":
        if frappe.request.args.get("hub.mode") == "subscribe" and frappe.request.args.get("hub.verify_token") == "123":
            return frappe.request.args["hub.challenge"]
        else:
            return "Verification token mismatch", 403

    elif frappe.request.method == "POST":
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
            return frappe.utils.response.build_response("json", {"status": "success"})
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), _("Facebook Webhook Error"))
            return frappe.utils.response.build_response("json", {"status": "error", "message": str(e)})

def fetch_lead_data(leadgen_id, access_token):
    url = f"https://graph.facebook.com/v11.0/{leadgen_id}"
    params = {"access_token": access_token}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        lead_data = response.json()
        process_lead_data(lead_data)

def process_lead_data(lead_data):
    field_data = lead_data.get("field_data", [])
    lead_info = {field["name"]: field["values"][0] for field in field_data}
    frappe.get_doc({
        "doctype": "Facebook Lead",
        "lead_name": lead_info.get("full_name"),
        "email_id": lead_info.get("email"),
        "mobile_no": lead_info.get("phone_number")
    }).insert()
