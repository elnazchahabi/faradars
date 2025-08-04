# Create your models here.
from django.db import models
from django.conf import settings



class ContactMessage(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField()
    subject= models.CharField(max_length=200)
    message= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – {self.subject}"

class NewsletterSubscription(models.Model):
    email= models.EmailField(unique=True)
    subscribed_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class BugReport(models.Model):
    email= models.EmailField(blank=True, null=True)
    description= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bug at {self.created_at:%Y-%m-%d %H:%M}"



class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'باز'),
        ('pending', 'در انتظار پاسخ'),
        ('answered', 'پاسخ داده شده'),
        ('closed', 'بسته شده'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.user}"

class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender} on {self.ticket}"
