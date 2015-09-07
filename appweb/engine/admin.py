from django.contrib import admin

from engine.models import Game, Player, PlayerScore


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'available', 'active', 'is_app',)
    readonly_fields = ('id', 'available', 'is_app',)
    list_filter = ('available', 'active', 'is_app',)
    search_fields = ('title',)

class PlayerScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'score',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'game',)
    list_filter = ('game', 'first_played', 'last_played',)

admin.site.register(Game, GameAdmin)
admin.site.register(PlayerScore, PlayerScoreAdmin)
admin.site.register(Player, PlayerAdmin)
