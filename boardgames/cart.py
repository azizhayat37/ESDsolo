# cart and checkout logic for the boardgames app
from django.shortcuts import redirect, render
from .models import Product, CartItem

def cart_add(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')