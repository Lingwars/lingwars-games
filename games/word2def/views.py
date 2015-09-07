
from django.conf import settings

from engine.utils.views import QuestionView

from .models import Question, Definition

ACCESS_TOKEN_IO = getattr(settings, 'ACCESS_TOKEN_IO')
ACCESS_TOKEN_STORE = getattr(settings, 'ACCESS_TOKEN_STORE')


class Word2DefQuestionView(QuestionView):
    template_name = 'word2def/game_play.html'

    def get_object(self, pk=None):
        return super(Word2DefQuestionView, self).get_object(pk='word2def')

    def score(self, question, response, user_answer):
        score = super(Word2DefQuestionView, self).score(question, response, user_answer)

        # Store data associated to 'response' and 'user_answer'
        def_options = []
        for opt in question['options']:
            instance, created = Definition.objects.get_or_create(word=opt[0], defaults={'definition': opt[1], 'level': question['level']})
            def_options.append(instance)

        r = response.get('answer')
        u = user_answer.get('answer', None)
        query = Definition.objects.get(word=question['options'][r][0])
        answer = Definition.objects.get(word=question['options'][int(u)][0])

        user = self.request.user if self.request.user and self.request.user.is_authenticated else None
        instance = Question(user=user, query=query, answer=answer, level=question['level'])
        instance.options = def_options
        instance.save(force_insert=True)

        return score
