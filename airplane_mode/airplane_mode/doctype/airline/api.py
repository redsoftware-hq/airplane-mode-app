import frappe
from frappe.utils.response import redirect

@frappe.whitelist(allow_guest=True)
def redirect_url():
    # Here you could add logic to fetch a specific URL from a doc if needed
    # For this example, we will redirect to a static URL
    return redirect("https://www.makemytrip.com/")
