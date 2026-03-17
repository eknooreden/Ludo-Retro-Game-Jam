import os
import random as rdm
import pygame

from settings import *
from helpers import safe_load, safe_sound

PLAYER_CHOICES = [
    "assets/game/player/player_red.png",
    "assets/game/player/player_green.png",
    "assets/game/player/player_blue.png",
    "assets/game/player/player_yellow.png",
]
player_color = rdm.choice(PLAYER_CHOICES)

class Assets:
    def __init__(self, audio_enabled):
        self.audio_enabled = audio_enabled

        self.move_sound = safe_sound(MOVE_SOUND_PATH, audio_enabled)
        self.dice_roll_snd = safe_sound(DICE_ROLL_SOUND_PATH, audio_enabled)
        self.dice_finish_snd = safe_sound(DICE_FINISH_SOUND_PATH, audio_enabled)

        self.dice_images = self.load_dice()
        self.menu_bg = self.load_menu_bg()
        self.game_bg = None

        self.play_button = self.load_play_button()
        self.game_title = safe_load(TITLE_PATH, size=TITLE_SIZE, alpha=True)

        art_w = int(SCREEN_WIDTH * ART_ZOOM)
        art_h = int(SCREEN_HEIGHT * ART_ZOOM)
        self.background_art = safe_load(
            MENU_ART_PATH,
            size=(art_w, art_h),
            alpha=True
        )
        self.background_art.set_alpha(110)

        self.player_src = safe_load(
            player_color,
            size=PLAYER_BASE_SIZE,
            alpha=True
        )

    def load_dice(self):
        dice_images = []
        for i in range(1, 7):
            img_path = f"{DICE_PATH}/{i}_dice.png"
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, DICE_SIZE)
                dice_images.append(img)
            else:
                fallback = pygame.Surface(DICE_SIZE, pygame.SRCALPHA)
                fallback.fill(GRAY)
                dice_images.append(fallback)
        return dice_images

    def load_menu_bg(self):
        bg_w = int(SCREEN_WIDTH * BG_ZOOM)
        bg_h = int(SCREEN_HEIGHT * BG_ZOOM)
        return safe_load(
            MENU_BG_PATH,
            size=(bg_w, bg_h),
            alpha=False,
            fallback_color=(100, 100, 100, 255)
        )

    def load_random_game_bg(self):
        bg_w = int(SCREEN_WIDTH * BG_ZOOM)
        bg_h = int(SCREEN_HEIGHT * BG_ZOOM)
        chosen = rdm.choice(GAME_BG_CHOICES)
        self.game_bg = safe_load(
            chosen,
            size=(bg_w, bg_h),
            alpha=False,
            fallback_color=(100, 100, 100, 255)
        )

    def load_play_button(self):
        src = safe_load(PLAY_BUTTON_PATH, alpha=True)
        w, h = src.get_size()
        return pygame.transform.scale(
            src,
            (int(w * PLAY_BUTTON_SCALE), int(h * PLAY_BUTTON_SCALE))
        )