from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from circle_component import CircleComponent
    from game import Game
    from line_component import LineComponent


class PhysWorld:
    def __init__(self, game: Game):
        self.game = game
        self.lines: list[LineComponent] = []
        self.circles: list[list[CircleComponent]] = []

    def add_line(self, line: LineComponent):
        self.lines.append(line)

    def remove_line(self, line: LineComponent):
        self.lines.remove(line)

    def add_circle(self, circle: CircleComponent):
        self.circles.append(circle)

    def remove_circle(self, circle: CircleComponent):
        self.circles.remove(circle)
