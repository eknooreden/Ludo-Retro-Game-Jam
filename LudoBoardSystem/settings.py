SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

PLAYER_MARGIN = 30
STUD = 5
PLAYER_BASE_SIZE = (9 * STUD, 9 * STUD)
BLOCK_SIZE = 17 * STUD

BASE_BG_PARALLAX_STRENGTH = 18
ART_PARALLAX_STRENGTH = 15

BG_ZOOM = 1.30
ART_ZOOM = 1.06

PLAY_BUTTON_SCALE = 6
TITLE_SIZE = (470, 313)
DICE_SIZE = (80, 80)

BOARD_GRID_SIZE = 15
BOARD_SIZE = (710, 710)
LUDO_BOARD_PATH = "assets/game/ludo_board_assets/ludo_board.png"

MENU_BG_PATH = "assets/backgrounds/blue_bg.png"
GAME_BG_CHOICES = [
    "assets/backgrounds/red_bg.png",
    "assets/backgrounds/blue_bg.png",
    "assets/backgrounds/yellow_bg.png",
    "assets/backgrounds/green_bg.png",
]

BOARD_INSET_X = 25
BOARD_INSET_Y = 25

DICE_PATH = "assets/game/dice"
PLAY_BUTTON_PATH = "assets/main_menu/play_button.png"
TITLE_PATH = "assets/main_menu/title.png"
MENU_ART_PATH = "assets/main_menu/background_art.png"

MOVE_SOUND_PATH = "assets/sounds/move.wav"
DICE_ROLL_SOUND_PATH = "assets/sounds/dice_roll.wav"
DICE_FINISH_SOUND_PATH = "assets/sounds/dice_finish.wav"

MAIN_PATH = [

    (6,13),(6,12),(6,11),(6,10),(6,9),

    (5,8),(4,8),(3,8),(2,8),(1,8),(0,8),

    (0,7),(0,6),

    (1,6),(2,6),(3,6),(4,6),(5,6),

    (6,5),(6,4),(6,3),(6,2),(6,1),(6,0),

    (7,0),

    (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),

    (9,6),(10,6),(11,6),(12,6),(13,6),(14,6),

    (14,7),(14,8),

    (13,8),(12,8),(11,8),(10,8),(9,8),

    (8,9),(8,10),(8,11),(8,12),(8,13),(8,14),

    (7,14),

    (6,14)
]

START_INDEX = {
    "blue": 13,
    "red": 26,
    "green": 39,
    "yellow": 52,
}

HOME_STRETCH = {
    "red": [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)],
    "green": [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7)],
    "yellow": [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8)],
    "blue": [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)],
}

HOME_POSITIONS = {
    "blue": [(1.6, 1), (4, 2), (2, 4), (4, 4)],
    "red": [(10, 2), (12, 2), (10, 4), (12, 4)],
    "yellow": [(2, 10), (4, 10), (2, 12), (4, 12)],
    "green": [(10, 10), (12, 10), (10, 12), (12, 12)],
}

HOME_DRAW_OFFSETS = [
    (-7.5, -6.5),
    (7.5, -6.5),
    (-7.5, 6.5),
    (7.5, 6.5),
]

SAFE_ZONES = {
    (6, 1),
    (13, 6),
    (8, 13),
    (1, 8),
}

COLOR_KEYS = ["red", "green", "yellow", "blue"]

BOARD_SIZE = (710, 710)