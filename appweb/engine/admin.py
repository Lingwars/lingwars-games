from django.contrib import admin

from engine.models import Game, Player, PlayerScore


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'available', 'active',)
    readonly_fields = ('name', 'available',)
    list_filter = ('available', 'active',)
    search_fields = ('title',)

class PlayerScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'score',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'game',)
    list_filter = ('game', 'first_played', 'last_played',)

admin.site.register(Game, GameAdmin)
admin.site.register(PlayerScore, PlayerScoreAdmin)
admin.site.register(Player, PlayerAdmin)
