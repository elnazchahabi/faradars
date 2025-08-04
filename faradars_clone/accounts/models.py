from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import random

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'دانشجو'),
        ('instructor', 'مدرس'),
        ('admin', 'ادمین'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="نقش")
    is_instructor = models.BooleanField(default=False, verbose_name="مدرس است؟")
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="عکس پروفایل")
    bio = models.TextField(blank=True, verbose_name="بیو")
    mobile = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="شماره موبایل")
    is_email_verified = models.BooleanField(default=False, verbose_name="تأیید ایمیل")
    is_mobile_verified = models.BooleanField(default=False, verbose_name="تأیید موبایل")

    def __str__(self):
        return self.username


class LoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=45, blank=True, verbose_name="آی‌پی")
    user_agent = models.CharField(max_length=256, blank=True, verbose_name="مرورگر/دستگاه")

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class MobileOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.user.mobile} - {self.code} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"








class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="موجودی (ریال)")

    def __str__(self):
        return f"کیف پول {self.user.username} - موجودی: {self.balance} ریال"


class WalletTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('charge', 'شارژ کیف پول'),
        ('purchase', 'خرید'),
        ('refund', 'بازگشت وجه'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.wallet.user.username} | {self.get_transaction_type_display()} | {self.amount} ریال"




from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_wallet(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'wallet'):
        Wallet.objects.create(user=instance)
