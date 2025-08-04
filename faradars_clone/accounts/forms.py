from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from instructors.models import InstructorRequest

# ۱. فقط اگر می‌خواهی فرم ثبت‌نام allauth سفارشی باشه (فیلد موبایل و بیو اضافه شه):
from allauth.account.forms import SignupForm

class CustomAllauthSignupForm(SignupForm):
    mobile = forms.CharField(max_length=15, required=True, label='شماره موبایل')
    bio = forms.CharField(widget=forms.Textarea, required=False, label='درباره من')

    def save(self, request):
        user = super().save(request)
        user.mobile = self.cleaned_data['mobile']
        user.bio = self.cleaned_data['bio']
        user.save()
        return user

# ۲. فرم پروفایل برای ویرایش اطلاعات (این بمونه! لازم داری)
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

User = get_user_model()

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label='نام')
    last_name = forms.CharField(required=False, label='نام خانوادگی')
    email = forms.EmailField(required=True, label='ایمیل')
    mobile = forms.CharField(required=False, label='شماره موبایل')
    profile_image = forms.ImageField(required=False, label='عکس پروفایل')
    bio = forms.CharField(widget=forms.Textarea, required=False, label='درباره من')

    class Meta:
        model = User
        fields = ('first_name','last_name','email','mobile','profile_image','bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'بروزرسانی'))

    def save(self, commit=True):
        user = super().save(commit=False)
        orig = CustomUser.objects.get(pk=user.pk)
        if orig.email != user.email:
            user.is_email_verified = False
        if hasattr(user, 'mobile') and orig.mobile != user.mobile:
            user.is_mobile_verified = False
        if commit:
            user.save()
        return user

# ۳. فرم درخواست مدرس
class InstructorRequestForm(forms.ModelForm):
    class Meta:
        model = InstructorRequest
        fields = ['full_name', 'expertise', 'resume']
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'expertise': 'زمینه تخصصی',
            'resume': 'رزومه/توضیحات',
        }

# ۴. فرم موبایل و OTP
class MobileRequestForm(forms.Form):
    mobile = forms.CharField(max_length=20)

class OTPVerifyForm(forms.Form):
    code = forms.CharField(max_length=6)




from django import forms

class WalletChargeForm(forms.Form):
    amount = forms.IntegerField(label="مبلغ (ریال)", min_value=1000)
