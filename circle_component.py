from __future__ import annotations

from typing import TYPE_CHECKING

from component import Component

if TYPE_CHECKING:
    from actor import Actor
    from collision import Sphere


class CircleComponent(Component):
    def __init__(self, owner: Actor):
        super().__init__(owner)
        self.circle: Sphere = None
        self._owner.game.physics.add_circle(self)

    def __del__(self):
        super().__del__()
        self._owner.game.physics.remove_circle(self)

    def update(self, delta_time: float):
        self.circle.center = self._owner.position

    def set_sphere(self, model: Sphere):
        self.circle = model

    def get_owner(self):
        return self._owner
