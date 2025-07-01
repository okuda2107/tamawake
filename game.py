from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pygame

import level_loader
from actor import Actor, state
from audio_system import AudioSystem
from mediapipe_input import MediapipeInput, camera_check
from physics import Physics
from test import Test

if TYPE_CHECKING:
    from sprite_component import SpriteComponent


class Game:
    def __init__(self):
        self.__is_running: bool = True
        self.__is_updating_actors: bool = False
        self.__ticks_counts: pygame.time.Clock = pygame.time.Clock()
        self.physics = Physics()
        self.mediapipe = MediapipeInput()
        self.audio_system = AudioSystem()
        self.screen_size = np.array([1300, 700])  # (1300, 700)
        self.camera_check_mode: bool = False
        self.__actors: list[Actor] = []
        self.__pending_actors: list[Actor] = []
        self.__sprites: list[SpriteComponent] = []

        self.point = 0

    def initialize(self) -> bool:
        result = pygame.init()
        if result[1] != 0:
            print(pygame.get_error())
            return False
        level_loader.load_game_properties(self, "asset/GameProperty.json")
        if self.camera_check_mode:
            camera_check()
            return False
        pygame.display.set_caption("tama|wake")
        self.__screen = pygame.display.set_mode(
            size=self.screen_size, flags=pygame.RESIZABLE
        )
        if self.__screen is None:
            print(pygame.get_error())
            return False
        if not self.mediapipe.initialize():
            print(pygame.get_error())
            return False
        self.__load_data()
        return True

    def run_loop(self) -> None:
        while self.__is_running:
            self.__process_input()
            self.__update_game()
            self.__generate_output()

    def __process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__is_running = False
        self.__is_updating_actors = True
        for actor in self.__actors:
            actor.process_input()
        self.__is_updating_actors = False

    def __update_game(self) -> None:
        delta_time: float = self.__ticks_counts.tick_busy_loop(25) / 1000
        if delta_time > 0.05:
            delta_time = 0.05
        self.__is_updating_actors = True
        for actor in self.__actors:
            actor.update(delta_time)
        self.__is_updating_actors = False
        for pending in self.__pending_actors:
            self.__actors.append(pending)
        self.__pending_actors.clear()
        dead_actors: list[Actor] = []
        for actor in self.__actors:
            if actor.state == state.dead:
                dead_actors.append(actor)
        for actor in dead_actors:
            actor.__del__()
        dead_actors.clear()

    def __generate_output(self) -> None:
        self.__screen.fill((43, 45, 49))
        for sprite in self.__sprites:
            sprite.draw(self.__screen)
        pygame.display.update()

    def shutdown(self) -> None:
        self.mediapipe.shutdown()
        pygame.quit()

    def add_actor(self, actor: Actor) -> None:
        if self.__is_updating_actors:
            self.__pending_actors.append(actor)
        else:
            self.__actors.append(actor)

    def remove_actor(self, actor: Actor) -> None:
        if actor in self.__pending_actors:
            self.__pending_actors.remove(actor)
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_sprite(self, sprite_comp: SpriteComponent) -> None:
        my_draw_order: int = sprite_comp.draw_order
        index = -1
        for sprite in self.__sprites:
            index += 1
            if my_draw_order < sprite.draw_order:
                break
        self.__sprites.insert(index, sprite_comp)

    def remove_sprite(self, sprite_comp: SpriteComponent) -> None:
        if sprite_comp in self.__sprites:
            self.__sprites.remove(sprite_comp)

    def __load_data(self) -> None:
        Test(self)
        # level_loader.load_level(self, "asset/title.json")
