from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
# Create your models here.

class Episode(models.Model):
    serie = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(1, "Serie must be greater than 1 characters")]
    )
    episode = models.CharField(
        max_length=3,
        validators=[MinLengthValidator(1, "episode must be greater than 1 characters")]
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       through='Fav', related_name='favorite_episodes')

class Fav(models.Model) :
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    class Meta:
        unique_together = ('episode', 'user')

    def __str__(self):
        return '%s likes %s' % (self.user.username, self.episode.title[:10])