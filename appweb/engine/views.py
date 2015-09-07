from __future__ import division
from __future__ import absolute_import

from django.views.generic import DetailView, TemplateView
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Sum, F, FloatField
from django.shortcuts import redirect


from .models import Game, Player
from .utils.views import QuestionView, GameMixinView


class GameDetailView(GameMixinView, DetailView):

    def get_template_names(self):
        names = super(GameDetailView, self).get_template_names()
        return ['%s/game_detail.html' % self.object.id] + names


class GameRankingView(GameMixinView, DetailView):
    template_name = 'engine/game_ranking.html'

    def get_context_data(self, **kwargs):
        context = super(GameRankingView, self).get_context_data(**kwargs)

        now = timezone.now().replace(hour=0, minute=0, second=0)
        players = Player.objects.filter(game=self.object.pk).annotate(sum=Sum('playerscore__score'), count=CountAsFloat('playerscore')).annotate(score=F('sum')/F('count')).order_by('-score')
        context.update({'players': players})
        return context


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
        now = timezone.now().replace(hour=0, minute=0, second=0)
        data = []
        for game in self.queryset:
            players = Player.objects.filter(game=game).annotate(sum=Sum('playerscore__score'), count=CountAsFloat('playerscore')).annotate(score=F('sum')/F('count')).order_by('-score')
            data.append((game, players))

        context = super(UserRankingView, self).get_context_data(**kwargs)
        context.update({'data': data})
        return context


class GamePlayView(QuestionView):
    template_name = 'engine/game_play.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_app:
            # Redirect to play URL inside app
            return redirect(reverse('%s:play' % self.object.id))
        else:
            return super(GamePlayView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        answer_url = reverse('game_answer', kwargs={'pk': self.object.pk, 'uuid': self.uuid})
        return super(GamePlayView, self).get_context_data(answer_url=answer_url, game=self.object)
