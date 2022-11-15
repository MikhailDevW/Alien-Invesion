import pygame


class Ship():
    """Класс для управления кораблем."""
    def __init__(self, screen):
        """Инициализирует корабль и задает его начальную позицию."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))

        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.delta = 5

    def update(self):
        """Обновляет позицию корабля с учетом флага."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.delta
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.delta

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        # .blit() - мето применяемый к поверхности НА которой рисуем
        # первый аргумент что рисуем, второй где
        self.screen.blit(self.image, self.rect)