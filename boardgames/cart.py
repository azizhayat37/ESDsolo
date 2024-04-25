from django.shortcuts import redirect
from .models import BoardGame, CartItem, Order
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User # to be used in pseudo order generator

# Here I'm going to create all the logic necessary to interact with carts and orders on the ecommerce site
# As we are not simulating the presence of inventory, we'll just assuming everything is infinitely available for purchase
'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
'''
def add_to_cart(request, bgg_id, quantity):
    if not request.user.is_authenticated:
        # warning flash and redirect so the user can log in
        messages.warning(request, 'Remember to log in before shopping!')
        return redirect('login_view')
    # bgg_id is the boardgame's id from boardgamegeek.com, the source of the Kaggle data
    boardgame = get_object_or_404(BoardGame, bgg_id=bgg_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, 
        boardgame=boardgame
    )
    print(cart_item)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        
    return redirect('cart_view')

def return_user_cart(request):
    # get the user's cart
    user_cart = CartItem.objects.filter(user=request.user.id)
    return user_cart

''' 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    date_ordered = models.DateTimeField(default=timezone.now)  
'''

def checkout(request):
    #if cart is empty, redirect to index
    if not return_user_cart(request):
        messages.warning(request, 'There\'s nothing in your cart!')
        return redirect('index')
    # create logic to pass cart items to create order then wipe the cart
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to log in to shop with us!')
        return redirect('login_view')
    new_order = Order(
        user=request.user,
        #items=return_user_cart(request),
        date_ordered=timezone.now()
        )
    #save to db
    new_order.save()
    # I don't know why this part works, but it does (from stack overflow)
    cart_items = return_user_cart(request)
    for item in cart_items:
            new_order.items.add(item)
    # flash a thank you message
    messages.success(request, 'Thank you for your order!')
    #clear the user's cart
    CartItem.objects.filter(user=request.user).delete()
    #back to do more shopping
    return redirect('display')


###### ALTERNATE VERSION TO BE USED AS DJANGO ADMIN COMMANDS FOR TESTING PURPOSES ######

# Instead of relying ona request, we're passing user id directly into it

def add_to_cart_command(user_id, bgg_id, quantity):
    user_instance = User.objects.get(pk=user_id)
    # bgg_id is the boardgame's id from boardgamegeek.com, the source of the Kaggle data
    boardgame = BoardGame.objects.get(bgg_id=bgg_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=user_instance, 
        boardgame=boardgame
    )
    print(cart_item)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        
    return

def checkout_command(user_id):
    user_instance = User.objects.get(pk=user_id)
    #if cart is empty, redirect to index
    if not CartItem.objects.filter(user=user_id):
        print('There\'s nothing in your cart!')
        return
    # create logic to pass cart items to create order then wipe the cart
    new_order = Order(
        user=user_instance,
        #items=return_user_cart(request),
        date_ordered=timezone.now()
        )
    #save to db
    new_order.save()
    # I don't know why this part works, but it does (from stack overflow)
    cart_items = CartItem.objects.filter(user=user_id)
    for item in cart_items:
            new_order.items.add(item)
    # flash a thank you message
    print('Thank you for your order!')
    #clear the user's cart
    CartItem.objects.filter(user=user_id).delete()
    #back to do more shopping
    return