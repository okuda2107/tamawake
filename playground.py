from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np

import level_loader
from actor import Actor, state
from ball_generator import BallGenerator
from bar import Bar
from point_manager import PointManager
from text_component import TextComponent

if TYPE_CHECKING:
    from game import Game


# 発生確率
@dataclass
class Level:
    probability: float
    size: float


LEVEL1 = Level(probability=0.05, size=0.2)
LEVEL2 = Level(probability=0.1, size=0.15)
LEVEL3 = Level(probability=0.3, size=0.1)


class PlayGround(Actor):
    """ゲームが遊ばれてるときにオブジェクトの管理をするクラス"""

    def __init__(self, game: Game):
        super().__init__(game)
        self.position = np.array([0, 0])
        self.bar = Bar(self.game)
        self.point_manager: PointManager = PointManager(self.game)
        self.ball_gen: BallGenerator = BallGenerator(self.game)
        self.ball_gen.point_manager = self.point_manager
        self.ball_gen.level = LEVEL1
        self.point_manager.level = LEVEL1
        self.timer: float = 60.0
        self.tc: TextComponent = None

    def __del__(self):
        super().__del__()

    def update_actor(self, delta_time: float) -> None:
        self.timer -= delta_time

        if self.timer > 30:
            self.ball_gen.level = LEVEL1
            self.point_manager.level = LEVEL1
        elif self.timer > 10:
            self.ball_gen.level = LEVEL2
            self.point_manager.level = LEVEL2
        else:
            self.ball_gen.level = LEVEL3
            self.point_manager.level = LEVEL3

        if self.timer <= 0:
            self.game.point = self.point_manager.score
            level_loader.load_level(self.game, "asset/result.json")
            self.bar.state = state.dead
            self.state = state.dead
            self.ball_gen.state = state.dead
            self.point_manager.state = state.dead
            for ball in self.point_manager.ball_list:
                ball.state = state.dead

        if self.tc is not None:
            self.tc.set_text(
                "time:"
                + str(round(self.timer, 1))
                + " score:"
                + str(self.point_manager.score),
                (239, 241, 250),
            )

    def load_properties(self, obj: dict[str, Any]) -> None:
        text_size = obj.get("timerSize")
        if text_size is None:
            text_size = 80
        self.tc = TextComponent(self, "microsoftsansserif", text_size)
        self.tc.set_text("", (239, 241, 250))
