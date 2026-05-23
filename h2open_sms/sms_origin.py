import requests


class SmsOriginAPI:
	URL = "https://processor.smsorigin.com/xml/process.aspx"
	PLATFORM_ID = "1"

	def __init__(self, username: str, password: str, channel_code: str):
		self.username = username
		self.password = password
		self.channel_code = channel_code

	def send_sms(self, message: str, numbers: list[str], originator: str = "", concat: str = "1") -> str:
		numbers_str = ",".join(numbers) if isinstance(numbers, list) else numbers
		xml_payload = f"""<?xml version="1.0" encoding="ISO-8859-9"?>
<MainmsgBody>
    <Command>0</Command>
    <PlatformID>{self.PLATFORM_ID}</PlatformID>
    <UserName>{self.username}</UserName>
    <PassWord>{self.password}</PassWord>
    <ChannelCode>{self.channel_code}</ChannelCode>
    <Mesgbody>{message}</Mesgbody>
    <Numbers>{numbers_str}</Numbers>
    <Type>1</Type>
    <Originator>{originator}</Originator>
    <SDate></SDate>
    <EDate></EDate>
    <Concat>{concat}</Concat>
</MainmsgBody>"""
		headers = {"Content-Type": "text/xml; charset=ISO-8859-9"}
		response = requests.post(self.URL, data=xml_payload.encode("iso-8859-9"), headers=headers)
		response.raise_for_status()
		return response.text

	def get_credit(self) -> str:
		xml_payload = f"""<?xml version="1.0" encoding="ISO-8859-9"?>
<MainReportRoot>
    <Command>6</Command>
    <PlatformID>{self.PLATFORM_ID}</PlatformID>
    <UserName>{self.username}</UserName>
    <ChannelCode>{self.channel_code}</ChannelCode>
    <PassWord>{self.password}</PassWord>
</MainReportRoot>"""
		headers = {"Content-Type": "text/xml; charset=ISO-8859-9"}
		response = requests.post(self.URL, data=xml_payload.encode("iso-8859-9"), headers=headers)
		response.raise_for_status()
		return response.text
