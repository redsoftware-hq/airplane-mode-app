# Copyright (c) 2024, Ak and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
		{'fieldname': 'airline', 'label': 'Airline', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'revenue', 'label': 'Revenue', 'fieldtype': 'Currency', 'width': 150},
	]
    data = []
    parent = frappe.db.sql("""
        SELECT 
            t3.airline AS airline,
            SUM(t1.total_amount) AS revenue
        FROM 
            `tabAirplane Ticket` t1
        JOIN 
            `tabAirplane Flight` t2 ON t1.flight = t2.name
        JOIN 
            `tabAirplane` t3 ON t2.airplane = t3.name
        GROUP BY 
            t3.name
        ORDER BY 
            revenue DESC
    """, as_dict=1)
    
    total_revenue = 0
    
    chart = {'data':{'labels': [item.airline for item in parent] ,'datasets':[{'values':[item.revenue for item in parent]}]},'type':'donut'}
    
    for item in parent:
        total_revenue += item.revenue
    parent.append({"airline":"Total","revenue":total_revenue})
    report_summary = [
    {"label":"Total Revenue","value":total_revenue,'indicator':'green'},
	]
    
    return columns, parent, None, chart, report_summary
	# data = []

# 	columns = ["Airline", "Revenue"]
# 	data = [['1', 1], ["2", 2]]
# 	chart = {'data':{'labels':['d','o','g','s'],'datasets':[{'values':[3,6,4,7]}]},'type':'donut'}
# 	report_summary = [
#     {"label":"cats","value":2287,'indicator':'Red'},
#     {"label":"dogs","value":3647,'indicator':'Blue'}
# ]
# 	return columns, data, None, chart, report_summary
