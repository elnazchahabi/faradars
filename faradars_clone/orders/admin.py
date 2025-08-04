from django.contrib import admin
from .models import Order, Wishlist


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'mobile', 'delivery_type', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'delivery_type', 'created_at')
    search_fields = ('user__username', 'full_name', 'mobile', 'city', 'province')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('مشخصات کاربر', {
            'fields': ('user', 'full_name', 'mobile', 'phone')
        }),
        ('آدرس و ارسال', {
            'fields': ('province', 'city', 'postal_code', 'address', 'delivery_type', 'delivery_time')
        }),
        ('وضعیت سفارش', {
            'fields': ('is_paid', 'payment_ref', 'note', 'created_at')
        }),
    )

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'added_at')
    list_filter = ('course',)
    search_fields = ('user__username', 'course__title')
    readonly_fields = ('added_at',)
