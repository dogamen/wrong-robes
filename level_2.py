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


def death_screen(screen, clock, assets):
    menu_assets = load_menu_assets(screen.get_width(), screen.get_height())
    restart_img = menu_assets['main_menu_buttons']["restart"]
    restart_zh_img = menu_assets['main_menu_buttons']["restart_zh"]
    quit_img = menu_assets['main_menu_buttons']["quit_button"]
    quit_zh_img = menu_assets['main_menu_buttons']["quit_button_zh"]

    restart_rect = restart_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    quit_rect = quit_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    selected_restart = selected_quit = False
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


def level2(screen, clock, WORLD_WIDTH, WORLD_HEIGHT):
    pygame.mixer.init()
    play_level_music(volume=0.1)
    pygame.display.set_caption("Level 2")

    walk_sound = pygame.mixer.Sound("sound/walk_sound.mp3")
    walk_sound.set_volume(0.5)

    level_bg = pygame.transform.scale(
        pygame.image.load('images/level/level2.png').convert_alpha(),
        (5000, 4000)
    )
    level_pos_x = (WORLD_WIDTH - 5000) // 2
    level_pos_y = (WORLD_HEIGHT - 4000) // 2

    player = Player(3640, 3135)
    level_bounds = pygame.Rect(level_pos_x, level_pos_y, 5000, 4000)

    blocks = [
        pygame.Rect(4750, 3470, 140, 1500),
        pygame.Rect(4196, 3470, 140, 1400),
        pygame.Rect(4056, 4270, 280, 660),
        pygame.Rect(3436, 3470, 340, 900),
        pygame.Rect(3420, 4268, 800, 130),
        pygame.Rect(4750, 4666, 420, 534),
        pygame.Rect(5724, 5200, 691, 2),
        pygame.Rect(5310, 3470, 550, 796),
        pygame.Rect(6280, 3470, 830, 264),
        pygame.Rect(5080, 4666, 1334, 135),
        pygame.Rect(6835, 3470, 280, 2125),
        pygame.Rect(5835, 4134, 1000, 132),
        pygame.Rect(5724, 5595, 1391, 2),
        pygame.Rect(5724, 5200, 140, 800),
        pygame.Rect(6280, 4666, 135, 535),
        pygame.Rect(3420, 4268, 220, 1200),
        pygame.Rect(3424, 5334, 910, 400),
        pygame.Rect(3436, 2870, 68, 600),
        pygame.Rect(3436, 2000, 1594, 930),
        pygame.Rect(5445, 2400, 2500, 530),
        pygame.Rect(5005, 1900, 1500, 100),
        pygame.Rect(7530, 2400, 900, 2265),
        pygame.Rect(5724, 5595, 560, 460),
        pygame.Rect(5024, 6000, 3000, 100),
        pygame.Rect(4224, 5595, 1080, 500),
        pygame.Rect(6280, 1900, 280, 660),
        pygame.Rect(7530, 5066, 1000, 1000),
        pygame.Rect(8360, 4500, 100, 700),
        pygame.Rect(4750, 4666, 420, 534),
    ]

    assets = load_assets(screen.get_width(), screen.get_height())
    walk_left = assets["walk_left"]
    walk_right = assets["walk_right"]
    dead_el = assets["dead_el"]
    spike_frames = assets["spike_frames"]
    key_frames = assets["key"]
    door_frames = assets["door"]

    spikes = [
        Spike(x, y, spike_frames, scale=(124, 124)) for x, y in [
            (3855, 3605), (3993, 3605), (4410, 3605), (4550, 3805),
            (4410, 4005), (4550, 4205), (4410, 4405), (4550, 4605),
            (4410, 4805), (4550, 5005), (5040, 5365), (4750, 5365),
            (7188, 3605), (7328, 3605), (7188, 4005), (7328, 4005),
            (7188, 4405), (7328, 4405), (7188, 4805), (7328, 4805),
            (7188, 5205), (7328, 5205), (7188, 5605), (7328, 5605),
            (4966, 3605), (5105, 3805), (4966, 4005), (5105, 4205),
            (4966, 4405), (5405, 4440), (6271, 4440), (5838, 4440),
        ]
    ]

    last_direction = "right"
    current_frame_index = 0
    last_update_time = 0
    is_dead = False
    death_frame_index = 0
    death_last_update = 0

    key_data = {"x": 6010, "y": 5400, "collected": False}
    key_frame_index = 0
    key_last_update = 0

    door_data = {"x": 6008, "y": 2140, "open": False}
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
            dx, dy, frame_img, last_direction, current_frame_index, last_update_time = handle_player_movement(
                keys, walk_left, walk_right, last_direction, current_frame_index, last_update_time, walk_sound
            )

            old_pos = player.rect.copy()
            player.move(dx, dy)
            player.rect.clamp_ip(level_bounds)

            if any(player.rect.colliderect(block) for block in blocks):
                player.rect = old_pos

            if check_spike_collision(player, spikes):
                is_dead = True
                death_frame_index = 0
                death_last_update = pygame.time.get_ticks()

            check_key_collection(player, key_data, key_frames)
            check_door_opening(player, door_data, door_frames, key_data["collected"])

        if door_data["open"]:
            door_opened = True

        for spike in spikes:
            spike.update()

        cam_x, cam_y = camera_follow(player, screen.get_width(), screen.get_height(), WORLD_WIDTH, WORLD_HEIGHT)

        screen.fill((0, 0, 0))
        screen.blit(level_bg, (level_pos_x - cam_x, level_pos_y - cam_y))

        for block in blocks:
            pygame.draw.rect(screen, (0, 0, 0), block.move(-cam_x, -cam_y))

        for spike in spikes:
            spike.draw(screen, cam_x, cam_y)

        if not key_data["collected"]:
            key_frame_index, key_last_update = animate_key(
                screen, key_data["x"] - cam_x, key_data["y"] - cam_y,
                key_frames, key_frame_index, key_last_update
            )
        else:
            draw_key_collected(screen, key_frames)

        door_open_frame_index, door_last_update = draw_door(
            screen, door_data["x"] - cam_x, door_data["y"] - cam_y,
            door_frames, door_data["open"], door_open_frame_index, door_last_update
        )

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
                    return level2(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
                else:
                    pygame.quit()
                    sys.exit()

        if door_opened and not fade_done:
            fade_alpha = min(fade_alpha + fade_speed, 255)
            fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            if fade_alpha >= 255:
                fade_done = True
                level_running = False

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    WORLD_WIDTH = 12000
    WORLD_HEIGHT = 8000
    level2(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
