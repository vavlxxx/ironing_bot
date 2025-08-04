import aiohttp
import random
import time

from src.config import settings


class SMSRuClient:
    
    async def _generate_code(self) -> str:
        return f"{random.randint(0, 9999):04d}"

    async def send_sms(self, phone: str):
        if settings.SMSRU_MODE == 'TEST':
            return {'success': True, 'data': None, 'code': '1234', 'timeout': time.time() + 60, 'error': None}

        sms_code = await self._generate_code()
        message = f"{settings.SMSRU_DEFAULT_MSG} {sms_code}"

        params = {
            'api_id': settings.SMSRU_API_KEY,
            'from': settings.SMSRU_DEFAULT_FROM,
            'to': phone,
            'msg': message,
            'json': 1
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(settings.SMSRU_BASE_URL, data=params, timeout=30) as response:
                    result = await response.json()
            
            return {
                'success': result.get('status') == 'OK',
                'code': sms_code,
                'timeout': time.time() + 60,
                'data': result,
                'error': result.get('status_text') if result.get('status') != 'OK' else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f'Ошибка соединения: {str(e)}'
            }
           