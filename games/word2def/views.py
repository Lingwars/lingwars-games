
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.apps import apps

from .game import Game
from .models import Question, Definition

ACCESS_TOKEN_IO = getattr(settings, 'ACCESS_TOKEN_IO')
ACCESS_TOKEN_STORE = getattr(settings, 'ACCESS_TOKEN_STORE')


class QuestionView(TemplateView):
    template_name = 'word2def/game_play.html'
    game = Game(ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE)
    app = apps.get_app_config('word2def')

    def get_context_data(self, *args, **kwargs):
        level = 2  # TODO: Allow user to select level
        question, response = self.game.make_question(level=level, n_options=4)
        unique = str(uuid.uuid4())
        self.request.session[unique] = {'question': question, 'response': response}

        context = super(QuestionView, self).get_context_data(*args, **kwargs)
        context.update({'question': question, 'level': level, 'id': unique})
        return context

    def post(self, request, *args, **kwargs):
        uuid = self.kwargs['uuid']
        if not request.session.get(uuid, False):
            messages.add_message(request, messages.ERROR, u"Invalid answer identifier")
            return self.get(request, *args, **kwargs)

        data = request.session[uuid]
        score = self.game.score(data['response'], request.POST)
        if score > 0:
            messages.add_message(request, messages.SUCCESS, 'Well done!')
        else:
            messages.add_message(request, messages.SUCCESS, 'Oooohhh! You failed')

        query = data['question']['query']
        answer = data['question']['options'][data['response']['answer']][1]
        messages.add_message(request, messages.INFO, u"%s: %s" % (query, answer))

        self.app.score(request.user, score)

        redirect_url = reverse('word2def:play')
        return redirect(redirect_url)
