// Copyright (c) 2024, Ak and contributors
// For license information, please see license.txt

frappe.ui.form.on("Contract Detail", {
	refresh(frm) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Shop Settings",
				name: "Shop Settings",
			},
			callback: function (r) {
				frm.set_value("rent", r.message.default_rent);
			},
		});
	},
});
