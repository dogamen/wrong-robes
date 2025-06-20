import pygame

def death_screen_menu(screen, clock, assets, cursor_frames):
    restart_img = assets["main_menu_buttons"]["restart"]
    restart_zh_img = assets["main_menu_buttons"]["restart_zh"]
    quit_img = assets["main_menu_buttons"]["quit_button"]
    quit_zh_img = assets["main_menu_buttons"]["quit_button_zh"]

    restart_rect = restart_img.get_rect(center=(960, 480))
    quit_rect = quit_img.get_rect(center=(960, 600))

    selected_restart = False
    selected_quit = False
    delay_start = 0
    delay_time = 400

    # Курсор
    current_cursor_frame = 0
    cursor_frame_delay = 120
    cursor_last_update = pygame.time.get_ticks()
    play_cursor_animation = False
    pygame.mouse.set_visible(False)

    # Затемнение
    fade_surface = pygame.Surface(screen.get_size()).convert_alpha()
    fade_alpha = 0
    fade_speed = 5  # чем меньше, тем медленнее затемнение

    while True:
        screen.fill((0, 0, 0))
        now = pygame.time.get_ticks()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    selected_restart = True
                    delay_start = now
                elif quit_rect.collidepoint(mouse_x, mouse_y):
                    selected_quit = True
                    delay_start = now
                play_cursor_animation = True

        # Кнопки с эффектом наведения и нажатия
        if restart_rect.collidepoint(mouse_x, mouse_y) or selected_restart:
            screen.blit(restart_zh_img, restart_rect.topleft)
        else:
            screen.blit(restart_img, restart_rect.topleft)

        if quit_rect.collidepoint(mouse_x, mouse_y) or selected_quit:
            screen.blit(quit_zh_img, quit_rect.topleft)
        else:
            screen.blit(quit_img, quit_rect.topleft)

        # Анимация курсора
        if play_cursor_animation and now - cursor_last_update > cursor_frame_delay:
            current_cursor_frame += 1
            if current_cursor_frame >= len(cursor_frames):
                current_cursor_frame = 0
                play_cursor_animation = False
            cursor_last_update = now

        screen.blit(cursor_frames[current_cursor_frame], (mouse_x, mouse_y))

        # Затемнение
        if fade_alpha < 255:
            fade_alpha = min(255, fade_alpha + fade_speed)
            fade_surface.fill((0, 0, 0, fade_alpha))
            screen.blit(fade_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

        # Обработка действий после задержки
        if selected_restart or selected_quit:
            if now - delay_start > delay_time:
                return "restart" if selected_restart else "quit"
