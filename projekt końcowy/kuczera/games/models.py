from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

# Create your models here.
class games(models.Model):
    game_name = models.TextField(validators=[MaxLengthValidator(50)])

    last_update = models.DateTimeField()

    creation_date = models.DateTimeField()

    status = models.SmallIntegerField() # 0-active / 1-insider_access / 2-debug_mode


class score_table(models.Model):
    game = models.ForeignKey(games, on_delete=models.CASCADE)

    player = models.ForeignKey(User, on_delete=models.CASCADE)

    player_score = models.DecimalField(max_digits=5, decimal_places=2)

    score_date = models.DateTimeField()

class events(models.Model):
    game = models.ForeignKey(games, on_delete=models.CASCADE)

    event_date = models.DateTimeField()

    event_description = models.TextField(validators=[MaxLengthValidator(1000)])
