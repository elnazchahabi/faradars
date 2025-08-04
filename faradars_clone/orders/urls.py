from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('cart/add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/review/', views.review_order, name='review_order'),
    path('history/', views.order_list, name='order_list'),
    path('history/<int:pk>/', views.order_detail, name='order_detail'),
    path('cart/add/<str:model_name>/<int:object_id>/', views.add_to_cart, name='add_to_cart'),
]
