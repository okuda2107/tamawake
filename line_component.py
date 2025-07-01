from __future__ import annotations

import copy
import math

import numpy as np

from actor import Actor
from collision import LineSegment
from component import Component


class LineComponent(Component):
    def __init__(self, owner: Actor):
        super().__init__(owner)
        self._owner.game.physics.add_line(self)
        self.__object_line: LineSegment = None
        self.__world_line: LineSegment = None

    def __del__(self):
        self._owner.game.physics.remove_line(self)
        super().__del__()

    def update(self, delta_time: float):
        self.update_world_line()

    def set_object_line(self, model: LineSegment):
        self.__object_line = model
        self.__world_line = copy.deepcopy(model)
        self.update_world_line()

    def update_world_line(self):
        rot_mat = np.array(
            [
                [math.cos(self.rotation), -math.sin(self.rotation)],
                [math.sin(self.rotation), math.cos(self.rotation)],
            ]
        )
        self.__world_line.start_pos = (
            rot_mat @ self.__object_line.start_pos + self._owner.position
        )
        self.__world_line.end_pos = (
            rot_mat @ self.__object_line.end_pos + self._owner.position
        )

    def get_world_box(self):
        return self.__world_line
