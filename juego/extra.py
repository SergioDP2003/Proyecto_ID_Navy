import cv2
import os
import numpy as np
import time

# Contador de FPS del juego
class FPSCounter:
    def __init__(self):
        self.prev_time = time.time()
        self.fps = 0
        self.counter = 0
        self.last_update = time.time()

    def update(self):
        self.counter += 1
        current_time = time.time()
        if current_time - self.last_update >= 0.5:
            elapsed = current_time - self.prev_time
            self.fps = self.counter / elapsed if elapsed > 0 else 0
            self.prev_time = current_time
            self.last_update = current_time
            self.counter = 0
        return self.fps

    def draw(self, frame):
        text = f"FPS: {self.fps:.1f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.7
        thickness = 2

        (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)

        # calcular coordenadas para abajo a la derecha
        x = frame.shape[1] - text_w - 10     # 10px desde el lado derecho
        y = frame.shape[0] - 10              # 10px desde el borde inferior

        cv2.putText(frame, text, (x, y), font, scale, (255, 255, 0), thickness)


# Da informacion de la detccion de la cara, la posicion, si detecta sonrisa
""""
def draw_debug_info(frame, face_data):
    text = f"Face X: {face_data.get('face_x', '-')}"
    text += f" | Smile: {face_data.get('smiling', False)}"
    text += f" | Mouth Open: {face_data.get('mouth_open', False)}"
    cv2.putText(frame, text, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
"""

# Carga el highscore del .txt 
def load_highscore(path="datos/puntuacion.txt"):
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r") as f:
            return int(f.read().strip())
    except ValueError:
        return 0

# Guarda el highscore en el .txt
def save_highscore(score, path="datos/puntuacion.txt"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(str(score))

# Pinta el marcador en la pantalla
def draw_score(frame, score, highscore):
    cv2.putText(frame, f"Score: {score}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, f"Highscore: {highscore}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# Pinta las vidas en la pantalla
def draw_lives(frame, lives):
    for i in range(lives):
        cv2.circle(frame, (frame.shape[1] - 30 - i * 30, 30), 10, (0, 0, 255), -1)

# Dibuja una pantalla donde se establece el fin de juego con el marcador final
def show_game_over(frame, score, highscore):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    text = "GAME OVER"
    text2 = f"Score: {score} | Highscore: {highscore}"
    cv2.putText(frame, text, (frame.shape[1] // 2 - 150, frame.shape[0] // 2 - 20), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 255), 3)
    cv2.putText(frame, text2, (frame.shape[1] // 2 - 200, frame.shape[0] // 2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, "Presiona Q para salir", (frame.shape[1] // 2 - 160, frame.shape[0] // 2 + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    return frame

# Representa un metodo que aplica un efecto al matar un enemigo
def apply_flash(frame, intensity=0.3):
    flash = np.full_like(frame, 255)
    return cv2.addWeighted(flash, intensity, frame, 1 - intensity, 0)
