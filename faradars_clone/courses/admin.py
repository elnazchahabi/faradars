from django.contrib import admin
from .models import Category, Tag, Course, Lesson, CourseReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ('title','slug')
    prepopulated_fields= {'slug':('title',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'instructor', 'category',
        'price', 'discount_price', 'discount_expiration',
        'is_discount_active', 'created_at'
    )
    search_fields = ('title','instructor__username')
    list_filter = ('category','instructor','tags')
    filter_horizontal = ('tags', 'prerequisites')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'thumbnail', 'instructor', 'category', 'tags', 'prerequisites')
        }),
        ('قیمت‌گذاری', {
            'fields': ('price', 'discount_price', 'discount_expiration')
        }),
        ('متفرقه', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)

    def is_discount_active(self, obj):
        return obj.has_active_discount()
    is_discount_active.boolean = True
    is_discount_active.short_description = "تخفیف فعال؟"

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title','course','order','is_preview')
    list_filter  = ('course','is_preview')

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('user','course','rating','created_at')
    list_filter  = ('rating',)
    search_fields = ('user__username', 'course__title')
