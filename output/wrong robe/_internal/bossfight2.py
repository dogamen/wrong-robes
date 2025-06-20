import pygame
import random
import sys
from assets import load_assets, load_menu_assets
from constants import *

pygame.init()
clock = pygame.time.Clock()

screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bossfight")

assets = load_assets(screen_width, screen_height)
pygame.display.set_icon(assets['icon'])

bg = assets['bg_bossfight']

font = pygame.font.SysFont("arial", 24, bold=True)

# Функция воспроизведения музыки
def play_bossfight_music(loop=True, volume=0.5):
    pygame.mixer.music.load("sound/bossfight_sound.mp3")
    pygame.mixer.music.set_volume(volume)
    loops = -1 if loop else 0
    pygame.mixer.music.play(loops=loops)

def set_music_volume(volume):
    pygame.mixer.music.set_volume(volume)

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

def update_frame_index(current_index, frame_count, last_update, delay, now):
    if now - last_update > delay:
        current_index = (current_index + 1) % frame_count
        last_update = now
    return current_index, last_update

def draw_controls_hint(surface):
    x = surface.get_width() - 200
    y = 20
    line_spacing = 30

    # Цвет текста
    text_color = (255, 255, 255)

    block_text = font.render('Блок: "q"', True, text_color)
    attack_text = font.render('Удар: "space"', True, text_color)

    bg_rect = pygame.Rect(x - 10, y - 10, 190, 70)
    s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 150))
    surface.blit(s, (bg_rect.x, bg_rect.y))

    surface.blit(block_text, (x, y))
    surface.blit(attack_text, (x, y + line_spacing))


def bossfight2():
    music_volume = 0.1
    play_bossfight_music(volume=music_volume)

    stay_frames = assets['stay_animation_player']
    stay_frame_index = 0
    stay_frame_delay = 100
    last_stay_frame_time = pygame.time.get_ticks()

    boss_frames = assets['animation_boss']
    boss_frame_index = 0
    boss_frame_delay = 150
    last_boss_frame_time = pygame.time.get_ticks()

    kick_boss_frames = assets['kick_animation_boss']
    kick_boss_index = 0
    kick_boss_delay = 100
    last_kick_boss_time = 0
    is_boss_kicking = False
    next_boss_kick_time = pygame.time.get_ticks() + random.randint(2000, 5000)
    boss_damage_done = False
    boss_kick_delay_range = [2000, 5000]

    kick_frames = assets['kick_animation_player']
    kick_frame_index = 0
    kick_frame_delay = 100
    last_kick_frame_time = 0
    is_kicking = False

    damage_frames = assets['damage_boss']
    damage_frame = None

    block_image = assets['block_player']
    is_blocking = False
    block_start_time = 0
    block_max_duration = 2000

    max_hp_width = 400
    hp_bar_height = 20
    margin = 10
    boss_health_width = max_hp_width
    player_health_width = max_hp_width

    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and not is_kicking and not is_blocking:
                    is_kicking = True
                    kick_frame_index = 0
                    last_kick_frame_time = now
                    damage_frame = random.choice(damage_frames)
                    old_health = boss_health_width
                    boss_health_width = max(0, boss_health_width - 10)
                    if old_health // 100 > boss_health_width // 100:
                        boss_kick_delay_range[0] = max(500, boss_kick_delay_range[0] - 500)
                        boss_kick_delay_range[1] = max(1000, boss_kick_delay_range[1] - 1000)
                elif event.key == pygame.K_q and not is_kicking:
                    is_blocking = True
                    block_start_time = now
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    is_blocking = False

        if is_blocking and now - block_start_time > block_max_duration:
            is_blocking = False

        if now >= next_boss_kick_time and not is_boss_kicking:
            is_boss_kicking = True
            kick_boss_index = 0
            last_kick_boss_time = now
            boss_damage_done = False

        if is_boss_kicking:
            if now - last_kick_boss_time > kick_boss_delay:
                kick_boss_index += 1
                last_kick_boss_time = now
                if kick_boss_index >= len(kick_boss_frames):
                    if not is_blocking and not boss_damage_done:
                        player_health_width = max(0, player_health_width - 100)
                        boss_damage_done = True
                    is_boss_kicking = False
                    next_boss_kick_time = now + random.randint(boss_kick_delay_range[0], boss_kick_delay_range[1])

        if not is_boss_kicking and now - last_boss_frame_time > boss_frame_delay:
            boss_frame_index = (boss_frame_index + 1) % len(boss_frames)
            last_boss_frame_time = now

        if is_kicking:
            if now - last_kick_frame_time > kick_frame_delay:
                kick_frame_index += 1
                last_kick_frame_time = now
                if kick_frame_index >= len(kick_frames):
                    is_kicking = False
                    damage_frame = None
        elif not is_blocking:
            stay_frame_index, last_stay_frame_time = update_frame_index(stay_frame_index, len(stay_frames), last_stay_frame_time, stay_frame_delay, now)

        screen.blit(bg, (0, 0))

        if is_boss_kicking:
            boss_image = kick_boss_frames[kick_boss_index]
        elif damage_frame:
            boss_image = damage_frame
        else:
            boss_image = boss_frames[boss_frame_index]
        screen.blit(boss_image, (0, 0))

        player_y_offset = -100
        if is_kicking:
            player_image = kick_frames[kick_frame_index]
        elif is_blocking:
            player_image = block_image
        else:
            player_image = stay_frames[stay_frame_index]
        screen.blit(player_image, (0, player_y_offset))

        boss_bar_x = 250
        boss_bar_y = margin + 100
        player_bar_x = 250
        player_bar_y = screen_height - margin - hp_bar_height - 100

        pygame.draw.rect(screen, (255, 0, 0), (boss_bar_x, boss_bar_y, boss_health_width, hp_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (player_bar_x, player_bar_y, player_health_width, hp_bar_height))

        draw_controls_hint(screen)

        if player_health_width == 0:
            choice = death_screen(screen, clock, assets)
            if choice == "restart":
                return True
            else:
                return False

        if boss_health_width == 0:
            end_time = pygame.time.get_ticks() + 2000
            toggle = True
            while pygame.time.get_ticks() < end_time:
                screen.blit(bg, (0, 0))
                screen.blit(kick_boss_frames[0 if toggle else 1], (0, 0))
                toggle = not toggle
                pygame.display.flip()
                pygame.time.delay(100)
            return False

        pygame.display.flip()
        clock.tick(60)

    return False


if __name__ == "__main__":
    while True:
        restart = bossfight2()
        if not restart:
            break

    pygame.quit()
    sys.exit()

