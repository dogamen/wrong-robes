import pygame
from assets import load_menu_assets

def main_menu(screen, clock):
    # Загрузка всех ресурсов меню
    menu_assets = load_menu_assets(1920, 1080)
    menu_frames = menu_assets['menu_frames']
    cursor_frames = menu_assets['cursor_frames']
    main_menu_buttons = menu_assets['main_menu_buttons']

    # Настройки анимации меню
    current_menu_frame = 0
    menu_frame_delay = 150
    menu_last_update = pygame.time.get_ticks()

    # Кнопки
    button_rects = {
        "new_game": main_menu_buttons["new_game"].get_rect(topleft=(700, 420)),
        "continue": main_menu_buttons["con"].get_rect(topleft=(715, 500)),
        "quit": main_menu_buttons["quit_button"].get_rect(topleft=(775, 580))
    }

    # Анимация курсора
    current_cursor_frame = 0
    cursor_frame_delay = 120
    cursor_last_update = pygame.time.get_ticks()
    play_cursor_animation = False
    pygame.mouse.set_visible(False)

    # Переменные для логики выбора
    action_delay = 400
    action_start_time = 0
    new_game = False
    exit_game = False

    running = True
    while running:
        now = pygame.time.get_ticks()

        # Анимация заднего фона меню
        if now - menu_last_update > menu_frame_delay:
            current_menu_frame = (current_menu_frame + 1) % len(menu_frames)
            menu_last_update = now

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Коррекция координат, если нужно
                adjusted_x = mouse_x + 50
                adjusted_y = mouse_y + 180

                if button_rects["quit"].collidepoint(adjusted_x, adjusted_y):
                    exit_game = True
                    action_start_time = now
                    main_menu_buttons["quit_button"] = main_menu_buttons["quit_button_zh"]

                elif button_rects["new_game"].collidepoint(adjusted_x, adjusted_y):
                    new_game = True
                    action_start_time = now
                    main_menu_buttons["new_game"] = main_menu_buttons["new_game_zh"]

                elif button_rects["continue"].collidepoint(adjusted_x, adjusted_y):
                    main_menu_buttons["con"] = main_menu_buttons["con_zh"]

                play_cursor_animation = True

        # Анимация курсора
        if play_cursor_animation and now - cursor_last_update > cursor_frame_delay:
            current_cursor_frame = (current_cursor_frame + 1) % len(cursor_frames)
            if current_cursor_frame == 0:
                play_cursor_animation = False
            cursor_last_update = now

        # Проверка логики завершения действия
        if exit_game and now - action_start_time > action_delay:
            return "quit"

        if new_game and now - action_start_time > action_delay:
            return "start"

        # Отрисовка фона и интерфейса
        screen.blit(menu_frames[current_menu_frame], (0, 0))
        screen.blit(main_menu_buttons["new_game"], button_rects["new_game"].topleft)
        screen.blit(main_menu_buttons["con"], button_rects["continue"].topleft)
        screen.blit(main_menu_buttons["quit_button"], button_rects["quit"].topleft)
        screen.blit(cursor_frames[current_cursor_frame], (mouse_x, mouse_y))

        pygame.display.flip()
        clock.tick(60)
