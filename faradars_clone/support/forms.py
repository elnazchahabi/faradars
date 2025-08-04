### support/forms.py

from django import forms
from .models import ContactMessage, NewsletterSubscription, BugReport,SupportTicket,TicketMessage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name','email','subject','message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'ارسال پیام'))

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'عضویت'))

class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ('email','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'ارسال گزارش'))





class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject']

class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'پیام خود را بنویسید...'}),
        }
