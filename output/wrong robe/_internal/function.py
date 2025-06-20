import pygame

# Инициализация звука шага и задержки
walk_sound = pygame.mixer.Sound("sound/walk_sound.mp3")
walk_sound.set_volume(0.3)
last_walk_sound_time = 0
walk_sound_delay = 250  # мс между шагами

# Функции для проигрывания музыки уровня и боссфайта
def play_level_music(loop=True, volume=0.5):
    pygame.mixer.music.load("sound/level_sound.mp3")
    pygame.mixer.music.set_volume(volume)
    loops = -1 if loop else 0
    pygame.mixer.music.play(loops=loops)

def play_bossfight_music(loop=True, volume=0.5):
    pygame.mixer.music.load("sound/bossfight_sound.mp3")
    pygame.mixer.music.set_volume(volume)
    loops = -1 if loop else 0
    pygame.mixer.music.play(loops=loops)

def set_music_volume(volume):
    pygame.mixer.music.set_volume(volume)
    # pygame.mixer.sound не существует, убрал эту строку

# Класс шипа с анимацией и состояниями
class Spike:
    def __init__(self, x, y, spike_frames, scale=(32, 32)):
        self.images = [pygame.transform.scale(img, scale) for img in spike_frames]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_time = 120
        self.cycle_delay = 1000
        self.hold_last_frame = 1000

        self.state = "idle"
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0

    def update(self):
        now = pygame.time.get_ticks()

        if self.state == "idle" and now - self.last_update >= self.cycle_delay:
            self.state = "animating"
            self.current_frame = 1
            self.last_update = now

        elif self.state == "animating" and now - self.last_update >= self.animation_time:
            self.image = self.images[self.current_frame]
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.state = "hold"
                self.last_update = now

        elif self.state == "hold":
            self.image = self.images[-1]
            if now - self.last_update >= self.hold_last_frame:
                self.state = "idle"
                self.image = self.images[0]
                self.last_update = now

    def draw(self, surface, offset_x=0, offset_y=0):
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


# Обработка движения игрока и проигрывание звука шагов
def handle_player_movement(keys, walk_left, walk_right, last_direction, current_frame_index, last_update, walk_sound):
    global last_walk_sound_time

    dx, dy = 0, 0
    speed = 7
    animation_delay = 150
    now = pygame.time.get_ticks()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx = -speed
        last_direction = "left"
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = speed
        last_direction = "right"

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy = -speed
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy = speed

    # Анимация и звук шагов с задержкой
    if dx != 0 or dy != 0:
        if now - last_update > animation_delay:
            current_frame_index = (current_frame_index + 1) % len(walk_left)
            last_update = now
            if now - last_walk_sound_time > walk_sound_delay:
                walk_sound.play()
                last_walk_sound_time = now

    current_frame_img = walk_left[current_frame_index] if last_direction == "left" else walk_right[current_frame_index] if dx != 0 or dy != 0 else (walk_left[0] if last_direction == "left" else walk_right[0])

    return dx, dy, current_frame_img, last_direction, current_frame_index, last_update


# Анимация смерти игрока
def play_death_animation(surface, x, y, dead_el_frames, is_dead, death_frame_index, last_update):
    animation_delay = 100
    now = pygame.time.get_ticks()

    if is_dead:
        if now - last_update > animation_delay:
            death_frame_index = min(death_frame_index + 1, len(dead_el_frames) - 1)
            last_update = now
        surface.blit(dead_el_frames[death_frame_index], (x, y))
    else:
        death_frame_index = 0

    return is_dead, death_frame_index, last_update


# Анимация ключа
def animate_key(surface, x, y, key_frames, frame_index, last_update):
    animation_speed = 100
    now = pygame.time.get_ticks()

    if now - last_update > animation_speed:
        frame_index = (frame_index + 1) % len(key_frames)
        last_update = now

    surface.blit(key_frames[frame_index], (x, y))
    return frame_index, last_update


# Отрисовка собранного ключа на экране
def draw_key_collected(surface, key_frames):
    screen_width, screen_height = surface.get_size()
    key_image = key_frames[0]
    surface.blit(key_image, (20, screen_height - key_image.get_height() - 20))


# Отрисовка и анимация двери
def draw_door(surface, x, y, door_frames, is_open, open_frame_index=0, last_update=0):
    now = pygame.time.get_ticks()
    animation_speed = 150

    if not is_open:
        surface.blit(door_frames[0], (x, y))
        return 0, last_update

    if now - last_update > animation_speed:
        if open_frame_index < len(door_frames) - 1:
            open_frame_index += 1
        last_update = now

    surface.blit(door_frames[open_frame_index], (x, y))
    return open_frame_index, last_update


# Проверка столкновения игрока с шипами (активными на 4-м кадре)
def check_spike_collision(player, spikes):
    for spike in spikes:
        if player.rect.colliderect(spike.rect) and spike.current_frame == 3:
            return True
    return False


# Обновление состояния ключа при сборе игроком
def check_key_collection(player, key_data, key_frames):
    if not key_data["collected"]:
        key_rect = key_frames[0].get_rect(topleft=(key_data["x"], key_data["y"]))
        if player.rect.colliderect(key_rect):
            key_data["collected"] = True


# Обновление состояния двери при наличии ключа и столкновении с игроком
def check_door_opening(player, door_data, door_frames, key_collected):
    if key_collected:
        door_rect = door_frames[0].get_rect(topleft=(door_data["x"], door_data["y"]))
        if player.rect.colliderect(door_rect):
            door_data["open"] = True


# Центрирование камеры на игроке с ограничением границ мира
def camera_follow(player, screen_width, screen_height, world_width, world_height):
    cam_x = player.rect.centerx - screen_width // 2
    cam_y = player.rect.centery - screen_height // 2
    cam_x = max(0, min(cam_x, world_width - screen_width))
    cam_y = max(0, min(cam_y, world_height - screen_height))
    return cam_x, cam_y

def death_screen(screen, clock, death_animation_frames, main_menu_buttons):
    frame_index = 0
    frame_delay = 100
    last_update = pygame.time.get_ticks()

    restart_img = main_menu_buttons["restart"]
    restart_zh_img = main_menu_buttons["restart_zh"]
    quit_img = main_menu_buttons["quit_button"]
    quit_zh_img = main_menu_buttons["quit_button_zh"]

    restart_rect = restart_img.get_rect(center=(screen.get_width() // 2 - 150, screen.get_height() // 2 + 100))
    quit_rect = quit_img.get_rect(center=(screen.get_width() // 2 + 150, screen.get_height() // 2 + 100))

    show_buttons = False
    selected_restart = False
    selected_quit = False
    delay_start = 0
    delay_time = 400

    running = True
    while running:
        now = pygame.time.get_ticks()
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and show_buttons:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    selected_restart = True
                    delay_start = now
                elif quit_rect.collidepoint(mouse_pos):
                    selected_quit = True
                    delay_start = now

        if not show_buttons:
            if now - last_update > frame_delay:
                frame_index = min(frame_index + 1, len(death_animation_frames) - 1)
                last_update = now
                if frame_index == len(death_animation_frames) - 1:
                    show_buttons = True

            frame = death_animation_frames[frame_index]
            screen.blit(frame,
                        ((screen.get_width() - frame.get_width()) // 2,
                         (screen.get_height() - frame.get_height()) // 2))
        else:
            screen.fill((0, 0, 0))

            screen.blit(restart_zh_img if selected_restart else restart_img, restart_rect)
            screen.blit(quit_zh_img if selected_quit else quit_img, quit_rect)

            if (selected_restart or selected_quit) and now - delay_start > delay_time:
                return "restart" if selected_restart else "quit"

        pygame.display.flip()
        clock.tick(60)
