import json

import frappe
from frappe import _
from frappe.utils import nowdate

from h2open_sms.sms_origin import SmsOriginAPI


def send_sms(receiver_list, msg, sender_name="", success_msg=True):
	if isinstance(receiver_list, str):
		receiver_list = json.loads(receiver_list)
	if not isinstance(receiver_list, list):
		receiver_list = [receiver_list]

	settings = frappe.get_single("SMS Origin Settings")
	if not settings.username:
		frappe.throw(_("Please configure SMS Origin Settings"))

	api = SmsOriginAPI(
		username=settings.username,
		password=settings.get_password("password"),
		channel_code=settings.channel_code,
	)

	response = api.send_sms(
		message=msg,
		numbers=receiver_list,
		originator=settings.originator or "",
	)

	_create_sms_log(receiver_list, msg, response)

	if success_msg:
		frappe.msgprint(_("SMS sent successfully"))

	return response


def _create_sms_log(receiver_list, message, response):
	sl = frappe.new_doc("SMS Log")
	sl.sent_on = nowdate()
	sl.message = message
	sl.no_of_requested_sms = len(receiver_list)
	sl.requested_numbers = "\n".join(receiver_list)
	sl.no_of_sent_sms = len(receiver_list)
	sl.sent_to = "\n".join(receiver_list)
	sl.flags.ignore_permissions = True
	sl.save()
