from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.apps import apps


class GameManager(models.Manager):
    def active(self):
        return self.filter(available=True, active=True)


@python_2_unicode_compatible
class Game(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    title = models.CharField(max_length=128)
    available = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    is_app = models.BooleanField()
    author = models.CharField(max_length=60, blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    objects = GameManager()
    engine_app = apps.get_app_config('engine')

    def __str__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})

    @property
    def author2(self):
        game = self.engine_app.games[self.id]
        return getattr(game, 'author', None)

    @property
    def description(self):
        game = self.engine_app.games[self.id]
        return getattr(game, 'description', None)


@python_2_unicode_compatible
class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    game = models.ForeignKey(Game)

    first_played = models.DateTimeField(auto_now_add=True)
    last_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s [%s]" % (self.user, self.game)

    def touch(self, commit=True):
        self.last_played = timezone.now()
        if commit:
            self.save()


@python_2_unicode_compatible
class PlayerScore(models.Model):
    player = models.ForeignKey(Player)
    score = models.FloatField(help_text=_(u"Work as 'points'. Based on this the engine will compute rankings"))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s" % self.player

