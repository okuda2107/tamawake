from __future__ import annotations

import random
from typing import TYPE_CHECKING

import numpy as np

from actor import Actor
from ball import Ball, Kind
from point_manager import PointManager
from sprite_component import SpriteComponent

if TYPE_CHECKING:
    from game import Game
    from playground import Level


class BallGenerator(Actor):
    def __init__(self, game: Game):
        super().__init__(game)
        self.position = np.array([random.random(), 0])
        self.velocity = 0.3
        self.level: Level = None
        # ボールの削除はPointManagerで行うため，生成したボールをlistに追加する必要がある
        self.point_manager: PointManager = None

    def __del__(self):
        super().__del__()

    def update_actor(self, delta_time: float) -> None:
        # generator自体の移動
        self.position += np.array([self.velocity * delta_time, 0])
        if (self.position[0] < 0 and self.velocity < 0) or (
            self.position[0] > 1 and self.velocity > 0
        ):
            self.velocity *= -1

        # ボールの生成
        if random.random() < self.level.probability:
            size: float = self.level.size
            actor = Ball(self.game, size)
            actor.position = self.position
            file = ""
            if random.random() < 0.5:
                actor.red_white = Kind.red
                file = "asset/red.png"
            else:
                actor.red_white = Kind.white
                file = "asset/white.png"
            sc = SpriteComponent(actor)
            temp_radius = actor.radius * self.game.screen_size[0]
            sc.set_image(file, (temp_radius, temp_radius))
            self.point_manager.ball_list.append(actor)
