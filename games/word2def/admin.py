from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import F

from .models import Definition, Question

class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('word', 'level',)
    list_filter = ('level',)
    search_fields = ('word__word',)

class QuestionCorrectFilter(admin.SimpleListFilter):
    title = _('correct')
    parameter_name = 'correct'

    def lookups(self, request, model_admin):
        return (
            (1, _('Yes')),
            (0, _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            print("CORRECT")
            return queryset.filter(query=F('answer'))
        elif self.value() == '0':
            print("FAIL")
            return queryset.exclude(query=F('answer'))
        print("ALL")
        return queryset


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'level', 'correct',)
    list_filter = ('level', QuestionCorrectFilter,)
    search_fields = ('query__word',)

admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Question, QuestionAdmin)