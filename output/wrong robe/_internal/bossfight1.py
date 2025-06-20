import pygame
import random
import sys

from constants import *
from assets import load_assets, load_menu_assets

pygame.init()
clock = pygame.time.Clock()

# Инициализация экрана в полноэкранном режиме и получение размеров
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption('game')

# Загрузка ресурсов и установка иконки окна
assets = load_assets(screen_width, screen_height)
pygame.display.set_icon(assets['icon'])

# Основные переменные состояния
running = True
death_animating = False
death_anim_start_time = 0
walls_start_time = None


def death_screen(screen, clock, assets):
    menu_assets = load_menu_assets(screen.get_width(), screen.get_height())
    main_menu_buttons = menu_assets['main_menu_buttons']

    restart_img = main_menu_buttons["restart"]
    restart_zh_img = main_menu_buttons["restart_zh"]
    quit_img = main_menu_buttons["quit_button"]
    quit_zh_img = main_menu_buttons["quit_button_zh"]

    restart_rect = restart_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    quit_rect = quit_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    selected_restart = False
    selected_quit = False
    delay_start = 0
    delay_time = 400

    pygame.mouse.set_visible(True)

    while True:
        screen.fill((0, 0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    selected_restart = True
                    delay_start = pygame.time.get_ticks()
                elif quit_rect.collidepoint(mouse_x, mouse_y):
                    selected_quit = True
                    delay_start = pygame.time.get_ticks()

        screen.blit(restart_zh_img if selected_restart else restart_img, restart_rect)
        screen.blit(quit_zh_img if selected_quit else quit_img, quit_rect)

        pygame.display.flip()
        clock.tick(60)

        if (selected_restart or selected_quit) and pygame.time.get_ticks() - delay_start > delay_time:
            pygame.mouse.set_visible(False)
            return "restart" if selected_restart else "quit"


# Воспроизведение музыки
def play_bossfight_music(loop=True, volume=0.5):
    pygame.mixer.music.load("sound/bossfight_sound.mp3")
    pygame.mixer.music.set_volume(volume)
    loops = -1 if loop else 0
    pygame.mixer.music.play(loops=loops)


# громкость музыки
def set_music_volume(volume):
    pygame.mixer.music.set_volume(volume)


# Сброс игры в начальное состояние
def reset_game():
    global player_x, player_y, player_direction, player_anim_count
    global bg_y, balls, walls, walls_active, walls_start_time
    global last_player_anim_time, last_bg_move_time
    global last_ball_add_time, last_ball_anim_time
    global last_wall_anim_time, last_wall_add_time
    global ball_anim_frame, wall_anim_frame
    global death_animating, death_anim_start_time
    global moving

    music_volume = 0.1
    play_bossfight_music(volume=music_volume)

    player_x = screen_width // 2
    player_y = screen_height // 2
    player_direction = 'right'
    player_anim_count = 0

    bg_y = 0

    balls = [{
        'x': random.randint(10, screen_width - BALL_WIDTH - 10),
        'y': 0,
        'speed': BALL_SPEED,
        'is_spawning': True,
        'spawn_frame': 0,
        'spawn_start_time': pygame.time.get_ticks(),
        'pause_start_time': pygame.time.get_ticks(),
        'paused': True
    }]

    walls = []
    walls_active = False
    walls_start_time = None

    last_player_anim_time = 0
    last_bg_move_time = 0
    last_ball_add_time = pygame.time.get_ticks()
    last_ball_anim_time = pygame.time.get_ticks()
    last_wall_anim_time = pygame.time.get_ticks()
    last_wall_add_time = 0

    ball_anim_frame = 0
    wall_anim_frame = 0

    death_animating = False
    death_anim_start_time = 0

    moving = False


# Обработка нажатий клавиш для перемещения игрока
def handle_input():
    global player_x, player_y, player_direction, moving
    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_a]:
        player_x -= PLAYER_SPEED
        player_direction = 'left'
        moving = True
    if keys[pygame.K_d]:
        player_x += PLAYER_SPEED
        player_direction = 'right'
        moving = True
    if keys[pygame.K_w]:
        player_y -= PLAYER_SPEED
        moving = True
    if keys[pygame.K_s]:
        player_y += PLAYER_SPEED + 7
        moving = True

    # Ограничение перемещения по границам экрана
    player_x = max(0, min(screen_width - PLAYER_WIDTH, player_x))
    player_y = max(0, min(screen_height - PLAYER_HEIGHT, player_y))


# Обновление и отрисовка прокрута фона
def update_background(now):
    global bg_y, last_bg_move_time
    if now - last_bg_move_time > BG_SCROLL_INTERVAL:
        bg_y += 7
        if bg_y >= screen_height:
            bg_y = 0
        last_bg_move_time = now

    screen.blit(assets['bg'], (0, int(bg_y)))
    screen.blit(assets['bg'], (0, int(bg_y - screen_height)))


# Обновление анимации и отрисовка игрока
def update_player(now):
    global player_anim_count, last_player_anim_time
    if moving and now - last_player_anim_time > PLAYER_ANIM_INTERVAL:
        player_anim_count = (player_anim_count + 1) % len(assets['walk_right'])
        last_player_anim_time = now

    frame = assets['walk_left'][player_anim_count] if player_direction == 'left' else assets['walk_right'][player_anim_count]
    screen.blit(pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT)), (player_x, player_y))


# Обновление и отрисовка мячей
def update_balls(now):
    global ball_anim_frame, last_ball_anim_time, last_ball_add_time, walls_active, balls, walls_start_time
    if not walls_active and now - last_ball_add_time >= BALL_ADD_INTERVAL and len(balls) < MAX_BALLS:
        balls.append({
            'x': random.randint(10, screen_width - BALL_WIDTH - 10),
            'y': 0,
            'speed': BALL_SPEED,
            'is_spawning': True,
            'spawn_frame': 0,
            'spawn_start_time': now,
            'pause_start_time': now,
            'paused': True
        })
        last_ball_add_time = now

    if not walls_active and len(balls) >= MAX_BALLS and now - last_ball_add_time >= 20000:
        walls_active = True
        walls.clear()
        balls.clear()
        walls_start_time = now

    if now - last_ball_anim_time >= BALL_ANIM_INTERVAL:
        ball_anim_frame = (ball_anim_frame + 1) % len(assets['electroball_frames'])
        last_ball_anim_time = now

    for ball in balls:
        if ball['paused']:
            if now - ball['pause_start_time'] < PAUSE_DURATION:
                screen.blit(pygame.transform.scale(assets['spawn_frames'][0], (BALL_WIDTH, BALL_HEIGHT)), (ball['x'], ball['y']))
                continue
            else:
                ball['paused'] = False
                ball['spawn_start_time'] = now

        if ball['is_spawning']:
            if now - ball['spawn_start_time'] >= SPAWN_ANIM_INTERVAL:
                ball['spawn_frame'] += 1
                ball['spawn_start_time'] = now

            if ball['spawn_frame'] < len(assets['spawn_frames']):
                spawn_img = pygame.transform.scale(assets['spawn_frames'][ball['spawn_frame']], (BALL_WIDTH, BALL_HEIGHT))
                screen.blit(spawn_img, (ball['x'], ball['y']))
            else:
                ball['is_spawning'] = False
        else:
            frame = pygame.transform.scale(assets['electroball_frames'][ball_anim_frame], (BALL_WIDTH, BALL_HEIGHT))
            screen.blit(frame, (ball['x'], ball['y']))
            ball['y'] += ball['speed']

            # респавн мяча обратно наверх при выходе за экран
            if ball['y'] > screen_height:
                ball['x'] = random.randint(10, screen_width - BALL_WIDTH - 10)
                ball['y'] = 0
                ball['is_spawning'] = True
                ball['spawn_frame'] = 0
                ball['spawn_start_time'] = now
                ball['pause_start_time'] = now
                ball['paused'] = True


# Обновление и отрисовка энергетических стен
def update_walls(now):
    global wall_anim_frame, last_wall_anim_time, last_wall_add_time, walls
    global running
    global walls_start_time

    if not walls_active:
        return

    # Завершение игры через 20 секунд прохождения стен
    if walls_start_time is not None and now - walls_start_time >= 20000:
        running = False
        return

    if now - last_wall_anim_time >= WALL_ANIM_INTERVAL:
        wall_anim_frame = (wall_anim_frame + 1) % len(assets['energy_wall_left'])
        last_wall_anim_time = now

    if now - last_wall_add_time >= WALL_ADD_INTERVAL:
        gap_x = random.randint(100, screen_width - WALL_GAP - 100)
        walls.append({
            'gap_x': gap_x,
            'gap_width': WALL_GAP,
            'y': 0,
            'speed': WALL_SPEED,
            'pause_start_time': now,
            'paused': True
        })
        last_wall_add_time = now

    for wall in walls:
        left_img = pygame.transform.scale(assets['energy_wall_left'][wall_anim_frame], (wall['gap_x'], 48))
        right_x = wall['gap_x'] + wall['gap_width']
        right_img = pygame.transform.scale(assets['energy_wall_right'][wall_anim_frame], (screen_width - right_x, 48))

        screen.blit(left_img, (0, wall['y']))
        screen.blit(right_img, (right_x, wall['y']))

        if wall['paused']:
            if now - wall['pause_start_time'] >= WALL_PAUSE_DURATION:
                wall['paused'] = False
        else:
            wall['y'] += wall['speed']

    walls[:] = [w for w in walls if w['y'] < screen_height]


# Проверка столкновений игрока с объектами
def check_collisions():
    global death_animating, death_anim_start_time
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    for ball in balls:
        if not ball['is_spawning'] and not ball['paused']:
            ball_rect = pygame.Rect(ball['x'], ball['y'], BALL_WIDTH, BALL_HEIGHT)
            if player_rect.colliderect(ball_rect):
                death_animating = True
                death_anim_start_time = pygame.time.get_ticks()

    for wall in walls:
        if not wall['paused']:
            if player_y + PLAYER_HEIGHT > wall['y'] and player_y < wall['y'] + 48:
                if player_x < wall['gap_x'] or player_x + PLAYER_WIDTH > wall['gap_x'] + wall['gap_width']:
                    death_animating = True
                    death_anim_start_time = pygame.time.get_ticks()


# Воспроизведение анимации смерти игрока
def play_death_animation(now):
    global death_animating
    frame_index = (now - death_anim_start_time) // DEATH_FRAME_DURATION
    if frame_index < len(assets['dead_el']):
        frame = pygame.transform.scale(assets['dead_el'][frame_index], (PLAYER_WIDTH, PLAYER_HEIGHT))
        screen.blit(frame, (player_x, player_y))
    else:
        death_animating = False
        result = death_screen(screen, clock, assets)
        if result == "restart":
            reset_game()
        else:
            pygame.quit()
            sys.exit()


def bossfight():
    reset_game()

    global running

    while running:
        now = pygame.time.get_ticks()
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if not death_animating:
            handle_input()
            update_background(now)
            update_player(now)
            update_balls(now)
            update_walls(now)
            check_collisions()
        else:
            play_death_animation(now)

        pygame.display.flip()
        clock.tick(60)

    return


if __name__ == '__main__':
    bossfight()
    pygame.quit()
    sys.exit()
