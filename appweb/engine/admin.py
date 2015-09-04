from django.contrib import admin

from engine.models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'available', 'active',)
    readonly_fields = ('name', 'available',)
    list_filter = ('available', 'active',)
    search_fields = ('title',)

admin.site.register(Game, GameAdmin)
