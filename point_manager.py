from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from actor import Actor, state
from ball import Ball, Kind

if TYPE_CHECKING:
    from game import Game
    from playground import Level

# ボールの発生確率が1としたときのポイント
# 実際のポイントは 現時点の発生確率 * POINT_RATE
POINT_RATE = 100


class PointManager(Actor):
    """スコア管理するクラス"""

    def __init__(self, game: Game):
        super().__init__(game)
        self.position = np.array([0, 0])
        self.score: int = 0
        self.level: Level = None
        self.ball_list: list[Ball] = []
        self.game.audio_system.set_sound("asset/error.wav")
        self.game.audio_system.set_sound("asset/pop.wav")
        self.game.audio_system.bgm("asset/get.mp3")

    def __del__(self):
        super().__del__()

    def update_actor(self, delta_time: float) -> None:
        # 得点計算とボールの削除処理
        dead_ball = []
        for ball in self.ball_list:
            if ball.position[0] < 0.5 and ball.position[1] > 1.0:
                if ball.red_white == Kind.red:
                    self.score += int(POINT_RATE * self.level.probability)
                    ball.state = state.dead
                    dead_ball.append(ball)
                    self.game.audio_system.play("asset/pop.wav")
                else:
                    self.score -= int(POINT_RATE * self.level.probability)
                    ball.state = state.dead
                    dead_ball.append(ball)
                    self.game.audio_system.play("asset/error.wav")
            if ball.position[0] > 0.5 and ball.position[1] > 1.0:
                if ball.red_white == Kind.white:
                    self.score += int(POINT_RATE * self.level.probability)
                    ball.state = state.dead
                    dead_ball.append(ball)
                    self.game.audio_system.play("asset/pop.wav")
                else:
                    self.score -= int(POINT_RATE * self.level.probability)
                    ball.state = state.dead
                    dead_ball.append(ball)
                    self.game.audio_system.play("asset/error.wav")
        for ball in dead_ball:
            self.ball_list.remove(ball)
