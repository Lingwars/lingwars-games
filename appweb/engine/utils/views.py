#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import uuid
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from ..models import Player, PlayerScore, Game



class GameMixinView(object):
    games_qs = Game.objects.active()

    @property
    def object(self):
        if not hasattr(self, '_object'):
            self._object = self.games_qs.get(pk=self.kwargs['pk'])
        return self._object

    @property
    def app(self):
        return self.object.get_app_config()

    @property
    def game(self):
        return self.object.get_game()


class QuestionView(GameMixinView, TemplateView):

    @property
    def uuid(self):
        if not hasattr(self, '_uuid'):
            if not 'uuid' in self.kwargs:
                print("*"*30)
                self._uuid = str(uuid.uuid4())
            else:
                self._uuid = self.kwargs['uuid']
        return self._uuid

    def get_context_data(self, *args, **kwargs):
        level = 2  # TODO: Allow user to select level
        question, response = self.game.make_question(level=level, n_options=4)
        self.request.session[self.uuid] = {'question': question, 'response': response}

        context = super(QuestionView, self).get_context_data(*args, **kwargs)
        context.update({'question': question, 'level': level, 'id': self.uuid})
        return context

    def post(self, request, *args, **kwargs):
        if not request.session.get(self.uuid, False):
            messages.add_message(request, messages.ERROR, u"Invalid answer identifier")
            return self.get(request, *args, **kwargs)

        data = request.session[self.uuid]
        score = self.score(data['response'], request.POST)

        if request.user and request.user.is_authenticated():
            player, created = Player.objects.get_or_create(user=request.user, game=self.app)
            PlayerScore.objects.create(player=player, score=score)
            player.touch()

        redirect_url = reverse('game_play', kwargs={'game_pk': self.app.pk})
        return redirect(redirect_url)

    def score(self, response, user_answer):
        score = self.game.score(response, user_answer)
        if score > 0:
            messages.add_message(self.request, messages.SUCCESS, 'Well done!')
        else:
            messages.add_message(self.request, messages.SUCCESS, 'Oooohhh! You failed')
        print(response)
        messages.add_message(self.request, messages.INFO, response.get('info', None))
        return score