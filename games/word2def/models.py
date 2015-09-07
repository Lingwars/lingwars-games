from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings


@python_2_unicode_compatible
class Definition(models.Model):
    word = models.CharField(max_length=128, primary_key=True)
    definition = models.TextField()
    level = models.SmallIntegerField()

    def __str__(self):
        return u"%s" % self.word


class QuestionManager(models.Manager):
    def correct(self):
        return self.filter(query=models.F('answer'))

    def fail(self):
        return self.exclude(query=models.F('answer'))

@python_2_unicode_compatible
class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    query = models.ForeignKey(Definition)
    answer = models.ForeignKey(Definition, related_name='+')
    level = models.SmallIntegerField()

    _n_options = models.SmallIntegerField(db_column='n_options')
    _options = models.TextField(db_column='options')

    objects = QuestionManager()

    def __str__(self):
        return u"%s" % self.query

    @property
    def correct(self):
        return self.query == self.answer

    @property
    def options(self):
        opts = self._options.split('|')
        assert len(opts)==self._n_options
        return Definition.objects.filter(word__in=opts)

    @options.setter
    def options(self, value_list):
        self._n_options = len(value_list)
        self._options = '|'.join([it.word for it in value_list])
