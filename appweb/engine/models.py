from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse


class GameManager(models.Manager):
    def active(self):
        return self.filter(active=True)


@python_2_unicode_compatible
class Game(models.Model):
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    available = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    objects = GameManager()

    def __str__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})