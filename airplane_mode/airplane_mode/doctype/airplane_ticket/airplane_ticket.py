# Copyright (c) 2024, Ak and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe.model.document import Document


class AirplaneTicket(Document):

	# def after_submit(self):
	# 	flight_doc = frappe.get_doc("Airplane Flight", self.flight)
	# 	flight_doc.status = "Completed"
	# 	flight_doc.save()
	# 	frappe.db.commit()

	def before_insert(self):
		flight_doc = frappe.get_doc("Airplane Flight", self.flight)
		airplane_doc = frappe.get_doc("Airplane", flight_doc.airplane)
		print("AA",frappe.db.count("Airplane Ticket", {"flight": self.flight}))
		if frappe.db.count("Airplane Ticket", {"flight": self.flight}) >= airplane_doc.capacity:
			frappe.throw("Airplane Ticket exceeds the limit")

	def validate(self):
		unique_add_ons = set()
		for add_on in self.add_ons:
			if add_on.item in unique_add_ons:
				frappe.throw("Duplicate add_on item found")
			else:
				unique_add_ons.add(add_on.item)
	def before_save(self):
		if self.status != "Boarded":
			frappe.throw("Status is not Boarded")
		else:
			total_child = 0	
			for item in self.add_ons:
				total_child += item.amount
		
			self.total_amount = self.flight_price + total_child
		
