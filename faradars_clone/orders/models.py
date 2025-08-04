# Create your models here.

from django.db import models
from django.conf import settings
from courses.models import Course


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_ref = models.CharField(max_length=100, blank=True, null=True)  # شماره پیگیری بانک/درگاه
    # فیلدهای اضافی مثل مبلغ کل، تخفیف و ... هم می‌تونه اضافه بشه
    DELIVERY_CHOICES = (
    ('normal', 'ارسال عادی'),
    ('express', 'ارسال فوری'),
    ('digital', 'تحویل دیجیتال'),
)

    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='digital', verbose_name="نوع ارسال")
    delivery_time = models.CharField(max_length=100, blank=True, null=True, verbose_name="زمان‌بندی ارسال")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس کامل")
    note = models.TextField(blank=True, null=True, verbose_name="توضیحات سفارش")
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    mobile = models.CharField(max_length=15, verbose_name="شماره موبایل")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="تلفن ثابت")
    province = models.CharField(max_length=100, verbose_name="استان")
    city = models.CharField(max_length=100, verbose_name="شهر")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def total_price(self):
        return sum(item.price for item in self.items.all())



from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    item_object = GenericForeignKey('content_type', 'object_id')

    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.item_object)

    # def get_type(self):
    #     return self.content_type.model
    def get_type(self):
        if self.content_type:
            return self.content_type.model
        return 'نامشخص'




# Wishlist هم مثل مدل فعلی خوبه و می‌تونه همون بمونه




class Wishlist(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} ♥ {self.course.title}"




# def user_has_course(user, course):
#     if not user.is_authenticated:
#         return False
#     return OrderItem.objects.filter(order__user=user, order__is_paid=True, course=course).exists()           

def user_has_course(user, course):
    return OrderItem.objects.filter(
        order__user=user,
        order__is_paid=True,
        content_type=ContentType.objects.get_for_model(course.__class__),
        object_id=course.id
    ).exists()
