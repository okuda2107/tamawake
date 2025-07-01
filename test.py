from __future__ import annotations

from typing import TYPE_CHECKING

from actor import Actor
from bar import bar

if TYPE_CHECKING:
    from game import Game


class Test(Actor):
    def __init__(self, game: Game):
        super().__init__(game)
        bar(game)
