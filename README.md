# Navy - mini Space Invaders con OpenCV

**Navy** es un videojuego 2D en tiempo real inspirado en *Space Invaders* en el cual el jugador controla la nave completamente mediante **gestos faciales detectados por cámara web** (webcam).  
No se utiliza teclado ni ratón para jugar.

Este proyecto ha sido desarrollado para la asignatura **Imagen Digital** y su objetivo es demostrar la capacidad de usar **procesamiento de imagen en tiempo real** con **OpenCV** aplicado a un contexto lúdico / interactivo.

---

## 1). Tecnologías utilizadas
- **OpenCV (cv2)** -> captura webcam, Haar cascades, dibujado, render 
- **NumPy** -> cálculos de distancia y normalizaciones 
- **Python 3.12** -> base del proyecto 

TODA la lógica del juego, render, UI, HUD y sprites se realizan **dentro de OpenCV**.

---

## 2). Resumen de funcionamiento


El funcionamiento de Navy se basa en un ciclo principal de ejecución que se repite continuamente mientras el juego está activo. 

Al iniciar la aplicación se abre la cámara web del usuario, se cargan los clasificadores Haar necesarios (detección de cara y detección de sonrisa) y se inicializan los objetos del juego: la nave del jugador, las listas de enemigos, las listas de balas y la puntuación acumulada junto con el “highscore” almacenado en disco. 

Cada fotograma capturado por la cámara se convierte primero a escala de grises y se procesa mediante OpenCV para localizar el rostro dentro de la imagen. Esta detección se realiza sobre el frame actual o cada varios frames para mantener una tasa de refresco estable. 

Si se detecta una cara se calcula la coordenada horizontal del centro del rostro y esa coordenada se utiliza para posicionar la nave del jugador en pantalla. Es decir, mover la cabeza físicamente hacia la izquierda o hacia la derecha desplaza la nave del juego en esa misma dirección. 

Dentro de esa misma región donde se detecta la cara se ejecuta el segundo clasificador encargado de identificar la sonrisa del jugador. Si la sonrisa se detecta de forma consistente se activa el disparo: se crea un objeto “bala” asociado a la nave, que avanza visualmente hacia arriba en el frame. Mientras tanto, el juego genera enemigos que caen desde la parte superior de la pantalla hacia abajo con una velocidad creciente o constante según la lógica configurada. 

Cada enemigo se dibuja sobre el frame utilizando OpenCV, al igual que la nave y las balas, de modo que todo el juego es renderizado usando únicamente primitivas de dibujo 2D de OpenCV, sin emplear frameworks externos de videojuegos. El movimiento de los enemigos ocurre continuamente, al igual que el avance de cada bala creada. Las balas se destruyen cuando salen del área visible de juego o cuando colisionan con algún enemigo.

Cuando una bala impacta un enemigo, éste se elimina y la puntuación del jugador se incrementa. Además se realizan comprobaciones de colisión entre la nave y los enemigos; si un enemigo llega a tocar la nave (o llega a un nivel inferior de la pantalla que equivalga a esa colisión lógica) la partida termina y se muestra la puntuación final. 

Si esa puntuación supera el valor almacenado previamente en el archivo `puntuacion.txt`, entonces ese valor se actualiza y se guarda de nuevo para partidas futuras. Todo este flujo se ejecuta en tiempo real a medida que OpenCV va capturando cada imagen y renderizando simultáneamente la interfaz del juego mediante rectángulos, textos y sprites opcionales. El usuario únicamente necesita moverse y sonreír para jugar. 

No se requiere teclado ni ratón, lo cual demuestra de forma directa cómo la visión por computador puede sustituir dispositivos de entrada tradicionales y convertirse en la interfaz de control principal en un sistema interactivo funcional.



---

## 3). Arquitectura del proyecto

| Archivo | Función |
|---|---|
| `main.py` | game loop principal donde se inicializa el juego y se van capturando los fotogramas |
| `/juego/deteccion_cara.py` | detección de cara y sonrisa (Haar cascades) |
| `/juego/items.py` | clases del juego (Nave, Bala, Enemigo) y funciones de colisión |
| `/juego/logica.py` | se establece todo la lógica del juego. Se establece que es lo que se modifica por cada frame que se captura |
| `/juego/extra.py` | utilidades: debug, puntuaciones, FPS |
| `/datos/puntuacion.txt` | almacenar la puntuación persistente |

---

## 4). Clases principales

El juego se base en 3 pilares fundamentales que son los objeto con los que se puede realizar el juego. 

### `Ship`
Clase para crear el objeto Ship.
Este objeto tendra una serie de atributo definidos: coordenadas, ancho, cooldown para disparar, etc.
Todos estos atributos son totlamente customizables por el usuario.
Además se inclyen 4 métodos: dibujar la nave, mover la nave, comporbar el cooldown y si puede disparar

### `Bullet`
Clase para crear el objeto bullet.
Este objeto tiene un serie de atributos para definir sus coordenadas, velocidad de movimiento, tamaño, etc.
A su vez, estos atributos también son totalmente customizables.

### `Enemy`
Clase para crear el objeto Enemy.
Este objeto tambien tiene sus propios atributos que pueden ser modificados a gusto del usuario.

Ademas de los 3 objetos principales, también se encuentra la clase FaceDetector utilizada para poder realizar las funcionalidades de la detección de la cara y la sonrisa.

### `FaceDetector`
usa Haar Cascades para:

- encontrar rostro
- detectar sonrisa

Para ello, se usa un diccionaria para almacenar los siguientes datos:

- smiling -> True si detecta sonrisa y False en caso contrario.
- face_middle -> se establece la coordenada x del centro de la cara detectada

---

## 5). Colisiones

La detección de colisiones se implementa de forma eficiente y suficiente para sprites 2D:

- Colisiones basadas en **bounding boxes** y **colisión círculo-rectángulo** cuando el enemigo se representa como un círculo.
- No se usan contornos (`cv2.findContours`) ni matching de formas porque:
  - son más costosos computacionalmente,
  - no aportan mejora significativa para sprites simples,
  - y empeorarían los FPS en tiempo real.

Se utiliza además un **padding** interno (hitbox reducida) para que la colisión coincida mejor con la percepción visual del jugador.

---

## 6). Instalación

Lo primero que se debe realizar es descargar el código disponible en el repositorio o en su defecto realizar un clonado del repositorio.
```bash
git clone https://github.com/SergioDP2003/Proyecto_ID_Navy.git
```

El siguiente paso es instalar todas las lbrerías necesarias para el proyecto.
```bash
pip install opencv-python numpy
```

Por último, solamente quedaría ejecutar el código del archivo `main.py`.
```bash
python main.py
```


