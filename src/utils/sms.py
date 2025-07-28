from datetime import datetime, timedelta


async def send_sms(phone: str, text: str):
    code = "1234"
    expire = datetime.now() + timedelta(hours=5)
    return code, expire
