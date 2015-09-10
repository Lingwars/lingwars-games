
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

from engine.utils.views import QuestionView
from engine.utils.game import QuestionError

from .models import Question, Definition
from .forms import LevelForm

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

    def score(self, question, response, user_answer):
        score = super(Word2DefQuestionView, self).score(question, response, user_answer)

        # Store data associated to 'response' and 'user_answer'
        def_options = Definition.objects.filter(word__in=[it[0] for it in response['options']])

        r = response.get('answer')
        u = user_answer.get('answer', None)
        query = Definition.objects.get(word=response['options'][r][0])
        answer = Definition.objects.get(word=response['options'][int(u)][0])

        user = self.request.user if self.request.user and self.request.user.is_authenticated else None
        instance = Question(user=user, query=query, answer=answer, level=question['level'])
        instance.options = def_options
        instance.save(force_insert=True)

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
