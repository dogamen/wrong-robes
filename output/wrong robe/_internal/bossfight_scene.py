import pygame
import sys

def run_cutscene(screen, clock):
    # Шрифт для текста
    font = pygame.font.SysFont("arial", 40)

    # Тексты под слайдами
    texts = [
        "тебя отправили выполнять задание вместо меня?",
        "так готовься умереть"
    ]

    # Загрузка и масштабирование двух изображений
    images = [
        pygame.transform.scale(
            pygame.image.load(f'images/b_scenes/b_scene{i}.jpeg').convert_alpha(),
            (800, 450)
        )
        for i in range(1, 3)
    ]

    # Центр экрана
    screen_width, screen_height = screen.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Позиции для каждого слайда (по центру)
    positions = [
        (center_x - 800 // 2, center_y - 450 // 2),
        (center_x - 800 // 2, center_y - 450 // 2)
    ]

    current_slide = 0

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if current_slide < len(images) - 1:
                        current_slide += 1
                    else:
                        running = False

        # Отрисовка текущего слайда
        img = images[current_slide]
        x, y = positions[current_slide]
        screen.blit(img, (x, y))

        # Отрисовка текста под изображением
        text_surface = font.render(texts[current_slide], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width // 2, y + 480))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption("Кат-сцена")
    clock = pygame.time.Clock()

    run_cutscene(screen, clock)