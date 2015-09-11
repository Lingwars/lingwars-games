#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import uuid
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.apps import apps
from django.views.generic.detail import SingleObjectMixin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from ..models import Player, PlayerScore, Game


engine_app = apps.get_app_config('engine')


class GameMixinView(SingleObjectMixin):
    queryset = Game.objects.active()

    def get_object(self, pk=None):
        pk = pk or self.kwargs[self.pk_url_kwarg]
        if not hasattr(self, '_object'):
            self._object = self.queryset.get(pk=pk)
        return self._object

    @property
    def game(self):
        return engine_app.games[self.object.id]

    def get_context_data(self, *args, **kwargs):
        context = super(GameMixinView, self).get_context_data(*args, **kwargs)
        context.update({'description': getattr(self.game, 'description', None)})
        return context


class QuestionView(GameMixinView, TemplateView):
    template_name = 'engine/game_play.html'

    @property
    def uuid(self):
        if not hasattr(self, '_uuid'):
            if not 'uuid' in self.kwargs:
                self._uuid = str(uuid.uuid4())
            else:
                self._uuid = self.kwargs['uuid']
        return self._uuid

    def get_answer_template(self, question):
        if 'options' in question:
            return 'engine/_answer_options.html'
        elif 'yesno' in question:
            return 'engine/_answer_yesno.html'
        else:
            return None

    def get_context_data(self, *args, **kwargs):
        question, response = self.make_question()
        question.update({'answer_template': self.get_answer_template(question)})
        self.request.session[self.uuid] = {'question': question, 'response': response}

        context = super(QuestionView, self).get_context_data(*args, **kwargs)
        context.update({'question': question, 'id': self.uuid,})

        answer_url = reverse('game_answer', kwargs={'pk': self.object.pk, 'uuid': self.uuid})
        context.update({'answer_url': answer_url})

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(QuestionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.session.get(self.uuid, False):
            messages.add_message(request, messages.ERROR, u"Invalid answer identifier")
            return self.get(request, *args, **kwargs)

        data = request.session[self.uuid]
        question = data['question']
        response = data['response']
        score = self.score(question, response, request.POST)

        if request.user and request.user.is_authenticated():
            player, created = Player.objects.get_or_create(user=request.user, game=self.object)
            PlayerScore.objects.create(player=player, score=score)
            player.touch()

        redirect_url = reverse('game_play', kwargs={'pk': self.object.pk})
        return redirect(redirect_url)

    def get_question_kwargs(self):
        return {}

    def make_question(self):
        return self.game.make_question(**self.get_question_kwargs())

    def score(self, question, response, user_answer, show_message=True):
        score = self.game.score(response, user_answer)

        if show_message:
            if score > 0:
                icon = 'glyphicon-thumbs-up'
                message_level = messages.SUCCESS
                sr_message = _('Well done')
            else:
                icon = 'glyphicon-thumbs-down'
                message_level = messages.ERROR
                sr_message = _('Error')

            msg = mark_safe('<span class="glyphicon %s" aria-hidden="true"></span> '
                            '<span class="sr-only">%s:</span> '
                            '%s' % (icon, sr_message, response.get('info', None)))
            messages.add_message(self.request, message_level, msg)

        return score