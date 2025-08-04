### orders/forms.py

from django import forms
from .models import Wishlist, Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = []  # فقط course و user از initial پر می‌شوند

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'افزودن به علاقه‌مندی'))



class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'mobile', 'phone',
            'province', 'city', 'postal_code',
            'address', 'delivery_type', 'delivery_time', 'note'
        ]
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'mobile': 'شماره موبایل',
            'phone': 'تلفن ثابت',
            'province': 'استان',
            'city': 'شهر',
            'postal_code': 'کد پستی',
            'address': 'آدرس کامل',
            'delivery_type': 'نوع ارسال',
            'delivery_time': 'زمان ارسال موردنظر',
            'note': 'توضیحات تکمیلی',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'note': forms.Textarea(attrs={'rows': 2}),
            'delivery_time': forms.TextInput(attrs={'placeholder': 'مثلاً فردا صبح'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'ثبت و پرداخت سفارش'))
