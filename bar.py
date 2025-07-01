from __future__ import annotations
import numpy as np
from game import *
from actor import *
from sprite_component import *

class bar(Actor):
    def __init__(self, game: Game):
        super().__init__(game)
        self.length: float = 0.8
        self.position = np.array([0.5, 0.65])
        sc = SpriteComponent(self)
        sc.set_image("asset/bar.png", (0.8 * self.game.screen_size[0], 0.04 * self.game.screen_size[0]))

    def __del__(self):
        super().__del__()

    def actor_input(self) -> None:
        result = self.game.mediapipe.detect_pose()
        if result != None:
            self.rotation = math.atan2((result.pose_landmarks.landmark[16].y - result.pose_landmarks.landmark[15].y) * self.game.screen_size[1], (result.pose_landmarks.landmark[15].x - result.pose_landmarks.landmark[16].x) * self.game.screen_size[0])
