import frappe
from frappe.utils import today

def send_rent_reminders():
    settings_doc = frappe.get_single('Shop Settings')
    if settings_doc.enable_rent_reminders:
        contracts = frappe.get_all('Contract Detail', fields=['tenant_information', 'shop_information'])
        print(contracts)
        for contract in contracts:
            tenant = frappe.get_doc('Tenant', contract['tenant_information'])
            send_email(tenant.email, tenant.name1, contract['shop_information'])

def send_email(email, tenant_name, shop_name):
    print(email, tenant_name, shop_name)
    subject = "Rent Due Reminder"
    message = f"Dear {tenant_name},<br><br>This is a reminder that your rent is due today for {shop_name}.<br><br>Thank you!"
    frappe.sendmail(recipients=email, subject=subject, message=message)

