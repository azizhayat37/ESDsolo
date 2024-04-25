from django.shortcuts import redirect, render
from .models import BoardGame, CartItem, Order, OrderItem
from django.utils import timezone

# Here I'm going to create all the logic necessary to interact with carts and orders on the ecommerce site
# As we are not simulating the presence of inventory, we'll just assuming everything is infinitely available for purchase
'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
'''
def add_to_cart(request, boardgame_id, quantity):
    # create an object to add to the cart
    cart_item = CartItem(
        user = request.user.id,
        boardgame = boardgame_id,
        quantity = quantity,
        date_added = timezone.now()
    )
    # commit to db
    cart_item.save()
    # go to cart view
    return redirect('cart')

def return_user_cart(request):
    # get the user's cart
    user_cart = CartItem.objects.filter(user=request.user.id)
    return user_cart