import sys
import pygame
import random

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from infoborder import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        # Настройки для полноэкранного режим
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # Его называют display rface, что можно перевести как экранная(дисплейная поверхность.
        # Она главная.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # задаем параметры главной игровой области
        pygame.display.set_caption("Alien Invasion")                    # Установка заголовка окна
        self.bg_color = self.settings.bg_color                          # Установка цвета фона главной области

        self.clock = pygame.time.Clock()

        self.stats = GameStats(self)            # Создание экземпляра для хранения игровой статистики.
        self.sb = Scoreboard(self)

        self.ship = Ship(self.screen)           # Создание экземпляра для создания корабля.
        self.bullets = pygame.sprite.Group()    # Создание экземпляра
        self.aliens = pygame.sprite.Group()     # Создание экземпляра
        # self._create_fleet()

    # def _create_fleet(self):
        # # Создание пришельца.
        # alien = Alien(self)
        # alien_width = alien.rect.width
        # available_space_x = self.settings.screen_width - (2 * alien_width)
        # number_aliens_x = available_space_x // (2 * alien_width)
        #
        # # Создание первого ряда пришельцев.
        # for alien_number in range(number_aliens_x):
        #     # Создание пришельца и размещение его в ряду.
        #     self._create_alien(alien_number)

    def _create_alien(self):
        # if len(self.bullets) < self.settings.bullets_allowed:
        #     new_bullet = Bullet(self)
        #     self.bullets.add(new_bullet)
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = random.randrange(alien_width, 1100, 100)  # alien_width # + 2 * alien_width * 1 # alien_number
        alien.rect.x = alien.x
        if len(self.aliens) < 5:
            self.aliens.add(alien)

    # Проверка была ли нажата клавиша, и какая
    def _check_event_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    # Проверка были ли отжата клавиша, и какая
    def _check_event_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Запуск нового снаряда
    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Удаление снарядов вышедших за границу поля
    def _update_bullets(self):
        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += 1
            self.sb.prep_score()
            print(self.stats.score)

    # Проверка столкновения с кораблем (минус жизнь)
    def _ship_hit(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.stats.ships_left -= 1              # Уменьшение ships_left.
            self.sb.prep_ships()
            self.aliens.empty()                     # Очистка списков пришельцев и снарядов.
            self.bullets.empty()
            print("Ship hit!!!")
            print(f"You have {self.stats.ships_left}!!!")
            if self.stats.ships_left == 0:          # Проверка, если израсходовали все жизни то игра останавливается
                self.stats.game_active = False

    # Проверка достигли ли пришельцы нижнего края области игры и минус жизнь
    def _is_aliens_bot(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:     # Происходит то же, что при столкновении с кораблем.
                self.stats.ships_left -= 1              # Уменьшение ships_left.
                self.sb.prep_ships()
                self.aliens.empty()                     # Очистка списков пришельцев и снарядов.
                self.bullets.empty()
                print("Alien is overbottom!!!")
                print(f"You have {self.stats.ships_left}!!!")
                if self.stats.ships_left == 0:
                    self.stats.game_active = False

    def check_events(self):
        self.clock.tick(self.settings.FPS)
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_event_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_event_keyup(event)

    def update_game(self):
        self.ship.update()      # Обновляем состояние корабля
        self.bullets.update()   # Обновляем состояние снарядов
        self.aliens.update()    # Обновляем состояние пришельцев
        self._update_bullets()  # Обновляем состояние
        self._ship_hit()        # Проверяем столкновение с кораблем
        self._is_aliens_bot()   # Проверяем положение пришельцев

        # if not self.aliens:
        #     # Уничтожение существующих снарядов и создание нового флота.
        #     self.bullets.empty()
        #     #self._create_fleet()

    def render(self):
        self.screen.fill(self.bg_color)         # При каждом проходе цикла перерисовывается экран.

        self.ship.blitme()                      # Прорисовка корабля
        for bullet in self.bullets.sprites():   # Прорисовка пулек
            bullet.draw_bullet()
        self.aliens.draw(ai.screen)
        self._create_alien()
        self.sb.show_score()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self.check_events()
            if self.stats.game_active:
                self.update_game()
            self.render()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()

    # Run the game
    ai.run_game()
