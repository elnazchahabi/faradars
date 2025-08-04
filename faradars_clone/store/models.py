from django.db import models



# ✅ models.py در اپ store
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    is_digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_similar_products(self):
        return Product.objects.filter(category=self.category).exclude(id=self.id)[:4]