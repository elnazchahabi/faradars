from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    views       = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug])

class Tag(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    slug        = models.SlugField(unique=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "تگ‌ها"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_list_by_tag', args=[self.slug])

class Post(models.Model):
    LEVEL_CHOICES = [
        ('beginner',     'مقدماتی'),
        ('intermediate', 'متوسط'),
        ('advanced',     'پیشرفته'),
    ]
    STATUS_CHOICES = [
        ('draft',     'پیشنویس'),
        ('published', 'منتشر شده'),
        ('scheduled', 'زمان‌بندی شده'),
    ]

    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True)
    content         = models.TextField()
    excerpt         = models.TextField(blank=True, null=True)
    thumbnail       = models.ImageField(upload_to='blog/thumbnails/', blank=True, null=True)
    og_image        = models.ImageField(upload_to='blog/og/', blank=True, null=True)
    level           = models.CharField(max_length=12, choices=LEVEL_CHOICES, default='beginner', verbose_name='سطح')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    published_date  = models.DateTimeField(default=timezone.now)
    status          = models.CharField(max_length=12, choices=STATUS_CHOICES, default='published')
    is_featured     = models.BooleanField(default=False)
    meta_description= models.CharField(max_length=160, blank=True)
    meta_keywords   = models.CharField(max_length=200, blank=True)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    category        = models.ForeignKey(Category, related_name='posts', null=True, blank=True, on_delete=models.SET_NULL)
    tags            = models.ManyToManyField(Tag, related_name='posts', blank=True)
    liked_by   = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts',   blank=True)
    disliked_by= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_posts',blank=True)

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    @property
    def likes(self):
        return self.liked_by.count()

    @property
    def dislikes(self):
        return self.disliked_by.count()
    

class Comment(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    post       = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    parent     = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved   = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user or 'مهمان'} - {self.content[:20]}"

class NewsletterSubscription(models.Model):
    email         = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'اشتراک خبرنامه'
        verbose_name_plural = 'اشتراک‌های خبرنامه'

    def __str__(self):
        return self.email