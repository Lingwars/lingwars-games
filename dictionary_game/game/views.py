from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

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
    request.session['question'] = question

    # Store data
    #Definition.objects.bulk_create([Definition(word=w[0], definition=w[1]) for w in words])
    for w in words:
        Definition.objects.get_or_create(word=w[0], defaults={'definition': w[1], 'level': level})

    return render(request, 'game/question.html', context={'question': question, 'level': level})


def answer(request, answer):
    if not request.session.get('question', False):
        messages.add_message(request, messages.INFO, 'Let\'s play')
        return redirect('play_level', level=0)

    answer_id = int(answer)-1
    level = request.session['level']
    question = request.session['question']
    options = [opt[0] for opt in question['options']]
    answer_def = Definition.objects.get(word = options[answer_id])
    if question['answer'] == answer_id:
        messages.add_message(request, messages.SUCCESS, 'Well done!')
    else:
        messages.add_message(request, messages.ERROR, 'Ooohhh! You failed')
    messages.add_message(request, messages.INFO, u"%s: %s" % (answer_def.word, answer_def.definition))

    # Store question
    question_def = Definition.objects.get(word = question['word'])
    instance = Question(query=question_def, answer=answer_def, level=level)
    instance.options = Definition.objects.filter(word__in=options)
    if request.user.is_authenticated():
        instance.user = request.user
    instance.save()

    return redirect('play_level', level=level)
