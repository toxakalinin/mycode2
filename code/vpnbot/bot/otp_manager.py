import random
import time

class OTPManager:
    def __init__(self):
        self.otp_store = {}  # Словарь для хранения OTP {telegram_id: (otp, expiration_time)}

    def generate_otp(self, telegram_id, expiration):
        otp = random.randint(100000, 999999)
        expiration_time = time.time() + expiration
        self.otp_store[telegram_id] = (otp, expiration_time)
        return otp

    def verify_otp(self, telegram_id, otp):
        if telegram_id not in self.otp_store:
            return False
        stored_otp, expiration_time = self.otp_store[telegram_id]
        if time.time() > expiration_time:
            del self.otp_store[telegram_id]  # Удаляем истекший код
            return False
        if stored_otp == otp:
            del self.otp_store[telegram_id]  # Удаляем использованный код
            return True
        return False
