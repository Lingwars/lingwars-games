#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from engine.utils.views import QuestionView
from engine.utils.game import QuestionError

from .models import Question, Definition, SavedWord
from .forms import LevelForm

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import logging
log = logging.getLogger(__name__)

ACCESS_TOKEN_IO = getattr(settings, 'ACCESS_TOKEN_IO')
ACCESS_TOKEN_STORE = getattr(settings, 'ACCESS_TOKEN_STORE')


class Word2DefQuestionView(QuestionView):
    template_name = 'word2def/game_play.html'

    def dispatch(self, request, *args, **kwargs):
        self.level = int(self.request.session.get('level', 2))  # TODO: Default level
        return super(Word2DefQuestionView, self).dispatch(request, *args, **kwargs)

    def get_object(self, pk=None):
        return super(Word2DefQuestionView, self).get_object(pk='word2def')

    def get_answer_template(self, question):
        return 'word2def/_answer_options.html'

    def make_question(self):
        try:
            question, response = self.game.make_question(level=self.level)

            # Store data associated to 'response' and 'user_answer'
            #defs = [Definition(word=opt[0], definition=opt[1], level=level) for opt in response['options']]
            # Definition.objects.bulk_create(defs)
            for opt in response['options']:
                Definition.objects.get_or_create(word=opt[0], defaults={'definition': opt[1], 'level': self.level})

        except QuestionError as e:
            words = Definition.objects.all().order_by('?').values_list('word', 'definition')[:4]
            word, options, answer = self.game.get_random_question(words, 4)
            question, response = self.game.build_question(word, options, answer, self.level)

        return question, response

    def score(self, question, response, user_answer, show_message=True):
        score = super(Word2DefQuestionView, self).score(question, response, user_answer, show_message=False)

        # Store data associated to 'response' and 'user_answer'
        def_options = Definition.objects.filter(word__in=[it[0] for it in response['options']])

        r = response.get('answer')
        u = user_answer.get('answer', None)
        query = Definition.objects.get(word=response['options'][r][0])
        answer = Definition.objects.get(word=response['options'][int(u)][0])

        user = self.request.user if self.request.user and self.request.user.is_authenticated() else None
        instance = Question(user=user, query=query, answer=answer, level=question['level'])
        instance.options = def_options
        instance.save(force_insert=True)

        # Compound message to show
        if score > 0:
            icon = 'glyphicon-thumbs-up'
            message_level = messages.SUCCESS
            sr_message = _('Well done')
        else:
            icon = 'glyphicon-thumbs-down'
            message_level = messages.ERROR
            sr_message = _('Error')

        msg = mark_safe(u'<span class="glyphicon %s" aria-hidden="true"></span> '
                        u'<span class="sr-only">%s:</span> '
                        u'%s' % (icon, sr_message, response.get('info', None)))

        # Tweet
        max_def_length = 140 - len(query.word) - len("► : \"\"\n -- via @lingwars")
        definition = query.definition if len(query.definition) <= max_def_length else u"%s..." % query.definition[:max_def_length-3]
        tw_text = u"► %s: \"%s\"\n -- via @lingwars" % (query.word.title(), definition)
        tweet = mark_safe(u'<a href="https://twitter.com/intent/tweet?%s" target="_blank">%s</a>' % (urlencode({'text': tw_text.encode('utf-8')}), _("Tweet")))

        opts = [tweet]
        if self.request.user.is_authenticated:
            # Save (only for authenticated users)
            save = mark_safe('<a href="#" id="save-word" word="%s">Save</a>' % query.word )
            opts.append(save)

        msg += mark_safe(' <small>[%s]</small>' % ' | '.join(opts))

        messages.add_message(self.request, message_level, msg)

        return score

    def get_context_data(self, **kwargs):
        context = super(Word2DefQuestionView, self).get_context_data(**kwargs)
        answer_url = reverse('word2def:answer', kwargs={'uuid': self.uuid})
        context.update({'answer_url': answer_url, 'level_form': LevelForm(initial={'level': self.level})})
        return context


class ChangeLevelView(FormView):
    form_class = LevelForm
    success_url = reverse_lazy('word2def:play')

    def form_valid(self, form):
        self.request.session['level'] = int(form.cleaned_data['level'])
        if 'next' in self.request.POST:
            self.success_url = self.request.POST['next']
        return super(ChangeLevelView, self).form_valid(form)


def save_word(request):
    user = request.user or None
    if user.is_authenticated:
        try:
            word = request.POST['word']
            word = Definition.objects.get(word=word)
            try:
                SavedWord.objects.get(word=word, user=user).update(deleted=False)
            except SavedWord.DoesNotExist:
                instance = SavedWord(word=word, user=user)
                instance.save(force_insert=True)
            return HttpResponse(status=201)
        except KeyError:
            log.warn("key 'word' not found in request.POST")
        except Definition.DoesNotExist:
            log.warn("Definition for word '%r' does not exist" % word)
    return HttpResponse(status=400)


class SavedWordList(ListView):
    def get_queryset(self):
        return SavedWord.objects.saved().filter(user=self.request.user)
