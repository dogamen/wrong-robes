import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # зелёный прямоугольник для примера
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen, offset_x=0, offset_y=0):
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

# Инициализация Pygame
pygame.init()

# Загрузка анимации движения влево
movel = [
    pygame.transform.scale(pygame.image.load(f'images/player_go/go_{i}.png'), (80, 120))
    for i in range(1, 8)
]

# Загрузка анимации движения вправо
mover = [
    pygame.transform.scale(pygame.image.load(f'images/player_go/gor_{i}.png'), (80, 120))
    for i in range(1, 8)
]


class Player:
    def __init__(self, x, y):
        self.frame_index = 0
        self.animation_started = False
        self.direction = 'right'
        self.rect = pygame.Rect(x, y, 80, 120)
        self.skip_first_frame = True

    def draw(self, surface, offset_x=0, offset_y=0):
        # Выбор текущего кадра в зависимости от направления
        frames = movel if self.direction == 'left' else mover
        frame = frames[self.frame_index // 5 % len(frames)]

        # Отрисовка игрока с учетом смещения камеры
        draw_pos = (self.rect.x - offset_x, self.rect.y - offset_y)
        surface.blit(frame, draw_pos)

        # Обновление анимации
        if self.animation_started:
            if not self.skip_first_frame:
                self.frame_index += 1
            if self.frame_index >= len(frames) * 5:
                self.frame_index = 0
        else:
            self.frame_index = 0
            self.skip_first_frame = True

    def move(self, dx, dy):
        if dx != 0 or dy != 0:
            if not self.animation_started:
                self.skip_first_frame = True

            self.animation_started = True

            if dx < 0:
                self.direction = 'left'
            elif dx > 0:
                self.direction = 'right'

            self.rect.x += dx
            self.rect.y += dy
        else:
            self.animation_started = False