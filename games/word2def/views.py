
from django.conf import settings

from engine.utils.views import QuestionView

from .models import Question, Definition

ACCESS_TOKEN_IO = getattr(settings, 'ACCESS_TOKEN_IO')
ACCESS_TOKEN_STORE = getattr(settings, 'ACCESS_TOKEN_STORE')


class Word2DefQuestionView(QuestionView):
    template_name = 'word2def/game_play.html'

    def get_object(self, pk=None):
        return super(Word2DefQuestionView, self).get_object(pk='word2def')

    def score(self, response, user_answer):
        score = super(Word2DefQuestionView, self).score(response, user_answer)

        # Store data associated to 'response' and 'user_answer'

        return score
