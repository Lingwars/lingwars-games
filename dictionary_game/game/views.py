
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.core.urlresolvers import reverse

from .utils import Game
from .models import Question, Definition

ACCESS_TOKEN_IO = getattr(settings, 'ACCESS_TOKEN_IO')
ACCESS_TOKEN_STORE = getattr(settings, 'ACCESS_TOKEN_STORE')


def question(request, level):
    level = int(level)
    game = Game(ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE)
    if settings.DEBUG and Definition.objects.filter(level=level).count()>100:
        words = Definition.objects.order_by('?').values_list('word', 'definition')
    else:
        words = game.lookup_words(level, n=4)
    question = game.random_question(words, n_options=4)
    # Save to session
    request.session['level'] = level
    unique = str(uuid.uuid4())
    request.session[unique] = question

    # Store data
    #Definition.objects.bulk_create([Definition(word=w[0], definition=w[1]) for w in words])
    for w in words:
        Definition.objects.get_or_create(word=w[0], defaults={'definition': w[1], 'level': level})

    context = {'question': question, 'level': level, 'id': unique}

    if request.is_ajax():
        return JsonResponse(context)

    return render(request, 'game/question.html', context=context)


def answer(request, uuid, answer):
    if not request.session.get(uuid, False):
        messages.add_message(request, messages.ERROR, 'There has been a problem with the previous question :/')
        return redirect('play_level', level=0)

    data = request.session[uuid]
    del request.session[uuid]
    level = request.session['level']
    answer_id = int(answer)

    options = [opt[0] for opt in data['options']]
    answer_def = Definition.objects.get(word = options[answer_id])

    if data['answer'] == answer_id:
        data.update({'result': 1})
        messages.add_message(request, messages.SUCCESS, 'Well done!')
    else:
        data.update({'result': 0})
        messages.add_message(request, messages.ERROR, 'Ooohhh! You failed')
    messages.add_message(request, messages.INFO, u"%s: %s" % (answer_def.word, answer_def.definition))

    # Store question
    question_def = Definition.objects.get(word = data['word'])
    instance = Question(query=question_def, answer=answer_def, level=level)
    instance.options = Definition.objects.filter(word__in=options)
    if request.user.is_authenticated():
        instance.user = request.user
    instance.save()

    redirect_url = reverse('play_level', kwargs={'level': level})

    if request.is_ajax():
        return JsonResponse(data.update({'redirect_to': redirect_url}))

    return redirect(redirect_url)
