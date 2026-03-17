import pygame
from os import system

def safe_load(path, size=None, alpha=True, fallback_color=(180, 180, 180, 255)):
    try:
        img = pygame.image.load(path)
        img = img.convert_alpha() if alpha else img.convert()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception:
        fallback_size = size if size else (64, 64)
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf


def safe_sound(path, audio_enabled):
    if not audio_enabled:
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


def smooth_approach(current, target, speed, dt):
    t = min(1.0, speed * dt)
    return current + (target - current) * t


def clamp(value, low, high):
    return max(low, min(value, high))


def draw_shadowed_blit(target, surf, center_pos, shadow_offset=(0, 4), shadow_alpha=70):
    shadow = surf.copy()
    shadow.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
    shadow.set_alpha(shadow_alpha)

    shadow_rect = shadow.get_rect(
        center=(int(center_pos[0] + shadow_offset[0]), int(center_pos[1] + shadow_offset[1]))
    )
    target.blit(shadow, shadow_rect)

    rect = surf.get_rect(center=(int(center_pos[0]), int(center_pos[1])))
    target.blit(surf, rect)
    return rect

def play_wav(filename):
    command = f"afplay {filename}&"
    system(command)