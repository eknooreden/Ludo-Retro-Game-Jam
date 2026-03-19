import math
import pygame

from LudoBoardSystem.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from LudoBoardSystem.helpers import smooth_approach, draw_shadowed_blit

class MainMenu:
    def __init__(self, assets):
        self.assets = assets

        self.play_button = assets.play_button
        self.adventure_button = assets.adventure_button

        self.play_button_scale = 1.0
        self.adventure_button_scale = 1.0
        self.button_alpha = 255

        self.play_base_w, self.play_base_h = self.play_button.get_size()
        self.adventure_base_w, self.adventure_base_h = self.adventure_button.get_size()

        self.play_center = (SCREEN_WIDTH // 2, 405)
        self.adventure_center = (SCREEN_WIDTH // 2, 535)

    def get_play_button_rect(self):
        w = int(self.play_base_w * self.play_button_scale)
        h = int(self.play_base_h * self.play_button_scale)
        rect = pygame.Rect(0, 0, w, h)
        rect.center = self.play_center
        return rect

    def get_adventure_button_rect(self):
        w = int(self.adventure_base_w * self.adventure_button_scale)
        h = int(self.adventure_base_h * self.adventure_button_scale)
        rect = pygame.Rect(0, 0, w, h)
        rect.center = self.adventure_center
        return rect

    def update(self, dt, hovering_play, hovering_adventure):
        play_target = 1.03 if hovering_play else 1.0
        adventure_target = 1.03 if hovering_adventure else 1.0

        self.play_button_scale = smooth_approach(
            self.play_button_scale, play_target, 10.0, dt
        )
        self.adventure_button_scale = smooth_approach(
            self.adventure_button_scale, adventure_target, 10.0, dt
        )

    def draw(self, surface, time_ms, art_offset_x, art_offset_y):
        art = self.assets.background_art
        art_w, art_h = art.get_size()

        art_draw_x = (SCREEN_WIDTH - art_w) // 2 + int(art_offset_x)
        art_draw_y = (SCREEN_HEIGHT - art_h) // 2 + int(art_offset_y)
        surface.blit(art, (art_draw_x, art_draw_y))

        title_y_float = math.sin(time_ms * 0.0015) * 2
        title_center = (SCREEN_WIDTH // 2, 150 + title_y_float)

        draw_shadowed_blit(
            surface,
            self.assets.game_title,
            title_center,
            shadow_offset=(0, 6),
            shadow_alpha=75
        )

        play_w = int(self.play_base_w * self.play_button_scale)
        play_h = int(self.play_base_h * self.play_button_scale)
        scaled_play = pygame.transform.scale(self.play_button, (play_w, play_h))
        scaled_play.set_alpha(self.button_alpha)

        draw_shadowed_blit(
            surface,
            scaled_play,
            self.play_center,
            shadow_offset=(0, 3),
            shadow_alpha=55
        )

        adv_w = int(self.adventure_base_w * self.adventure_button_scale)
        adv_h = int(self.adventure_base_h * self.adventure_button_scale)
        scaled_adventure = pygame.transform.scale(self.adventure_button, (adv_w, adv_h))
        scaled_adventure.set_alpha(self.button_alpha)

        draw_shadowed_blit(
            surface,
            scaled_adventure,
            self.adventure_center,
            shadow_offset=(0, 3),
            shadow_alpha=55
        )