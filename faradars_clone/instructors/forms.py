### instructors/forms.py

from django import forms
from .models import InstructorRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class InstructorRequestForm(forms.ModelForm):
    class Meta:
        model = InstructorRequest
        fields = ('motivation', 'portfolio_url')
        widgets = {'motivation': forms.Textarea(attrs={'rows':4})}
        labels = {
            'motivation': 'انگیزه شما برای مدرس شدن',
            'portfolio_url': 'آدرس نمونه‌کار (اختیاری)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'ارسال درخواست'))

    def clean(self):
        cleaned = super().clean()
        user = getattr(self.instance, 'user', None) or self.initial.get('user')
        if user and InstructorRequest.objects.filter(user=user).exists():
            raise forms.ValidationError('شما قبلاً درخواست داده‌اید.')
        return cleaned