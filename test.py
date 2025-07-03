from __future__ import annotations

from typing import TYPE_CHECKING

from actor import Actor
from ball import Ball
from bar import Bar

if TYPE_CHECKING:
    from game import Game


class Test(Actor):
    def __init__(self, game: Game):
        super().__init__(game)
        Bar(self.game)
        ball = Ball(self.game, 0.1)
        ball.position = [0.5, 0.5]
