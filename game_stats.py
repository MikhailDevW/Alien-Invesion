class GameStats:
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.ships_left = 3
        self.score = 0
        self.game_active = True     # Игра Alien Invasion запускается в активном состоянии.
