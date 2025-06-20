import pygame
import sys

def cutscenes(screen, clock):
    # Шрифт для текста под изображениями
    font = pygame.font.SysFont("arial", 28)

    # Текстовые реплики для каждой сцены
    texts = [
        "здесь можно поживиться",
        "только роба?",
        "какая аудиенция с королем?",
        "задание найти артефакты?",
        "они приняли меня за мага",
        "пора отправляться в путь"
    ]

    # Загрузка и масштабирование изображений сцен
    images = [
        pygame.transform.scale(
            pygame.image.load(f'images/scenes/scene{i}.jpeg').convert_alpha(),
            (500, 300)
        ) for i in range(1, 7)
    ]

    # отступы и размеры
    padding_x, padding_y = 40, 40
    img_width, img_height = 500, 300
    screen_width, screen_height = screen.get_size()

    # Общая ширина и высота изображений
    total_width = 3 * img_width + 2 * padding_x
    total_height = 2 * img_height + padding_y

    # Центрирование изображений на экране
    start_x = (screen_width - total_width) // 2
    start_y = (screen_height - total_height) // 2

    # Расчёт координат каждой сцены (3x2 сетка)
    positions = [
        (start_x + col * (img_width + padding_x),
         start_y + row * (img_height + padding_y))
        for row in range(2) for col in range(3)
    ]

    current_visible = 0  # Сколько сцен уже показано
    running = True

    while running:
        screen.fill((10, 10, 10))  # Очистка экрана (тёмный фон)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # перелистывание сцен и работа кнопок
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if current_visible < len(images):
                        current_visible += 1
                    if current_visible == len(images):
                        running = False

        # Отрисовка сцен и подписей к ним
        for i in range(current_visible):
            x, y = positions[i]
            screen.blit(images[i], (x, y))

            # Рендер текста под сценой
            text_surf = font.render(texts[i], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x + img_width // 2, y + img_height + 20))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(60)

    return "finished"


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Кат-сцена")
    clock = pygame.time.Clock()

    result = cutscenes(screen, clock)

    pygame.quit()
    sys.exit()
