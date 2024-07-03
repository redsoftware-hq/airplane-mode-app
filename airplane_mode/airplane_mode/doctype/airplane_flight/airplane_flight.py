# Copyright (c) 2024, Ak and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	
	def after_submit(self):
		self.status = "Completed"
