import cv2


# ------------------------------------------------------------------------------
# Encapsula la detección facial basada en haarcascades. Esta clase se utiliza
# para extraer dos parámetros fundamentales para el control del videojuego:
#   - La posición horizontal del rostro 
#   - La presencia de sonrisa 
#
# La detección se realiza sobre una imagen en escala de grises (gray), pero se
# dibujan anotaciones sobre el frame original en color para visualizar feedback.
# ------------------------------------------------------------------------------
class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

    def detect_face_smile(self, gray, frame):
        # Diccionario para guardar los datos de la detección
        data = {
            "face_middle": None,
            "smiling": False,
        }

        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

            # Se introducen la coordenada del centro de la cara en el diccionario
            data["face_middle"] = x + w // 2

            face_gray = gray[y:y + h, x:x + w]
            face_color = frame[y:y + h, x:x + w]

            smiles = self.smile_cascade.detectMultiScale(face_gray,scaleFactor=1.9,minNeighbors=20,minSize=(30, 30))

            if len(smiles) > 0:
                # Se establece que se ha detectado la sonrisa
                data["smiling"] = True

                (sx, sy, sw, sh) = smiles[0]
                
                cv2.rectangle(face_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)

            break

        return data
