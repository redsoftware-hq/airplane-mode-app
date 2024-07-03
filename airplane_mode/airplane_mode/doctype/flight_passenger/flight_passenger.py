# Copyright (c) 2024, Ak and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		self.full_name = self.first_name + " " + self.last_name
