# orders/views.py
# Create your views here.
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Order, OrderItem
from django.contrib import messages
from .forms import CheckoutForm

from orders.models import Order, OrderItem


@login_required
def add_to_cart(request, model_name, object_id):
    from django.contrib.contenttypes.models import ContentType
    model = ContentType.objects.get(model=model_name).model_class()
    obj = get_object_or_404(model, id=object_id)

    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    content_type = ContentType.objects.get_for_model(obj)

    item, created = OrderItem.objects.get_or_create(
        order=order,
        content_type=content_type,
        object_id=obj.id,
        defaults={'price': obj.price}
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('orders:cart_detail')


@login_required
def cart_detail(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    items = order.items.all() if order else []
    return render(request, 'orders/cart_detail.html', {'order': order, 'items': items})




@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_paid=False)

    item.delete()
    # می‌تونی پیام موفقیت با Django messages اضافه کنی (فعلاً ساده)
    return redirect('orders:cart_detail')





@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    if not order or order.items.count() == 0:
        messages.error(request, "سبد خرید شما خالی است!")
        return redirect('orders:cart_detail')

    if request.method == "POST":
        form = CheckoutForm(request.POST, instance=order)
        if form.is_valid():
            # ذخیره اطلاعات در session برای نمایش در صفحه بعدی
            request.session['order_data'] = form.cleaned_data
            return redirect('orders:review_order')
    else:
        form = CheckoutForm(instance=order)

    return render(request, 'orders/checkout.html', {
        'order': order,
        'items': order.items.all(),
        'form': form
    })


@login_required
def review_order(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    data = request.session.get('order_data')

    if not order or not data:
        messages.error(request, "اطلاعات سفارش یافت نشد.")
        return redirect('orders:checkout')

    if request.method == "POST":
        for field, value in data.items():
            setattr(order, field, value)
        order.is_paid = True
        order.save()
        request.session.pop('order_data', None)
        messages.success(request, "سفارش با موفقیت پرداخت شد.")
        return redirect('orders:order_list')

    return render(request, 'orders/review_order.html', {
        'order': order,
        'items': order.items.all(),
        'data': data
    })


# orders/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

# … توابع add_to_cart, cart_detail, remove_from_cart, checkout …

@login_required
def order_list(request):
    """
    لیست سفارش‌های پرداخت‌شدهٔ کاربر
    """
    orders = Order.objects.filter(user=request.user, is_paid=True).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    """
    جزئیات یک سفارش مشخص (با pk)
    """
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})




