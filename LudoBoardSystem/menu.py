import math
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from helpers import smooth_approach, draw_shadowed_blit


class MainMenu:
    def __init__(self, assets):
        self.assets = assets
        self.button_current_scale = 1.0
        self.button_alpha = 255

        self.play_button = assets.play_button
        self.button_base_w, self.button_base_h = self.play_button.get_size()

        self.btn_center = (SCREEN_WIDTH // 2, 505)

    def get_button_rect(self):
        btn_draw_w = int(self.button_base_w * self.button_current_scale)
        btn_draw_h = int(self.button_base_h * self.button_current_scale)
        rect = pygame.Rect(0, 0, btn_draw_w, btn_draw_h)
        rect.center = self.btn_center
        return rect

    def update(self, dt, hovering):
        target_scale = 1.03 if hovering else 1.0
        self.button_current_scale = smooth_approach(
            self.button_current_scale, target_scale, 10.0, dt
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

        btn_w = int(self.button_base_w * self.button_current_scale)
        btn_h = int(self.button_base_h * self.button_current_scale)
        scaled_btn = pygame.transform.scale(self.play_button, (btn_w, btn_h))
        scaled_btn.set_alpha(self.button_alpha)

        draw_shadowed_blit(
            surface,
            scaled_btn,
            self.btn_center,
            shadow_offset=(0, 3),
            shadow_alpha=55
        )