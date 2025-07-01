from __future__ import annotations
from component import Component
from collision import LineSegment
from actor import Actor
import copy

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

    def set_object_box(self, model: LineSegment):
        self.__object_line = model
        self.__world_line = copy.deepcopy(model)
        self.update_world_line()

    def update_world_line(self):
        self.__world_line.start_pos = 0
        self.__world_line.end_pos = 0
        self.__world_box.min_pos = self.__object_box.min_pos * self._owner.scale
        self.__world_box.max_pos = self.__object_box.max_pos * self._owner.scale
        self.__world_box.min_pos = self.__object_box.min_pos + self._owner.position
        self.__world_box.max_pos = self.__object_box.max_pos + self._owner.position

    def get_world_box(self):
        return self.__world_line
