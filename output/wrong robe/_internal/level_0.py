import pygame
from player import Player
from function import (
    handle_player_movement, Spike, play_death_animation,
    animate_key, draw_key_collected, draw_door,
    check_spike_collision, check_key_collection, check_door_opening,
    camera_follow, walk_sound, play_level_music
)
from assets import load_assets, load_menu_assets

import sys

# Экран смерти
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

        # Подсвечивание кнопки при выборе
        screen.blit(restart_zh_img if selected_restart else restart_img, restart_rect)
        screen.blit(quit_zh_img if selected_quit else quit_img, quit_rect)

        pygame.display.flip()
        clock.tick(60)

        # Задержка перед переходом
        if (selected_restart or selected_quit) and pygame.time.get_ticks() - delay_start > delay_time:
            pygame.mouse.set_visible(False)
            return "restart" if selected_restart else "quit"

# Главный уровень
def level0(screen, clock, WORLD_WIDTH, WORLD_HEIGHT):
    pygame.mixer.init()
    play_level_music(volume=0.1)  # Фоновая музыка/громкость

    pygame.display.set_caption("Level 0")

    # Загрузка фона уровня
    level_bg = pygame.transform.scale(
        pygame.image.load('images/level/level0.png').convert_alpha(),
        (3000, 2000)
    )
    level_pos_x = (WORLD_WIDTH - 3000) // 2
    level_pos_y = (WORLD_HEIGHT - 2000) // 2

    player = Player(4740, 3235)
    level_bounds = pygame.Rect(level_pos_x, level_pos_y, 3000, 2000)

    # блоки как границы карты
    blocks = [
        pygame.Rect(4500, 3590, 2375, 800),
        pygame.Rect(5400, 4000, 100, 1000)
    ]

    # Загрузка ассетов
    assets = load_assets(screen.get_width(), screen.get_height())
    walk_left = assets["walk_left"]
    walk_right = assets["walk_right"]
    dead_el = assets["dead_el"]
    spike_frames = assets["spike_frames"]
    key_frames = assets["key"]
    door_frames = assets["door"]

    # Шипы
    spikes = [
        Spike(5000, 3115, spike_frames, scale=(124, 124)),
        Spike(5000, 3235, spike_frames, scale=(124, 124)),
        Spike(5000, 3355, spike_frames, scale=(124, 124)),
        Spike(5000, 3413, spike_frames, scale=(124, 124)),
    ]

    # Игровые переменные
    last_direction = "right"
    current_frame_index = 0
    last_update_time = 0
    is_dead = False
    death_frame_index = 0
    death_last_update = 0

    key_data = {"x": 5500, "y": 3300, "collected": False}
    key_frame_index = 0
    key_last_update = 0

    door_data = {"x": 6000, "y": 3300, "open": False}
    door_open_frame_index = 0
    door_last_update = 0

    fade_alpha = 0
    fade_speed = 3
    door_opened = False
    fade_done = False
    level_running = True

    while level_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not is_dead:
            # Обработка движения игрока
            dx, dy, frame_img, last_direction, current_frame_index, last_update_time = handle_player_movement(
                keys, walk_left, walk_right, last_direction, current_frame_index, last_update_time, walk_sound
            )
            old_pos = player.rect.copy()
            player.move(dx, dy)
            player.rect.clamp_ip(level_bounds)

            # Столкновение с блоками
            for block in blocks:
                if player.rect.colliderect(block):
                    player.rect = old_pos
                    break

            # Проверка столкновения с шипами
            if check_spike_collision(player, spikes):
                is_dead = True
                death_frame_index = 0
                death_last_update = pygame.time.get_ticks()

            # Проверка на взятие ключа
            check_key_collection(player, key_data, key_frames)
            # Проверка открытия двери
            check_door_opening(player, door_data, door_frames, key_data["collected"])

        if door_data["open"]:
            door_opened = True

        for spike in spikes:
            spike.update()

        # Камера
        cam_x, cam_y = camera_follow(player, screen.get_width(), screen.get_height(), WORLD_WIDTH, WORLD_HEIGHT)

        screen.fill((0, 0, 0))
        screen.blit(level_bg, (level_pos_x - cam_x, level_pos_y - cam_y))

        # отрисовка блоков как границ карты
        for block in blocks:
            pygame.draw.rect(screen, (0, 0, 0), block.move(-cam_x, -cam_y))

        # отрисовка шипов
        for spike in spikes:
            spike.draw(screen, cam_x, cam_y)

        # Анимация ключа
        if not key_data["collected"]:
            key_frame_index, key_last_update = animate_key(
                screen, key_data["x"] - cam_x, key_data["y"] - cam_y,
                key_frames, key_frame_index, key_last_update
            )
        else:
            draw_key_collected(screen, key_frames)

        # Дверь
        door_open_frame_index, door_last_update = draw_door(
            screen, door_data["x"] - cam_x, door_data["y"] - cam_y,
            door_frames, door_data["open"], door_open_frame_index, door_last_update
        )

        # Анимация игрока / смерти
        if not is_dead:
            screen.blit(frame_img, (player.rect.x - cam_x, player.rect.y - cam_y))
        else:
            is_dead, death_frame_index, death_last_update = play_death_animation(
                screen, player.rect.x - cam_x, player.rect.y - cam_y,
                dead_el, is_dead, death_frame_index, death_last_update
            )
            if death_frame_index >= len(dead_el) - 1:
                choice = death_screen(screen, clock, assets)
                if choice == "restart":
                    return level0(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
                elif choice == "quit":
                    pygame.quit()
                    sys.exit()

        # Затемнение при победе
        if door_opened and not fade_done:
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                fade_done = True
                level_running = False

            fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

# Запуск уровня
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    WORLD_WIDTH = 12000
    WORLD_HEIGHT = 8000
    level0(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
    pygame.quit()
