# Copyright (c) 2024, Ak and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airplane(Document):
	def validate(self):
		if self.capacity < frappe.db.count("Airplane"):
			frappe.throw("Seats are not available")
