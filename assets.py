import pygame

def load_assets(screen_width, screen_height):
    icon = pygame.image.load('images/icon.png')
    bg = pygame.transform.scale(pygame.image.load('images/bg.png'), (screen_width, screen_height))

    # Масштаб для игрока
    player_scale = (64, 124)

    walk_left = [pygame.transform.scale(pygame.image.load(f'images/player_left/player_left{i}.png').convert_alpha(), player_scale) for i in range(1, 8)]
    walk_right = [pygame.transform.scale(pygame.image.load(f'images/player_right/player_right{i}.png').convert_alpha(), player_scale) for i in range(1, 8)]

    electroball_frames = [pygame.image.load(f'images/atachment/ball{i}.png').convert_alpha() for i in range(1, 3)]
    spawn_frames = [pygame.image.load(f'images/ball/ball{i}.png').convert_alpha() for i in range(1, 5)]

    energy_wall_left = [pygame.image.load(f'images/energy_wall_left/energy_wall_left{i}.png').convert_alpha() for i in range(1, 5)]
    energy_wall_right = [pygame.image.load(f'images/energy_wall_right/energy_wall_right{i}.png').convert_alpha() for i in range(1, 5)]

    dead_el = [pygame.transform.scale(pygame.image.load(f'images/player_dead/dead_el{i}.png').convert_alpha(), player_scale) for i in range(1, 15)]

    animation_boss = [pygame.image.load(f'images/animation_boss/animation_boss{i}.png').convert_alpha() for i in range(1, 9)]
    damage_boss = [pygame.image.load(f'images/damage_boss/damage_boss{i}.png').convert_alpha() for i in range(1, 4)]
    kick_animation_boss = [pygame.image.load(f'images/kick_animation_boss/kick_animation_boss{i}.png').convert_alpha() for i in range(1, 6)]

    kick_animation_player = [pygame.image.load(f'images/kick_animation_player/kick_animation_player{i}.png').convert_alpha() for i in range(1, 4)]
    stay_animation_player = [pygame.image.load(f'images/stay_animation_player/stay_animation_player{i}.png').convert_alpha() for i in range(1, 6)]
    bg_bossfight = pygame.image.load('images/bg_bossfight.png').convert()
    block_player = pygame.image.load('images/block_player.png').convert_alpha()

    key = [pygame.transform.scale(pygame.image.load(f'images/key/key{i}.png').convert_alpha(), (64, 64)) for i in range(1, 9)]

    door = [pygame.transform.scale(pygame.image.load(f'images/door/door{i}.png').convert_alpha(), (124, 124)) for i in range(1, 7)]

    # Загрузка и масштабирование спрайтов шипов
    spike_frames = [pygame.image.load(f"images/spike/spike{i}.png").convert_alpha()for i in range(1, 5)]

    return {
        'icon': icon,
        'bg': bg,
        'walk_left': walk_left,
        'walk_right': walk_right,
        'electroball_frames': electroball_frames,
        'spawn_frames': spawn_frames,
        'energy_wall_left': energy_wall_left,
        'energy_wall_right': energy_wall_right,
        'dead_el': dead_el,
        'animation_boss': animation_boss,
        'damage_boss': damage_boss,
        'kick_animation_boss': kick_animation_boss,
        'kick_animation_player': kick_animation_player,
        'stay_animation_player': stay_animation_player,
        'bg_bossfight': bg_bossfight,
        'block_player': block_player,
        'spike_frames': spike_frames,
        'key': key,
        'door': door,
    }

def load_menu_assets(screen_width, screen_height):
    menu_frames = [pygame.transform.scale(
        pygame.image.load(f'images/Main_menu/Menu_{i}.png'), (screen_width, screen_height))
        for i in range(1, 17)]

    cursor_frames = [pygame.transform.scale(
        pygame.image.load(f'images/Main_menu/Cursor_{i}.png'), (100, 200))
        for i in range(1, 5)]

    stay_left = [pygame.transform.scale(
        pygame.image.load(f'images/Player_stay_left/Left_{i}.png'), (128, 240))
        for i in range(1, 11)]

    stay_right = [pygame.transform.flip(img, True, False) for img in stay_left]

    main_menu_buttons = {
        "new_game": pygame.image.load('images/Main_menu/New game.png'),
        "new_game_zh": pygame.image.load('images/Main_menu/New_game_zh.png'),
        "quit_button": pygame.image.load('images/Main_menu/Quit.png'),
        "quit_button_zh": pygame.image.load('images/Main_menu/Quit_zh.png'),
        "con": pygame.image.load('images/Main_menu/next.png'),
        "con_zh": pygame.image.load('images/Main_menu/next_zh.png'),
        "restart": pygame.image.load('images/Main_menu/restart.png'),
        "restart_zh": pygame.image.load('images/Main_menu/restart_zh.png'),
    }

    return {
        'menu_frames': menu_frames,
        'cursor_frames': cursor_frames,
        'main_menu_buttons': main_menu_buttons,
        'stay_left': stay_left,
        'stay_right': stay_right,
    }
