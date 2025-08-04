from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    category_slug = request.GET.get('category')
    tag_name = request.GET.get('tag')

    products = Product.objects.all()
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if tag_name:
        products = products.filter(tags__name=tag_name)

    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories
    })



from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # فیلتر بر اساس دسته و تگ‌ها
    similar_by_category = Product.objects.filter(category=product.category).exclude(id=product.id)

    similar_by_tags = Product.objects.filter(tags__in=product.tags.all()).exclude(id=product.id)

    # ترکیب و حذف تکراری‌ها
    similar = (similar_by_category | similar_by_tags).distinct()[:10]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'similar': similar,
    })



from django.http import JsonResponse
from django.shortcuts import redirect

def add_to_compare(request, product_id):
    compare_list = request.session.get('compare_list', [])
    if product_id not in compare_list:
        compare_list.append(product_id)
        request.session['compare_list'] = compare_list
    return redirect('store:compare_products')


def remove_from_compare(request, product_id):
    compare_list = request.session.get('compare_list', [])
    if product_id in compare_list:
        compare_list.remove(product_id)
        request.session['compare_list'] = compare_list
    return redirect('store:compare_products')


def compare_products(request):
    from .models import Product
    compare_list = request.session.get('compare_list', [])
    products = Product.objects.filter(id__in=compare_list)
    return render(request, 'store/compare.html', {
        'products': products
    })
