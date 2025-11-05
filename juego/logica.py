import cv2
import random
from juego.items import Ship, Bullet, generate_enemies, check_collision, check_ship_enemy_collision
from juego.extra import *


# ------------------------------------------------------------------------------
# Clase de alto nivel que encapsula TODA la lógica del videojuego.
# Se invoca una vez por frame desde el bucle principal (main.py).
# Mantiene y actualiza el estado global del juego:
#   - nave del jugador
#   - enemigos activos
#   - balas en vuelo
#   - marcador, vidas y highscore
#   - estado de fin de partida
#
# ------------------------------------------------------------------------------
class Game:
    def __init__(self, frame_width=640, frame_height=480):
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.ship = Ship(x=frame_width // 2, y=frame_height - 60)
        self.enemies = generate_enemies(5, frame_width)
        self.bullets = []

        self.score = 0
        self.lives = 3
        self.highscore = load_highscore()

        self.game_over = False

        self.fps_counter = FPSCounter()

    # --------------------------------------------------------------------------
    # Este método se ejecuta 1 vez por cada frame de cámara recibido.
    #
    # Aquí ocurre "el juego" en sí:
    #   - se mueve la nave (según posición del rostro detectado)
    #   - se dispara cuando hay sonrisa
    #   - se actualiza física de enemigos y balas
    #   - se evalúan colisiones
    #   - se dibujan sprites, HUD y efectos visuales
    # --------------------------------------------------------------------------
    def update(self, frame, face_data):

        if self.game_over:
            return show_game_over(frame, self.score, self.highscore)

        self.ship.move_to(face_data.get("face_middle"), self.frame_width)
        self.ship.update_cooldown()

        if face_data.get("smiling") and self.ship.can_shoot():
            bullet_x = self.ship.x + self.ship.width // 2
            bullet_y = self.ship.y
            self.bullets.append(Bullet(bullet_x, bullet_y))

        for enemy in self.enemies:
            enemy.move(self.frame_height)
        for bullet in self.bullets:
            bullet.move()

        self.bullets = [b for b in self.bullets if b.active]
        self.enemies = [e for e in self.enemies if e.alive]

        if len(self.enemies) < 5:
            self.enemies += generate_enemies(5 - len(self.enemies), self.frame_width)

        for bullet in self.bullets:
            for enemy in self.enemies:
                if check_collision(bullet, enemy):
                    bullet.active = False
                    enemy.alive = False
                    self.score += 1
                    frame = apply_flash(frame, 0.4)
                    break

        """
        for enemy in self.enemies:
            if enemy.y + enemy.size >= self.ship.y:
                self.lives -= 1
                enemy.alive = False
                if self.lives <= 0:
                    self.game_over = True
        """

        for enemy in self.enemies:
            if enemy.alive and check_ship_enemy_collision(self.ship, enemy):
                self.lives -= 1
                enemy.alive = False

                if self.lives <= 0:
                    self.game_over = True


        self.ship.draw(frame)
        for enemy in self.enemies:
            enemy.draw(frame)
        for bullet in self.bullets:
            bullet.draw(frame)

        draw_score(frame, self.score, self.highscore)
        draw_lives(frame, self.lives)

        fps_value = self.fps_counter.update()
        self.fps_counter.draw(frame)
        # draw_debug_info(frame, face_data)

        if self.score > self.highscore:
            self.highscore = self.score
            save_highscore(self.highscore)

        return frame
