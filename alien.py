import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        """Инициализирует пришельца и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))

        # Каждый новый пришелец появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции пришельца.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.count = 0
        self.flag = 'right'

    def update(self):
        self.y += 1
        self.rect.y = self.y
