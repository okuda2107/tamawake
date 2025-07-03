# ballとbarが依存している
from __future__ import annotations

import math
from enum import Enum
from typing import TYPE_CHECKING

import numpy as np

from actor import Actor
from circle_component import CircleComponent
from collision import Sphere, intersect
from gravity_component import GravityComponent

if TYPE_CHECKING:
    from game import Game


class Kind(Enum):
    null = 0
    red = 1
    white = 2


class Ball(Actor):
    def __init__(self, game: Game, radius: float):
        super().__init__(game)
        self.radius: float = radius  # 縦方向の長さ
        self.cc = CircleComponent(self)
        sphere = Sphere()
        sphere.center = self.position
        sphere.radius = radius
        self.cc.set_sphere(sphere)
        self.red_white: Enum = Kind.null
        GravityComponent(self)
        self.velocity = 0.0

    def __del__(self):
        super().__del__()

    def update_actor(self, delta_time: float) -> None:
        # contact_actors = self.game.physics.isCollision(self.sprite)
        # for actor in contact_actors:
        #     actor_pos = np.array([actor.center.x / self.game.screen_size[0], actor.center.y / self.game.screen_size[1]])
        #     normal /= np.linalg.norm(self.position - actor_pos)
        #     normal_vel = np.dot(normal, self.velocity)
        #     self.velocity -= 1.5 * normal_vel * normal
        bar = self.game.physics.lines[0].get_world_line()
        if intersect(bar, self.cc.circle):
            normal: np.ndarray = None
            outT: float
            # ベクトルを準備する
            ab = bar.end_pos - bar.start_pos
            ba = -1.0 * ab
            ac = self.position - bar.start_pos
            bc = self.position - bar.end_pos
            if np.dot(ab, ac) < 0:  # c が a の前に突き出している
                normal = ac
                outT = 0
            elif np.dot(ba, bc) < 0:  # c が b の前に突き出している
                normal = bc
                outT = 1
            else:  # c を線分に射影する
                scalar = float(np.dot(ab, ac)) / float(np.sum(ab**2))
                p = scalar * ab
                normal = ac - p
                x = bar.start_pos - self.position
                y = ab
                a = float(np.sum(y**2))
                b = float(2 * np.dot(x, y))
                c = float(np.sum(x**2) - self.radius**2)
                # 判別式
                disc = math.sqrt(float(b**2) - 4.0 * a * c)
                # 方程式の公式を使ってtの解を求める
                t_min = (-b - disc) / (2.0 * a)
                t_max = (-b + disc) / (2.0 * a)
                outT = (t_max + t_min) / 2
                if outT < 0:
                    outT = 0
                elif outT > 1:
                    outT = 1

            normal_vel = np.dot(normal, self.velocity) / np.sum(normal**2) * normal
            self.position = (
                bar.point_on_segument(outT)
                + normal / np.linalg.norm(normal) * self.radius
            )
            # 反発係数 1.3
            self.velocity -= 1.3 * normal_vel
