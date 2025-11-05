import cv2
import numpy as np
from juego.deteccion_cara import FaceDetector
from juego.logica import Game

# ------------------------------------------------------------------------------
# Punto de entrada principal del programa.
# Aquí se inicializa el módulo de detección visual (FaceDetector) y la lógica
# de juego (Game). También se abre la cámara y se ejecuta el game loop.
# En cada iteración del bucle se captura un nuevo frame de la webcam, se procesa
# la detección de cara/sonrisa y se actualiza el estado del juego en función
# de la información de visión por computador obtenida.
# ------------------------------------------------------------------------------
def main():
    # Instancia del detector facial (haarcasacde)
    detector = FaceDetector()

    # Instacia de la lógica del juego
    game = Game()

    # Captura de vídeo con la webcam
    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("Error en camara")
        return

    print("Pulsa 'q' para salir")

    while True:
        # Se captura el frame
        ret, frame = camara.read()

        if not ret:
            print("Error en el frame")
            break

        # Se establece el efecto espejo
        frame = cv2.flip(frame, 1)

        # Conversión a escala de grises para la detección
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Se realiza la detección facial
        face_data = detector.detect_face_smile(gray, frame)

        # Actualiza el estado del juego en función de los datos visuales detectados
        # y devuelve el frame renderizado con la nave, enemigos, balas, etc.
        frame = game.update(frame, face_data)

        cv2.imshow("Navy", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camara.release()
    cv2.destroyAllWindows()
    print("Finalizando...")


if __name__ == "__main__":
    main()
