import cv2
import numpy as np
import random

# ------------------------------------------------------------------------------
# Representa la "nave" controlada por el jugador. La nave se renderiza como un
# rectángulo y su posición horizontal depende del centro estimado del rostro
# detectado en la cámara. La nave es quien dispara balas hacia los enemigos.
# ------------------------------------------------------------------------------    
class Ship:
    def __init__(self, x, y, width=60, height=20, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 10
        self.cooldown = 0  

    # Mueve la nave horizontalmente alineando su centro con el punto target_x
    def move_to(self, target_x, frame_width):
        if target_x is None:
            return
        self.x = int(np.clip(target_x - self.width // 2, 0, frame_width - self.width))

    # Renderiza la nave como un rectángulo sólido
    def draw(self, frame):
        cv2.rectangle(frame,(self.x, self.y),(self.x + self.width, self.y + self.height),self.color,-1)

    # Permite disparar solo si el cooldown está en cero.
    def can_shoot(self):
        if self.cooldown <= 0:
            self.cooldown = 10  
            return True
        return False

    # Reduce el cooldown gradualmente frame a frame
    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1


# ------------------------------------------------------------------------------
# Entidad enemigo representada como un círculo. Entra en pantalla desde la zona
# superior y avanza verticalmente hacia abajo. Si sale de la pantalla, se marca
# como no vivo y podrá ser eliminado.
# ------------------------------------------------------------------------------
class Enemy:
    def __init__(self, x, y, size=30, color=(0, 0, 255), speed=3):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.alive = True

    # Avanza verticalmente. Si supera el límite inferior, queda fuera de juego
    def move(self, frame_height):
        self.y += self.speed
        if self.y > frame_height:
            self.alive = False

    def draw(self, frame):
        cv2.circle(frame,(int(self.x + self.size // 2), int(self.y + self.size // 2)),self.size // 2,self.color,-1)


# ------------------------------------------------------------------------------
# Proyectiles disparados por la nave. Suben desde la posición de la nave hacia
# la zona superior. Su vida finaliza automáticamente si salen del frame.
# ------------------------------------------------------------------------------
class Bullet:
    def __init__(self, x, y, radius=5, color=(0, 255, 0), speed=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.active = True

    def move(self):
        self.y -= self.speed
        if self.y < 0:
            self.active = False

    def draw(self, frame):
        cv2.circle(frame,(int(self.x), int(self.y)),self.radius,self.color,-1)


# ------------------------------------------------------------------------------
# Generación aleatoria de enemigos en el borde superior
# ------------------------------------------------------------------------------
def generate_enemies(num, frame_width):
    enemies = []
    for _ in range(num):
        x = random.randint(0, frame_width - 40)
        y = random.randint(-150, -40)
        enemies.append(Enemy(x, y))
    return enemies


# ------------------------------------------------------------------------------
# Colisión bala vs enemigo: aproximación por distancia entre centros
# ------------------------------------------------------------------------------
def check_collision(bullet, enemy):
    dx = (bullet.x - enemy.x)
    dy = (bullet.y - enemy.y)
    distance = np.sqrt(dx ** 2 + dy ** 2)
    return distance < enemy.size

# ------------------------------------------------------------------------------
# Colisión rectángulo (nave) vs círculo (enemigo)
# Se usa el método estándar de "punto más cercano" del rectángulo respecto al
# centro del círculo → es más robusto que bounding boxes puros.
# ------------------------------------------------------------------------------
def circle_rect_collision(circle_x, circle_y, radius, rect_x, rect_y, rect_w, rect_h):

    # punto más cercano del rect al centro del círculo
    closest_x = np.clip(circle_x, rect_x, rect_x + rect_w)
    closest_y = np.clip(circle_y, rect_y, rect_y + rect_h)

    dx = circle_x - closest_x
    dy = circle_y - closest_y
    return (dx * dx + dy * dy) <= (radius * radius)


def check_ship_enemy_collision(ship, enemy, pad_ship=12):
    # hitbox reducida de la nave (padding interno)
    rx = ship.x + pad_ship
    ry = ship.y + pad_ship
    rw = max(1, ship.width - 2 * pad_ship)
    rh = max(1, ship.height - 2 * pad_ship)

    # centro y radio del enemigo (enemy.size es diámetro en tu código)
    cx = enemy.x + enemy.size / 2.0
    cy = enemy.y + enemy.size / 2.0
    radius = enemy.size / 2.0

    return circle_rect_collision(cx, cy, radius, rx, ry, rw, rh)


