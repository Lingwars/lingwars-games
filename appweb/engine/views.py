from __future__ import division
from __future__ import absolute_import

from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, RedirectView, TemplateView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Sum, Count, F, FloatField
from django.shortcuts import redirect
from django.utils.module_loading import import_string

from .models import Game, PlayerScore, Player
from .utils.views import QuestionView


class GameMixinView(object):
    @property
    def app(self):
        if not hasattr(self, '_app'):
            self._app = Game.objects.active().get(pk=self.kwargs['game_pk'])
        return self._app

    @property
    def game(self):
        if not hasattr(self, '_game'):
            module = self.app.name
            GameClass = import_string(module)
            self._game = GameClass()
        return self._game

    def get_app_label(self):
        return self.app.get_namespace()


class GameDetailView(GameMixinView, DetailView):

    def get_object(self, queryset=None):
        return self.app

    def get_template_names(self):
        names = super(GameDetailView, self).get_template_names()
        return ['%s/game_detail.html' % self.get_app_label()] + names


class GameRankingView(GameMixinView, DetailView):
    template_name = 'engine/game_ranking.html'

    def get_object(self, queryset=None):
        return self.app


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



class GamePlayView(GameMixinView, QuestionView):
    template_name = 'engine/game_play.html'

    def get(self, request, *args, **kwargs):
        if self.app.is_app:
            # Redirect to play URL inside app
            app_label = self.get_app_label()
            return redirect(reverse('%s:play' % app_label))
        else:
            return super(GamePlayView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        answer_url = reverse('game_answer', kwargs={'game_pk': self.app.pk, 'uuid': self.uuid})
        return super(GamePlayView, self).get_context_data(answer_url=answer_url, game=self.app)
