import math
import random as rdm
import pygame

from LudoBoardSystem.settings import *
from LudoBoardSystem.helpers import clamp, smooth_approach, draw_shadowed_blit

class Gameplay:
    def __init__(self, assets):
        self.assets = assets

        self.board_image = pygame.transform.scale(
            pygame.image.load(LUDO_BOARD_PATH).convert(),
            BOARD_SIZE
        )
        self.board_rect = self.board_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.grid_left = self.board_rect.left + BOARD_INSET_X
        self.grid_top = self.board_rect.top + BOARD_INSET_Y
        self.grid_width = self.board_rect.width - (BOARD_INSET_X * 2)
        self.grid_height = self.board_rect.height - (BOARD_INSET_Y * 2)

        self.cell_size = self.grid_width / BOARD_GRID_SIZE

        self.player_color = rdm.choice(COLOR_KEYS)

        color_to_asset = {
            "red": "assets/game/player/player_red.png",
            "green": "assets/game/player/player_green.png",
            "yellow": "assets/game/player/player_yellow.png",
            "blue": "assets/game/player/player_blue.png",
        }

        self.assets.player_src = pygame.transform.scale(
            pygame.image.load(color_to_asset[self.player_color]).convert_alpha(),
            PLAYER_BASE_SIZE
        )

        self.player_current_scale = 1.0
        self.pawn_is_selected = False

        self.selected_pawn_index = 0
        self.pawns = []
        self.move_queue = []

        self.speed = 250
        self.particles = []

        self.dice_rolling = False
        self.dice_roll_duration = 1.2
        self.dice_timer = 0.0
        self.dice_frame_timer = 0.0
        self.dice_frame_index = 0
        self.final_dice_val = 1
        self.target_dir = (0, 0)
        self.show_dice = False

        self._create_pawns()
        self._sync_selected_pawn_draw_data()

    def _create_pawns(self):
        self.pawns.clear()
        for home_grid in HOME_POSITIONS[self.player_color]:
            cx, cy = self.grid_to_center(*home_grid)
            pawn_rect = self.assets.player_src.get_rect(center=(int(cx), int(cy)))
            self.pawns.append({
                "home_grid": home_grid,
                "grid_pos": home_grid,
                "x": cx,
                "y": cy,
                "draw_rect": pawn_rect.copy(),
                "rect": pawn_rect.copy(),
                "progress": -1,
                "in_home": True,
                "finished": False,
                "current_scale": 1.0,
                "bounce": 0.0,
            })

    def grid_to_topleft(self, col, row):
        x = self.grid_left + col * self.cell_size
        y = self.grid_top + row * self.cell_size
        return x, y

    def grid_to_center(self, col, row):
        x = self.grid_left + (col + 0.5) * self.cell_size
        y = self.grid_top + (row + 0.5) * self.cell_size
        return x + 1, y

    def get_track_pos(self, color, progress):
        if 0 <= progress <= 51:
            idx = (START_INDEX[color] + progress) % len(MAIN_PATH)
            return MAIN_PATH[idx]
        if 52 <= progress <= 57:
            return HOME_STRETCH[color][progress - 52]
        return (7, 7)

    def _sync_selected_pawn_draw_data(self):
        pawn = self.pawns[self.selected_pawn_index]
        self.current_x = pawn["x"] - PLAYER_BASE_SIZE[0] / 2
        self.current_y = pawn["y"] - PLAYER_BASE_SIZE[1] / 2
        self.player_rect = pawn["rect"].copy()
        self.player_draw_rect = pawn["draw_rect"].copy()

    def get_selected_pawn(self):
        return self.pawns[self.selected_pawn_index]

    def any_pawn_moving(self):
        return len(self.move_queue) > 0

    def can_move_selected_pawn(self, dice_val):
        pawn = self.get_selected_pawn()
        if pawn["finished"]:
            return False
        if pawn["in_home"]:
            return dice_val == 6
        return pawn["progress"] + dice_val <= 57

    def build_move_queue_for_selected_pawn(self):
        pawn = self.get_selected_pawn()
        self.move_queue.clear()

        if pawn["in_home"]:
            if self.final_dice_val != 6:
                return
            target_grid = self.get_track_pos(self.player_color, 0)
            tx, ty = self.grid_to_center(*target_grid)
            self.move_queue.append((tx, ty, target_grid))
            return

        new_progress = pawn["progress"] + self.final_dice_val
        if new_progress > 57:
            return

        for step in range(1, self.final_dice_val + 1):
            step_progress = pawn["progress"] + step
            target_grid = self.get_track_pos(self.player_color, step_progress)
            tx, ty = self.grid_to_center(*target_grid)
            self.move_queue.append((tx, ty, target_grid))

    def select_pawn_at_mouse(self, mouse_pos):
        if self.any_pawn_moving() or self.dice_rolling:
            return False

        for i, pawn in enumerate(self.pawns):
            if pawn["draw_rect"].collidepoint(mouse_pos):
                self.selected_pawn_index = i
                self.pawn_is_selected = True
                self._sync_selected_pawn_draw_data()
                return True

        self.pawn_is_selected = False
        return False

    def start_dice_roll(self, mouse_pos):
        if self.any_pawn_moving():
            return

        self.dice_rolling = True
        self.show_dice = True
        self.dice_timer = self.dice_roll_duration
        self.dice_frame_timer = 0.0
        self.target_dir = (
            mouse_pos[0] - self.player_draw_rect.centerx,
            mouse_pos[1] - self.player_draw_rect.centery,
        )

        if self.assets.dice_roll_snd:
            self.assets.dice_roll_snd.play()

    def update_dice(self, dt):
        if not self.dice_rolling:
            return

        self.dice_timer -= dt
        self.dice_frame_timer += dt

        if self.dice_frame_timer >= 0.12:
            self.dice_frame_timer = 0.0
            self.dice_frame_index = (self.dice_frame_index + 1) % 6

        if self.dice_timer <= 0:
            self.dice_rolling = False
            self.final_dice_val = rdm.randint(1, 6)
            self.dice_frame_index = self.final_dice_val - 1

            if self.assets.dice_finish_snd:
                self.assets.dice_finish_snd.play()

            self.build_move_queue_for_selected_pawn()

    def update_particles(self, dt):
        for p_data in self.particles[:]:
            p_data[0][0] += p_data[1][0] * dt
            p_data[0][1] += p_data[1][1] * dt
            p_data[2] -= 600 * dt

            if p_data[2] <= 0:
                self.particles.remove(p_data)

    def update_player(self, dt, mouse_pos):
        for i, pawn in enumerate(self.pawns):
            is_selected = i == self.selected_pawn_index
            is_hovering = pawn["draw_rect"].collidepoint(mouse_pos)

            if is_selected and self.any_pawn_moving():
                tx, ty, target_grid = self.move_queue[0]
                dx = tx - pawn["x"]
                dy = ty - pawn["y"]
                curr_d = math.hypot(dx, dy)

                prog = 1.0 - (curr_d / self.cell_size if self.cell_size else 0)
                prog = clamp(prog, 0.0, 1.0)

                pawn["bounce"] = math.sin(prog * math.pi) * 10
                step = self.speed * dt

                if curr_d <= step:
                    pawn["x"], pawn["y"] = tx, ty
                    pawn["grid_pos"] = target_grid
                    self.move_queue.pop(0)

                    if self.assets.move_sound:
                        self.assets.move_sound.play()

                    for _ in range(8):
                        self.particles.append([
                            [pawn["x"], pawn["y"] + PLAYER_BASE_SIZE[1] / 3],
                            [rdm.uniform(-80, 80), rdm.uniform(-40, 10)],
                            255
                        ])

                    if not self.move_queue:
                        if pawn["in_home"]:
                            pawn["in_home"] = False
                            pawn["progress"] = 0
                        else:
                            pawn["progress"] += self.final_dice_val

                        if pawn["progress"] >= 57:
                            pawn["progress"] = 57
                            pawn["finished"] = True

                else:
                    ang = math.atan2(dy, dx)
                    pawn["x"] += math.cos(ang) * step
                    pawn["y"] += math.sin(ang) * step
            else:
                pawn["bounce"] = smooth_approach(pawn["bounce"], 0.0, 12.0, dt)

            target_scale = 1.0
            if is_selected:
                if self.any_pawn_moving() or self.pawn_is_selected or self.dice_rolling:
                    target_scale = 1.15
                elif is_hovering:
                    target_scale = 1.08
            else:
                if is_hovering and not self.any_pawn_moving() and not self.dice_rolling:
                    target_scale = 1.05

            pawn["current_scale"] = smooth_approach(
                pawn["current_scale"], target_scale, 12.0, dt
            )

            draw_scale = pawn["current_scale"]
            draw_w = max(1, int(PLAYER_BASE_SIZE[0] * draw_scale))
            draw_h = max(1, int(PLAYER_BASE_SIZE[1] * draw_scale))
            scaled_p = pygame.transform.scale(self.assets.player_src, (draw_w, draw_h))

            ox, oy = (0, 0)

            if pawn["in_home"]:
                ox, oy = HOME_DRAW_OFFSETS[i]

            base_center = (int(pawn["x"] + ox), int(pawn["y"] + oy))

            pawn["draw_surface"] = scaled_p
            pawn["draw_rect"] = scaled_p.get_rect(center=base_center)
            pawn["draw_rect"].move_ip(0, int(-pawn["bounce"]))
            pawn["rect"] = pygame.Rect(
                int(pawn["x"] - PLAYER_BASE_SIZE[0] / 2),
                int(pawn["y"] - PLAYER_BASE_SIZE[1] / 2),
                PLAYER_BASE_SIZE[0],
                PLAYER_BASE_SIZE[1]
            )

        self._sync_selected_pawn_draw_data()
        return self.pawns[self.selected_pawn_index]["draw_surface"]

    def draw_particles(self, surface):
        for p_data in self.particles:
            p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(
                p_surf,
                (200, 200, 200, int(clamp(p_data[2], 0, 255))),
                (3, 3),
                3
            )
            surface.blit(p_surf, (p_data[0][0] - 3, p_data[0][1] - 3))

    def draw(self, surface, scaled_player):
        surface.blit(self.board_image, self.board_rect)
        for col, row in MAIN_PATH:
            cx, cy = self.grid_to_center(col, row)
            pygame.draw.circle(surface, (255, 0, 0), (int(cx), int(cy)), 4)
        for col, row in HOME_POSITIONS[self.player_color]:
            cx, cy = self.grid_to_center(col, row)
            pygame.draw.circle(surface, (0, 255, 0), (int(cx), int(cy)), 4)

        for i, pawn in enumerate(self.pawns):
            draw_shadowed_blit(
                surface,
                pawn["draw_surface"],
                pawn["draw_rect"].center,
                shadow_offset=(0, 4),
                shadow_alpha=70
            )

            if i == self.selected_pawn_index and self.pawn_is_selected:
                pygame.draw.circle(
                    surface,
                    (255, 255, 255),
                    pawn["draw_rect"].center,
                    max(pawn["draw_rect"].width, pawn["draw_rect"].height) // 2 + 6,
                    3
                )

        if self.show_dice:
            dice_img = self.assets.dice_images[self.dice_frame_index]
            dice_rect = dice_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            surface.blit(dice_img, dice_rect)