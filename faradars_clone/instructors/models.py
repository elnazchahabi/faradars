from django.db import models
from django.conf import settings

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="instructor_profile", verbose_name="کاربر")
    bio = models.TextField(blank=True, verbose_name="بیوگرافی")
    avatar = models.ImageField(upload_to='instructors/avatars/', blank=True, null=True, verbose_name="عکس پروفایل")
    skills = models.CharField(max_length=256, blank=True, verbose_name="مهارت‌ها (با کاما جدا کن)")
    linkedin = models.URLField(blank=True, verbose_name="لینک لینکدین")
    website = models.URLField(blank=True, verbose_name="وبسایت شخصی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    class Meta:
        verbose_name = "مدرس"
        verbose_name_plural = "مدرسین"

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class InstructorRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در حال بررسی'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)
    resume = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده؟")
    # اختیاری: فیلد برای رد درخواست
    is_rejected = models.BooleanField(default=False, verbose_name="رد شده؟")
    class Meta:
        verbose_name = "درخواست مدرس شدن"
        verbose_name_plural = "درخواست‌های مدرس شدن"

    def __str__(self):
        return self.user.get_full_name() or self.user.username
