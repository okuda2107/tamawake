from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from actor import Actor
from collision import LineSegment
from line_component import LineComponent
from sprite_component import SpriteComponent

if TYPE_CHECKING:
    from game import Game


class Bar(Actor):
    def __init__(self, game: Game):
        super().__init__(game)
        length: float = 0.8
        thin = 0.04
        self.position = np.array([0.5, 0.65])
        sc = SpriteComponent(self)
        sc.set_image(
            "asset/bar.png",
            (length * self.game.screen_size[0], thin * self.game.screen_size[0]),
        )
        lc = LineComponent(self)
        lc.set_object_line(LineSegment([-length / 2, 0.0], [length / 2, 0.0]))

    def __del__(self):
        super().__del__()

    def actor_input(self) -> None:
        result = self.game.mediapipe.detect_pose()
        if result is not None:
            self.rotation = self.rotation = (
                (
                    result.pose_landmarks.landmark[16].y
                    - result.pose_landmarks.landmark[15].y
                )
                * self.game.screen_size[1]
            ) / (
                (
                    result.pose_landmarks.landmark[15].x
                    - result.pose_landmarks.landmark[16].x
                )
                * self.game.screen_size[0]
            )
