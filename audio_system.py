import pygame

class AudioSystem:
    def __init__(self):
        self.sound_by_name: dict[str, pygame.mixer.Sound] = {}

    def set_sound(self, file_name: str) -> None:
        if self.sound_by_name.get(file_name) == None:
            temp = pygame.mixer.Sound(file_name)
            self.sound_by_name[file_name] = temp

    def play(self, key: str) -> None:
        self.sound_by_name[key].play()

    def bgm(self, key: str) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(key)
        pygame.mixer.music.play(-1)
