from django.shortcuts import redirect, render
from .models import BoardGame, CartItem, Order, OrderItem
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Here I'm going to create all the logic necessary to interact with carts and orders on the ecommerce site
# As we are not simulating the presence of inventory, we'll just assuming everything is infinitely available for purchase
'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
'''
def add_to_cart(request, bgg_id, quantity):
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
    #check if the user already has this boardgame in their cart
    # check if the user already has this boardgame in their cart
    if CartItem.objects.filter(user=request.user, boardgame_id=boardgame_id).exists():
        specific_item = CartItem.objects.get(user=request.user, boardgame_id=boardgame_id)
        specific_item.quantity += 1
        specific_item.save()
    else:
        boardgame = get_object_or_404(BoardGame, pk=boardgame_id)
        # create an object to add to the cart
        cart_item = CartItem(
            user = request.user,
            boardgame = boardgame, #passing in the actual boardgame instance resolved this bug, don't use the ID here (note to self)
            quantity = quantity,
            date_added = timezone.now()
        )
        # commit to db
        cart_item.save()
        # go to cart view
        return redirect('cart_view')
    '''   