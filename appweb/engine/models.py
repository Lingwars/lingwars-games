from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class GameManager(models.Manager):
    def active(self):
        return self.filter(active=True)


@python_2_unicode_compatible
class Game(models.Model):
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    available = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    date_added = models.DateTimeField(auto_now_add=True)

    objects = GameManager()

    def __str__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    game = models.ForeignKey(Game)

    first_played = models.DateTimeField(auto_now_add=True)
    last_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s" % self.title

    def touch(self, commit=True):
        self.last_played = timezone.now()
        if commit:
            self.save()


@python_2_unicode_compatible
class PlayerScore(models.Model):
    player = models.ForeignKey(Player)
    score = models.PositiveIntegerField(help_text=_(u"Work as 'points'. Based on this the engine will compute rankings"))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        super(PlayerScore, self).save(*args, **kwargs)
        self.player.touch()
