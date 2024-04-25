from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# This is all products you'll find in our inventory (we're not keeping specific counts of an actual inventory)
#I've ommitted items I dont think are necessary what we're doing here
class BoardGame(models.Model):
    bgg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    year_published = models.IntegerField()
    game_weight = models.FloatField()
    avg_rating = models.FloatField()
    bayes_avg_rating = models.FloatField()
    std_dev = models.FloatField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    com_age_rec = models.FloatField(null=True, blank=True)
    language_ease = models.FloatField(null=True, blank=True)
    #best_players = models.CharField(max_length=255) 
    #good_players = models.CharField(max_length=255) 
    #num_owned = models.IntegerField()
    #num_want = models.IntegerField()
    #num_wish = models.IntegerField()
    #num_weight_votes = models.IntegerField()
    #mfg_playtime = models.IntegerField()
    #com_min_playtime = models.IntegerField()
    #com_max_playtime = models.IntegerField()
    #mfg_age_rec = models.IntegerField()
    #num_user_ratings = models.IntegerField()
    #num_comments = models.IntegerField()
    #num_alternates = models.IntegerField()
    #num_expansions = models.IntegerField()
    #num_implementations = models.IntegerField()
    #is_reimplementation = models.BooleanField()
    #family = models.CharField(max_length=255, null=True, blank=True)
    kickstarted = models.BooleanField()
    image_path = models.URLField(max_length=1024)
    rank_boardgame = models.IntegerField()
    rank_strategygames = models.IntegerField()
    rank_abstracts = models.IntegerField()
    rank_familygames = models.IntegerField()
    rank_thematic = models.IntegerField()
    rank_cgs = models.IntegerField()
    rank_wargames = models.IntegerField()
    rank_partygames = models.IntegerField()
    rank_childrensgames = models.IntegerField()
    cat_thematic = models.BooleanField()
    cat_strategy = models.BooleanField()
    cat_war = models.BooleanField()
    cat_family = models.BooleanField()
    cat_cgs = models.BooleanField()
    cat_abstract = models.BooleanField()
    cat_party = models.BooleanField()
    cat_childrens = models.BooleanField()
    price = models.FloatField()

    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.quantity} of {self.boardgame.name}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    date_ordered = models.DateTimeField(default=timezone.now)    
    
    def __str__(self):
        return f'Order for {self.user.username}'
