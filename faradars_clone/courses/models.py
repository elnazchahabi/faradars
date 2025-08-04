# Create your models here.
from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.utils import timezone


class Category(models.Model):
    title= models.CharField(max_length=100)
    slug= models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name= models.CharField(max_length=50, unique=True)
    slug= models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/thumbnails/')
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="قیمت با تخفیف")
    discount_expiration = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضای تخفیف")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    tags = models.ManyToManyField(Tag, blank=True, related_name='courses')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='unlocking_courses')
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    def total_buyers(self):
        return self.orders.count()

    def get_final_price(self):
        if self.discount_price and self.discount_expiration and self.discount_expiration > timezone.now():
            return self.discount_price
        return self.price

    def has_active_discount(self):
        return self.discount_price is not None and self.discount_expiration and self.discount_expiration > timezone.now()

    def discount_time_left(self):
        if self.has_active_discount():
            return self.discount_expiration - timezone.now()
        return None

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title= models.CharField(max_length=200)
    video= models.FileField(upload_to='courses/lessons/')
    is_preview= models.BooleanField(default=False)
    order= models.PositiveIntegerField(default=0)  # ← اضافه شد

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} – {self.title}"



class CourseReview(models.Model):
    course= models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating= models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    comment= models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating is None:
            raise ValidationError('امتیاز نباید خالی باشد')
        if not 1 <= self.rating <= 5:
            raise ValidationError('امتیاز باید بین ۱ تا ۵ باشد')

        
    class Meta:
        unique_together = ('course', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} – {self.course.title} ({self.rating})"


def user_has_course(user, course):
    if not user.is_authenticated:
        return False
    return course.orders.filter(user=user, is_paid=True).exists()





class CourseQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class CourseAnswer(models.Model):
    question = models.ForeignKey(CourseQuestion, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} پاسخ به {self.question.id}"






from django.contrib.auth import get_user_model
User = get_user_model()

class UserCourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progresses')
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    class Meta:
        unique_together = ('user', 'course')

    def progress_percentage(self):
        total = self.course.lessons.count()
        if total == 0:
            return 0
        return int((self.completed_lessons.count() / total) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.progress_percentage()}%"







