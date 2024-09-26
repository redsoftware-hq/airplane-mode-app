// Copyright (c) 2024, Ak and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button("Assign Seat", () => {
			frappe.prompt(
				"Select Seat",
				({ value }) => {
					frm.set_value("seat", value);
					frm.save_or_update();
				},
				"Seat Number",
				"Assign"
			);
		});

		frm.set_query("target_link_field_Name", () => {
			return {
				filter: {
					"state": "GUJ"
				}
			}
		})
	},
});
