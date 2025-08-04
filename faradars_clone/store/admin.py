from django.contrib import admin
from .models import Product, Category, Tag  # اگر tag هم داری

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'category']
    list_filter = ['category', 'tags']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
