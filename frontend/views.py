from django.shortcuts import render

def home_view(request):
    return render(request, 'base/home.html')

def login_view(request):
    return render(request, 'user/login.html')

def register_view(request):
    return render(request, 'user/register.html')

def product_list_view(request):
    return render(request, 'products/product_list.html')

def product_detail_view(request, product_id):
    return render(request, 'products/product_detail.html', {'product_id': product_id})

def cart_view(request):
    return render(request, 'cart/cart.html')

def checkout_view(request):
    return render(request, 'cart/checkout.html')

def profile_view(request):
    return render(request, 'user/profile.html')

def orders_view(request):
    return render(request, 'user/orders.html')