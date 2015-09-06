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


from django.db.models.aggregates import Aggregate, Value
class CountAsFloat(Aggregate):
    function = 'COUNT'
    name = 'Count'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        if expression == '*':
            expression = Value(expression)
        super(CountAsFloat, self).__init__(
            expression, distinct='DISTINCT ' if distinct else '', output_field=FloatField(), **extra)

    def __repr__(self):
        return "{}({}, distinct={})".format(
            self.__class__.__name__,
            self.arg_joiner.join(str(arg) for arg in self.source_expressions),
            'False' if self.extra['distinct'] == '' else 'True',
        )

    def convert_value(self, value, expression, connection, context):
        if value is None:
            return 0
        return int(value)


class UserRankingView(TemplateView):
    queryset = Game.objects.active()
    template_name = 'engine/user_ranking.html'

    def get_context_data(self, **kwargs):
        now = timezone.now()
        now = now.replace(hour=0, minute=0, second=0)
        data = []
        for game in self.queryset:
            players = Player.objects.filter(game=game).annotate(sum=Sum('playerscore__score'), count=CountAsFloat('playerscore')).annotate(score=F('sum')/F('count')).order_by('-score')
            data.append((game, players))

        context = super(UserRankingView, self).get_context_data(**kwargs)
        context.update({'data': data})
        return context
