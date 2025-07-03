from __future__ import annotations

import math
from typing import Union, overload

import numpy as np


class LineSegment:
    start_pos = np.array([0.0, 0.0])
    end_pos = np.array([0.0, 0.0])

    def __init__(self, start: np.array, end: np.array):
        self.start_pos = np.array(start)
        self.end_pos = np.array(end)

    def point_on_segument(self, t: float) -> np.array:
        return self.start_pos + (self.end_pos - self.start_pos) * t

    def min_dist_sq(self, point: np.array) -> float:
        # ベクトルを準備する
        ab = self.end_pos - self.start_pos
        ba = -1.0 * ab
        ac = point - self.start_pos
        bc = point - self.end_pos

        if np.dot(ab, ac) < 0:  # c が a の前に突き出している
            return float(np.sum(ac**2))
        elif np.dot(ba, bc) < 0:  # c が b の前に突き出している
            return float(np.sum(bc**2))
        else:  # c を線分に射影する
            scalar = float(np.dot(ab, ac)) / float(np.sum(ab**2))
            p = scalar * ab
            return float(np.sum((ac - p) ** 2))


class Sphere:
    """pixel数を入力する"""

    center = np.array([0.0, 0.0])
    radius: float = 0.0


class AABB:
    min_pos = np.array([0.0, 0.0])
    max_pos = np.array([0.0, 0.0])

    def __init__(self, size: np.array):
        self.min_pos = -size / 2
        self.max_pos = size / 2

    def update_min_max(self, point: np.array) -> None:
        self.min_pos[0] = min(self.min_pos[0], point[0])
        self.min_pos[1] = min(self.min_pos[1], point[1])
        self.max_pos[0] = max(self.max_pos[0], point[0])
        self.max_pos[1] = max(self.max_pos[1], point[1])

    def contains(self, point: np.array) -> bool:
        outside: bool = (
            point[0] < self.min_pos[0]
            or point[1] < self.min_pos[1]
            or point[0] > self.max_pos[0]
            or point[1] > self.max_pos[1]
        )
        return not outside

    def min_dist_sq(self, point: np.array) -> float:
        dx: float = max(self.min_pos[0] - point[0], 0)
        dx = max(dx, point[0] - self.max_pos[0])
        dy: float = max(self.min_pos[1] - point[1], 0)
        dy = max(dy, point[1] - self.max_pos[1])
        return dx**2 + dy**2


@overload
def intersect(l: LineSegment, s: Sphere) -> bool:
    pass


@overload
def intersect(a: AABB, b: AABB) -> bool:
    pass


@overload
def intersect(s: Sphere, box: AABB) -> bool:
    pass


@overload
def intersect(a: Sphere, b: Sphere) -> bool:
    pass


def __line_intersect(l: LineSegment, s: Sphere) -> bool:
    # 線分と球の交点を見つけるには直線から球の中心までの距離が，球の半径と等しくなるようなtの値を計算する
    # 方程式を解く
    x = l.start_pos - s.center
    y = l.end_pos - l.start_pos
    a = float(np.sum(y**2))
    b = float(2 * np.dot(x, y))
    c = float(np.sum(x**2) - s.radius**2)
    # 判別式
    disc = b**2 - 4.0 * a * c
    if disc < 0.0:
        return False
    else:
        disc = math.sqrt(disc)
        # 方程式の公式を使ってtの解を求める
        t_min = (-b - disc) / (2.0 * a)
        t_max = (-b + disc) / (2.0 * a)
        if t_min > 1.0 or t_max < 0.0:
            return False
        else:
            return True


def intersect(a: Union[LineSegment, AABB, Sphere], b: Union[AABB, Sphere]) -> bool:
    """図形の交差判定"""
    if isinstance(a, LineSegment) and isinstance(b, Sphere):
        return __line_intersect(a, b)

    if isinstance(a, AABB) and isinstance(b, AABB):
        no = (
            a.max_pos[0] < b.min_pos[0]
            or a.max_pos[1] < b.min_pos[1]
            or b.max_pos[0] < a.min_pos[0]
            or b.max_pos[1] < a.min_pos[1]
        )
        return not no

    if isinstance(a, Sphere) and isinstance(b, AABB):
        distSq = b.min_dist_sq(a.center)
        return distSq <= (a.radius**2)

    if isinstance(a, Sphere) and isinstance(b, Sphere):
        dist_sq = np.linalg.norm((a.center - b.center))
        sum_radii = a.radius + b.radius
        return dist_sq <= sum_radii

    return False
