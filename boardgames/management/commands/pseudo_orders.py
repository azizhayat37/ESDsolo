from pathlib import Path
from django.core.management.base import BaseCommand
import random
from django.core.exceptions import ObjectDoesNotExist
from boardgames.models import BoardGame, CartItem, Order
from boardgames.cart import add_to_cart_command, checkout_command

class Command(BaseCommand):

    def handle(self, *args, **options):
        help = "Pseudo-order generator"

        # Generate 100 pseudo orders, some including multiples of the same item in a single cart
        # Orders will be randomly distributed among our 4 personas (there may be errors if you run this after wiping the database)
        for i in range(1,100):
            cart_count = random.randint(1, 5)
            user_id = random.randint(1, 4) #azizhayat, bill, mike, or steve -- our 4 personas


            # add items to cart and proceed to checkout
            for i in range(cart_count):
                bgg_id = random.randint(1, 10)
                quantity = random.randint(1, 5) #occasionally more than one similar item
                try:
                    add_to_cart_command(user_id, bgg_id, quantity)
                    checkout_command(user_id)
                except ObjectDoesNotExist:
                    print("User does not exist")
                    continue

