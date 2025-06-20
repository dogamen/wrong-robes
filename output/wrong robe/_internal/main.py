import pygame
import sys

from main_menu import main_menu
from cutscene import cutscenes
from level_0 import level0
from level_1 import level1
from level_2 import level2
from bossfight_scene import run_cutscene
from bossfight1 import bossfight
from bossfight2 import bossfight2

def run_game_sequence(screen, clock, WORLD_WIDTH, WORLD_HEIGHT):
    result = cutscenes(screen, clock)
    if result != "finished":
        return "quit"

    # Запуск уровней и кат-сцены
    level0(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
    level1(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
    level2(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
    run_cutscene(screen, clock)
    bossfight()
    bossfight2()

    return "quit"

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption("Начало игры")
    clock = pygame.time.Clock()

    WORLD_WIDTH = 12000
    WORLD_HEIGHT = 8000

    while True:
        choice = main_menu(screen, clock)
        if choice == "start":
            result = run_game_sequence(screen, clock, WORLD_WIDTH, WORLD_HEIGHT)
            if result == "quit":
                break
        elif choice == "quit":
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
