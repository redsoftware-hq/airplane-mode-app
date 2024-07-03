import frappe

def get_context(context):
    context.airports = frappe.get_all('Airport', fields=['name'])
    context.status_options = ['Lease', 'Occupied', 'All']
    filters = get_filters()
    context.shops = frappe.get_all('Shop Detail', filters=filters, fields=['shop_name', 'area', 'shop_owner', 'shop_number'])
    context.selected_airport = frappe.form_dict.get('airport', '')
    context.selected_status = frappe.form_dict.get('available_for_lease', 'All')
    return context

def get_filters():
    filters = {}
    airport = frappe.form_dict.get('airport')
    available_for_lease = frappe.form_dict.get('available_for_lease')

    if airport:
        filters['airport'] = airport
    if available_for_lease == 'Lease':
        filters['available_for_lease'] = 1
    elif available_for_lease == 'Occupied':
        filters['available_for_lease'] = 0

    return filters

