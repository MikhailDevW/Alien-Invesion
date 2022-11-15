import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Создает объект снарядов в текущей позиции корабля."""
    def __init__(self, ai):
        """Создает объект снарядов в текущей позиции корабля."""
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings
        self.color = (60, 60, 60)

        # Создание снаряда в позиции (0,0)  и назначение правильной позиции.
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.midtop = ai.ship.rect.midtop

        # Позиция снаряда хранится в веществ енном формате.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        # Обновление позиции снаряда в вещественном формате.
        self.y -= 3
        self.x -= 0

        # Обновление позиции прямоугольника.
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """Вывод снаряда на экран."""
        # Функция рисует геом примитивы на поверхности
        # 1 аргумент - поверхность где рисуем
        # 2 аргумент - цвет в РГБ
        # 3 аргумент - Третьим аргументом является кортеж из четырех чисел.
        # Первые два определяют координаты верхнего левого угла прямоугольника,
        # вторые – его ширину и высоту.
        pygame.draw.rect(self.screen, self.color, self.rect)