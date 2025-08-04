from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LoginHistory

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR', '')
    agent = request.META.get('HTTP_USER_AGENT', '')
    LoginHistory.objects.create(user=user, ip_address=ip, user_agent=agent)
