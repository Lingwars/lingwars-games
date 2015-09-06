from __future__ import division

from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, RedirectView, TemplateView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Sum, Count, F, FloatField

from engine.models import Game, PlayerScore, Player


class GameMixinView(SingleObjectMixin):
    #model = Game
    queryset = Game.objects.active()

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super(GameMixinView, self).get_object(queryset)
        return self._object

    def get_app_label(self):
        return self.get_object().name.split('.')[-1]


class GameDetailView(GameMixinView, DetailView):

    def get_template_names(self):
        names = super(GameDetailView, self).get_template_names()
        return ['%s/game_detail.html' % self.get_app_label()] + names


class GameRankingView(GameMixinView, DetailView):
    template_name = 'engine/game_ranking.html'


class GamePlayRedirectView(GameMixinView, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # Redirect to play URL inside app
        app_label = self.get_app_label()
        return reverse('%s:play' % app_label)


class UserRankingView(TemplateView):
    queryset = Game.objects.active()
    template_name = 'engine/user_ranking.html'

    def get_context_data(self, **kwargs):
        now = timezone.now()
        now = now.replace(hour=0, minute=0, second=0)
        data = []
        for game in self.queryset:
            players = Player.objects.filter(game=game).annotate(sum=Sum('playerscore__score'), count=Count('playerscore')).annotate(score=F('sum')/F('count'))
            data.append((game, players))

        context = super(UserRankingView, self).get_context_data(**kwargs)
        context.update({'data': data})
        return context
