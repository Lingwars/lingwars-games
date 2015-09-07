

from django.conf import settings
from engine.utils.apps import GameConfig
from .game import Game

import logging
log = logging.getLogger(__name__)

ACCESS_TOKEN_IO = getattr(settings, 'ACCESS_TOKEN_IO')
ACCESS_TOKEN_STORE = getattr(settings, 'ACCESS_TOKEN_STORE')


class Word2DefConfig(GameConfig):
    name = 'games.word2def'
    verbose_name = u"Word 2 Definition"
    game = Game(ACCESS_TOKEN_IO, ACCESS_TOKEN_STORE)

    def get_game(self):
        return self.game

