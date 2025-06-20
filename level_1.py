import pygame
import sys
from player import Player
from function import (
    handle_player_movement, Spike, play_death_animation,
    animate_key, draw_key_collected, draw_door,
    check_spike_collision, check_key_collection, check_door_opening,
    camera_follow, play_level_music
)
from assets import load_assets, load_menu_assets


def death_screen(screen, clock):
    menu_assets = load_menu_assets(screen.get_width(), screen.get_height())
    btns = menu_assets['main_menu_buttons']

    restart_img, restart_zh_img = btns["restart"], btns["restart_zh"]
    quit_img, quit_zh_img = btns["quit_button"], btns["quit_button_zh"]

    restart_rect = restart_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    quit_rect = quit_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    selected_restart, selected_quit = False, False
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


def level1(screen, clock, WORLD_WIDTH, WORLD_HEIGHT):
    pygame.mixer.init()
    play_level_music(volume=0.1)
    pygame.display.set_caption("Level 1")

    walk_sound = pygame.mixer.Sound("sound/walk_sound.mp3")

    level_bg = pygame.image.load('images/level/level1.png').convert_alpha()
    level_bg = pygame.transform.scale(level_bg, (5000, 4000))
    level_rect = level_bg.get_rect(center=(WORLD_WIDTH // 2, WORLD_HEIGHT // 2))

    player = Player(3900, 3350)
    level_bounds = level_rect.copy()

    blocks = [
        pygame.Rect(3760, 3000, 2110, 150),
        pygame.Rect(3760, 3660, 2110, 150),
        pygame.Rect(3564, 3000, 200, 800),
        pygame.Rect(5720, 1950, 150, 1200),
        pygame.Rect(5720, 1950, 680, 160),
        pygame.Rect(5720, 3750, 150, 1000),
        pygame.Rect(5720, 4700, 600, 150),
        pygame.Rect(6264, 1950, 150, 2900),
    ]

    assets = load_assets(screen.get_width(), screen.get_height())
    walk_left, walk_right = assets["walk_left"], assets["walk_right"]
    dead_el, spike_frames = assets["dead_el"], assets["spike_frames"]
    key_frames, door_frames = assets["key"], assets["door"]

    spikes = [Spike(x, y, spike_frames, (124, 124)) for x, y in [
        (6070, 3088), (5938, 3088), (6070, 2828), (5938, 2828),
        (6070, 2568), (5938, 2568), (6070, 2310), (5938, 2310),
        (6070, 4380), (5938, 4380), (6070, 4124), (5938, 4124),
        (6070, 3864), (5938, 3864), (6070, 3604), (5938, 3604),
    ]]

    last_dir = "right"
    frame_idx = 0
    last_update = 0
    is_dead = False
    death_idx = 0
    death_update = 0

    key_data = {"x": 6040, "y": 2200, "collected": False}
    key_idx = 0
    key_update = 0

    door_data = {"x": 6004, "y": 4512, "open": False}
    door_idx = 0
    door_update = 0

    fade_alpha = 0
    fade_speed = 3
    fade_done = False
    door_opened = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not is_dead:
            dx, dy, frame_img, last_dir, frame_idx, last_update = handle_player_movement(
                keys, walk_left, walk_right, last_dir, frame_idx, last_update, walk_sound
            )
            old_pos = player.rect.copy()
            player.move(dx, dy)
            player.rect.clamp_ip(level_bounds)

            if any(player.rect.colliderect(b) for b in blocks):
                player.rect = old_pos

            if check_spike_collision(player, spikes):
                is_dead = True
                death_idx = 0
                death_update = pygame.time.get_ticks()

            check_key_collection(player, key_data, key_frames)
            check_door_opening(player, door_data, door_frames, key_data["collected"])

        if door_data["open"]:
            door_opened = True

        for spike in spikes:
            spike.update()

        cam_x, cam_y = camera_follow(player, screen.get_width(), screen.get_height(), WORLD_WIDTH, WORLD_HEIGHT)

        screen.fill((0, 0, 0))
        screen.blit(level_bg, (level_rect.x - cam_x, level_rect.y - cam_y))

        for block in blocks:
            pygame.draw.rect(screen, (0, 0, 0), block.move(-cam_x, -cam_y))

        for spike in spikes:
            spike.draw(screen, cam_x, cam_y)

        if not key_data["collected"]:
            key_idx, key_update = animate_key(
                screen, key_data["x"] - cam_x, key_data["y"] - cam_y,
                key_frames, key_idx, key_update
            )
        else:
            draw_key_collected(screen, key_frames)

        door_idx, door_update = draw_door(
            screen, door_data["x"] - cam_x, door_data["y"] - cam_y,
            door_frames, door_data["open"], door_idx, door_update
        )

        if not is_dead:
            screen.blit(frame_img, (player.rect.x - cam_x, player.rect.y - cam_y))
        else:
            is_dead, death_idx, death_update = play_death_animation(
                screen, player.rect.x - cam_x, player.rect.y - cam_y,
                dead_el, is_dead, death_idx, death_update
            )
            if death_idx >= len(dead_el) - 1:
                choice = death_screen(screen, clock)
                return level1(screen, clock, WORLD_WIDTH, WORLD_HEIGHT) if choice == "restart" else sys.exit()

        if door_opened and not fade_done:
            fade_alpha = min(fade_alpha + fade_speed, 255)
            if fade_alpha >= 255:
                fade_done = True
                running = False

            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    WORLD_WIDTH, WORLD_HEIGHT = 12000, 8000

    level1(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
    pygame.quit()
