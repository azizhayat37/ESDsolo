import csv
import os
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError

from boardgames.models import BoardGame

class Command(BaseCommand):
    help = "Load data from CSVs"

    def handle(self, *args, **options):

        # Clear out database in order to avoid redundancy
        BoardGame.objects.all().delete()
        print("Data cleared")
        # Create table again

        # Open CSV and begin to read it
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        print(base_dir)
        with open(str(base_dir) + '/boardgames/data/games.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader) # Skip header, single row
            for row in reader:
                print(row)

                try:
                    data = BoardGame(
                        bgg_id=row[0],
                        name=row[1],
                        description=row[2],
                        year_published=row[3],
                        game_weight=row[4],
                        avg_rating=row[5],
                        bayes_avg_rating=row[6],
                        std_dev=row[7],
                        min_players=row[8],
                        max_players=row[9],
                        com_age_rec=row[10],
                        language_ease=float(row[11]) if row[11].isdigit() else 0.0, # corrects for issues where value is not an integer but '' string
                        best_players=row[13],
                        good_players=row[13],
                        num_owned=row[14],
                        num_want=row[15],
                        num_wish=row[16],
                        num_weight_votes=row[17],
                        mfg_playtime=row[18],
                        com_min_playtime=row[19],
                        com_max_playtime=row[20],
                        mfg_age_rec=row[21],
                        num_user_ratings=row[22],
                        num_comments=row[23],
                        num_alternates=row[24],
                        num_expansions=row[25],
                        num_implementations=row[26],
                        is_reimplementation=row[27],
                        family=row[28],
                        kickstarted=row[29],
                        image_path=row[30],
                        rank_boardgame=row[31],
                        rank_strategygames=row[32],
                        rank_abstracts=row[33],
                        rank_familygames=row[34],
                        rank_thematic=row[35],
                        rank_cgs=row[36],
                        rank_wargames=row[37],
                        rank_partygames=row[38],
                        rank_childrensgames=row[39],
                        cat_thematic=True if row[40] == '1' else False,
                        cat_strategy=True if row[41] == '1' else False,
                        cat_war=True if row[42] == '1' else False,
                        cat_family=True if row[43] == '1' else False,
                        cat_cgs=True if row[44] == '1' else False,
                        cat_abstract=True if row[45] == '1' else False,
                        cat_party=True if row[46] == '1' else False,
                        cat_childrens=True if row[47] == '1' else False
                    )
                    data.save()
                    print("Data has been saved to database!")
                except Exception as e:
                    print(e)
                    print("Data could not be saved to database!")
                        


