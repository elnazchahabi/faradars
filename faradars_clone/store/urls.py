from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),

    # مسیرهای ثابت (مثل compare) باید قبل از مسیرهای داینامیک بیان
    path('compare/', views.compare_products, name='compare_products'),
    path('compare/add/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('compare/remove/<int:product_id>/', views.remove_from_compare, name='remove_from_compare'),

    # این مسیر آخر بیاد چون خیلی کلیه و هر slugی رو می‌گیره
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
