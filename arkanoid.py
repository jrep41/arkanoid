"""
ARKANOID - JUEGO CLÁSICO EN PYTHON
==================================
Un juego completo de Arkanoid desarrollado en Python usando pygame.
Este código está completamente comentado para principiantes en Python.

Autor: GitHub Copilot
Fecha: Julio 2025
"""

# ==========================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================
import pygame  # Librería principal para crear juegos en Python
import sys  # Para funciones del sistema como salir del programa
import math  # Para cálculos matemáticos (ángulos, trigonometría)
import random  # Para generar números aleatorios

# ==========================================
# INICIALIZACIÓN DE PYGAME
# ==========================================
# SIEMPRE necesario antes de usar cualquier función de pygame
pygame.init()

# ==========================================
# CONSTANTES DEL JUEGO
# ==========================================
# Las constantes son valores que NO cambian durante el juego
# Se escriben en MAYÚSCULAS por convención en Python

# Dimensiones de la ventana del juego (en píxeles)
WINDOW_WIDTH = 800  # Ancho de la ventana
WINDOW_HEIGHT = 600  # Alto de la ventana

# Dimensiones de la paleta del jugador
PADDLE_WIDTH = 100  # Ancho de la paleta
PADDLE_HEIGHT = 15  # Alto de la paleta

# Propiedades de la pelota
BALL_SIZE = 15  # Tamaño de la pelota (diámetro)

# Dimensiones de los ladrillos
BRICK_WIDTH = 75  # Ancho de cada ladrillo
BRICK_HEIGHT = 20  # Alto de cada ladrillo
BRICK_ROWS = 8  # Número de filas de ladrillos
BRICK_COLS = 10  # Número de columnas de ladrillos

# Velocidades del juego (píxeles por frame)
PADDLE_SPEED = 8  # Qué tan rápido se mueve la paleta
BALL_SPEED = 2  # Velocidad inicial de la pelota

# ==========================================
# DEFINICIÓN DE COLORES
# ==========================================
# En pygame, los colores se definen como tuplas RGB (Rojo, Verde, Azul)
# Cada valor va de 0 a 255. Ejemplo: (255, 0, 0) = rojo puro

BLACK = (0, 0, 0)  # Negro - ausencia de color
WHITE = (255, 255, 255)  # Blanco - todos los colores al máximo
BLUE = (0, 100, 255)  # Azul personalizado
RED = (255, 0, 0)  # Rojo puro
GREEN = (0, 255, 0)  # Verde puro
YELLOW = (255, 255, 0)  # Amarillo (rojo + verde)
ORANGE = (255, 165, 0)  # Naranja
PURPLE = (128, 0, 128)  # Púrpura
PINK = (255, 192, 203)  # Rosa

# Lista de colores para los ladrillos (se repite el patrón)
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED]


# ==========================================
# CLASE PADDLE (PALETA DEL JUGADOR)
# ==========================================
class Paddle:
    """
    Clase que representa la paleta controlada por el jugador.
    La paleta es el rectángulo azul que se mueve horizontalmente
    para hacer rebotar la pelota y mantenerla en juego.
    """

    def __init__(self, x, y):
        """
        Constructor de la paleta. Se ejecuta cuando creamos una nueva paleta.

        Parámetros:
        - x: posición horizontal inicial (píxeles desde la izquierda)
        - y: posición vertical inicial (píxeles desde arriba)
        """
        self.x = x  # Posición horizontal (esquina izquierda de la paleta)
        self.y = y  # Posición vertical (esquina superior de la paleta)

        # Dimensiones de la paleta (tomadas de las constantes)
        self.width = PADDLE_WIDTH  # Ancho de la paleta
        self.height = PADDLE_HEIGHT  # Alto de la paleta

        # Velocidad de movimiento (píxeles por frame)
        self.speed = PADDLE_SPEED

    def move_left(self):
        """
        Mueve la paleta hacia la izquierda.
        Incluye verificación para no salirse del borde izquierdo de la pantalla.
        """
        # Solo mover si no estamos en el borde izquierdo (x > 0)
        if self.x > 0:
            self.x -= self.speed  # Reducir posición X = mover izquierda

    def move_right(self):
        """
        Mueve la paleta hacia la derecha.
        Incluye verificación para no salirse del borde derecho de la pantalla.
        """
        # Solo mover si no estamos en el borde derecho
        # (posición + ancho) debe ser menor que el ancho total de la ventana
        if self.x < WINDOW_WIDTH - self.width:
            self.x += self.speed  # Aumentar posición X = mover derecha

    def draw(self, screen):
        """
        Dibuja la paleta en la pantalla con efectos visuales.

        Parámetros:
        - screen: superficie de pygame donde dibujar la paleta
        """
        # Dibujar rectángulo principal de la paleta (azul)
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

        # Agregar efecto 3D: línea blanca en la parte superior
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, 3))

    def get_rect(self):
        """
        Devuelve un objeto Rect de pygame que representa la paleta.
        Esto es útil para detectar colisiones con otros objetos.

        Retorna:
        - pygame.Rect: rectángulo con la posición y dimensiones de la paleta
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ==========================================
# CLASE BALL (PELOTA)
# ==========================================
class Ball:
    """
    Clase que representa la pelota del juego.
    La pelota rebota por la pantalla, destruye ladrillos cuando los toca,
    y el jugador debe evitar que caiga fuera de la pantalla.
    """

    def __init__(self, x, y):
        """
        Constructor de la pelota.

        Parámetros:
        - x: posición horizontal inicial (centro de la pelota)
        - y: posición vertical inicial (centro de la pelota)
        """
        self.x = x  # Posición horizontal del centro de la pelota
        self.y = y  # Posición vertical del centro de la pelota

        # Propiedades físicas de la pelota
        self.size = BALL_SIZE  # Diámetro de la pelota
        self.radius = BALL_SIZE // 2  # Radio (la mitad del diámetro)

        # Velocidad de movimiento (píxeles por frame)
        self.speed_x = BALL_SPEED  # Velocidad horizontal (positivo = derecha)
        self.speed_y = -BALL_SPEED  # Velocidad vertical (negativo = arriba)

    def move(self):
        """
        Mueve la pelota según su velocidad actual.
        Este método se llama cada frame para actualizar la posición.
        """
        self.x += self.speed_x  # Nueva posición X = actual + velocidad horizontal
        self.y += self.speed_y  # Nueva posición Y = actual + velocidad vertical

    def bounce_x(self):
        """
        Invierte la dirección horizontal de la pelota.
        Se usa cuando la pelota rebota en paredes laterales.
        """
        self.speed_x = -self.speed_x  # Cambiar signo = cambiar dirección

    def bounce_y(self):
        """
        Invierte la dirección vertical de la pelota.
        Se usa cuando la pelota rebota en paredes, paleta o ladrillos.
        """
        self.speed_y = -self.speed_y  # Cambiar signo = cambiar dirección

    def check_wall_collision(self):
        """
        Verifica si la pelota está tocando las paredes de la pantalla.
        Hace rebotar automáticamente en paredes laterales y superior.

        Retorna:
        - bool: True si la pelota salió por el fondo (perder vida), False si no
        """
        # Verificar colisión con paredes laterales (izquierda y derecha)
        if self.x <= self.radius or self.x >= WINDOW_WIDTH - self.radius:
            self.bounce_x()  # Rebotar horizontalmente

        # Verificar colisión con pared superior
        if self.y <= self.radius:
            self.bounce_y()  # Rebotar verticalmente

        # Verificar si la pelota salió por el fondo (game over)
        if self.y >= WINDOW_HEIGHT:
            return True  # La pelota se perdió
        return False  # La pelota sigue en juego

    def check_paddle_collision(self, paddle):
        """
        Verifica si la pelota está colisionando con la paleta del jugador.
        Implementa física realista basada en dónde golpea la pelota.

        Parámetros:
        - paddle: objeto Paddle para verificar colisión

        Retorna:
        - bool: True si hubo colisión, False si no
        """
        # Crear rectángulos para detección de colisión
        ball_rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.size, self.size
        )
        paddle_rect = paddle.get_rect()

        # Verificar si los rectángulos se superponen
        if ball_rect.colliderect(paddle_rect):
            # Calcular dónde golpeó la pelota en la paleta
            # 0 = extremo izquierdo, 0.5 = centro, 1 = extremo derecho
            hit_pos = (self.x - paddle.x) / paddle.width

            # Convertir posición de golpe a ángulo de rebote
            # hit_pos - 0.5 da un rango de -0.5 a 0.5
            # Multiplicar por π/3 da un ángulo máximo de 60 grados
            angle = (hit_pos - 0.5) * math.pi / 3

            # Calcular velocidad total actual
            speed = math.sqrt(self.speed_x**2 + self.speed_y**2)

            # Aplicar nueva dirección basada en el ángulo calculado
            self.speed_x = speed * math.sin(angle)  # Componente horizontal
            self.speed_y = -abs(
                speed * math.cos(angle)
            )  # Componente vertical (hacia arriba)

            return True  # Hubo colisión
        return False  # No hubo colisión

    def draw(self, screen):
        """
        Dibuja la pelota en la pantalla con efectos visuales.

        Parámetros:
        - screen: superficie de pygame donde dibujar la pelota
        """
        # Dibujar círculo principal (blanco)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

        # Agregar efecto de brillo (círculo más pequeño y azulado)
        pygame.draw.circle(
            screen,
            (200, 200, 255),  # Azul claro
            (int(self.x - 3), int(self.y - 3)),  # Ligeramente desplazado
            self.radius // 3,  # Un tercio del tamaño original
        )

    def get_rect(self):
        """
        Devuelve un rectángulo pygame que representa la pelota.
        Útil para detección de colisiones.

        Retorna:
        - pygame.Rect: rectángulo con posición y dimensiones de la pelota
        """
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.size, self.size
        )


# ==========================================
# CLASE BRICK (LADRILLO)
# ==========================================
class Brick:
    """
    Clase que representa un ladrillo destructible.
    Los ladrillos forman la estructura que el jugador debe destruir
    para completar el nivel. Cada ladrillo tiene un color y posición específicos.
    """

    def __init__(self, x, y, color):
        """
        Constructor del ladrillo.

        Parámetros:
        - x: posición horizontal (esquina izquierda)
        - y: posición vertical (esquina superior)
        - color: color del ladrillo (tupla RGB)
        """
        self.x = x  # Posición horizontal
        self.y = y  # Posición vertical

        # Dimensiones del ladrillo (tomadas de las constantes)
        self.width = BRICK_WIDTH  # Ancho del ladrillo
        self.height = BRICK_HEIGHT  # Alto del ladrillo

        # Propiedades del ladrillo
        self.color = color  # Color para dibujar
        self.destroyed = False  # Si el ladrillo fue destruido o no

    def draw(self, screen):
        """
        Dibuja el ladrillo en la pantalla con efectos 3D.
        Solo dibuja si el ladrillo no ha sido destruido.

        Parámetros:
        - screen: superficie de pygame donde dibujar
        """
        if not self.destroyed:  # Solo dibujar si no está destruido
            # Dibujar rectángulo principal del ladrillo
            pygame.draw.rect(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )

            # Crear efecto 3D con bordes de diferentes colores

            # Borde superior e izquierdo más claro (simula luz desde arriba-izquierda)
            light_color = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.rect(
                screen, light_color, (self.x, self.y, self.width, 3)
            )  # Borde superior
            pygame.draw.rect(
                screen, light_color, (self.x, self.y, 3, self.height)
            )  # Borde izquierdo

            # Borde inferior y derecho más oscuro (simula sombra)
            dark_color = tuple(max(0, c - 50) for c in self.color)
            pygame.draw.rect(
                screen,
                dark_color,
                (self.x, self.y + self.height - 3, self.width, 3),  # Borde inferior
            )
            pygame.draw.rect(
                screen,
                dark_color,
                (self.x + self.width - 3, self.y, 3, self.height),  # Borde derecho
            )

    def get_rect(self):
        """
        Devuelve un rectángulo pygame que representa el ladrillo.
        Útil para detección de colisiones con la pelota.

        Retorna:
        - pygame.Rect: rectángulo con posición y dimensiones del ladrillo
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def hit(self):
        """
        Marca el ladrillo como destruido cuando es golpeado por la pelota.
        Este método se llama cuando la pelota toca el ladrillo.
        """
        self.destroyed = True  # Marcar como destruido para que no se dibuje más


# ==========================================
# CLASE POWERUP (MEJORA ESPECIAL)
# ==========================================
class PowerUp:
    """
    Clase que representa los power-ups (mejoras especiales) del juego.
    Los power-ups aparecen aleatoriamente cuando se destruyen ladrillos
    y otorgan habilidades especiales temporales al jugador.
    """

    def __init__(self, x, y, power_type):
        """
        Constructor del power-up.

        Parámetros:
        - x: posición horizontal inicial
        - y: posición vertical inicial
        - power_type: tipo de mejora ('expand', 'multi_ball', 'slow_ball')
        """
        self.x = x  # Posición horizontal
        self.y = y  # Posición vertical

        # Dimensiones del power-up
        self.width = 30  # Ancho del power-up
        self.height = 15  # Alto del power-up

        # Propiedades de movimiento
        self.speed = 3  # Velocidad de caída (píxeles por frame)

        # Propiedades del juego
        self.power_type = (
            power_type  # Tipo de mejora ('expand', 'multi_ball', 'slow_ball')
        )
        self.active = True  # Si el power-up sigue activo en pantalla

    def move(self):
        """
        Mueve el power-up hacia abajo por la pantalla.
        Lo desactiva si sale de la pantalla sin ser recogido.
        """
        self.y += self.speed  # Mover hacia abajo

        # Desactivar si sale de la pantalla por abajo
        if self.y > WINDOW_HEIGHT:
            self.active = False

    def draw(self, screen):
        """
        Dibuja el power-up en la pantalla con colores según su tipo.

        Parámetros:
        - screen: superficie de pygame donde dibujar
        """
        if self.active:  # Solo dibujar si está activo
            # Determinar color según el tipo de power-up
            color = (
                GREEN
                if self.power_type == "expand"  # Verde para expandir
                else (
                    YELLOW
                    if self.power_type == "multi_ball"  # Amarillo para multi-pelota
                    else PURPLE
                )  # Púrpura para pelota lenta
            )

            # Dibujar rectángulo del power-up
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

            # Dibujar símbolo identificativo en el centro
            font = pygame.font.Font(None, 16)  # Fuente pequeña para el símbolo

            # Determinar símbolo según el tipo
            symbol = (
                "E"
                if self.power_type == "expand"  # E de Expand
                else (
                    "M" if self.power_type == "multi_ball" else "S"  # M de Multi-ball
                )  # S de Slow
            )

            # Renderizar y centrar el texto del símbolo
            text = font.render(symbol, True, WHITE)  # Texto blanco
            text_rect = text.get_rect(
                center=(self.x + self.width // 2, self.y + self.height // 2)
            )
            screen.blit(text, text_rect)  # Dibujar el texto en pantalla

    def get_rect(self):
        """
        Devuelve un rectángulo pygame que representa el power-up.
        Útil para detección de colisiones con la paleta.

        Retorna:
        - pygame.Rect: rectángulo con posición y dimensiones del power-up
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ==========================================
# CLASE GAME (JUEGO PRINCIPAL)
# ==========================================
class Game:
    """
    Clase principal que maneja todo el juego de Arkanoid.
    Coordina todos los objetos (paleta, pelota, ladrillos, power-ups),
    maneja los eventos, actualiza la lógica del juego y dibuja todo en pantalla.
    """

    def __init__(self):
        """
        Constructor del juego. Inicializa pygame y configura el estado inicial.
        """
        # Configurar ventana del juego
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Arkanoid - Python Game")
        self.clock = pygame.time.Clock()  # Para controlar velocidad del juego (60 FPS)

        # Variables del estado del juego
        self.score = 0  # Puntuación actual del jugador
        self.lives = 3  # Vidas restantes del jugador
        self.level = 1  # Nivel actual del juego

        # Configurar fuentes para mostrar texto en pantalla
        self.font = pygame.font.Font(None, 36)  # Fuente grande para títulos
        self.small_font = pygame.font.Font(None, 24)  # Fuente pequeña para información

        # Estado actual del juego
        self.game_state = (
            "menu"  # Posibles valores: 'menu', 'playing', 'game_over', 'victory'
        )

        # Inicializar el juego
        self.reset_game()

    def reset_game(self):
        """
        Reinicia el juego a su estado inicial.
        Crea nuevos objetos y limpia las listas para empezar un nivel fresco.
        """
        # Crear paleta centrada en la parte inferior de la pantalla
        self.paddle = Paddle(WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, WINDOW_HEIGHT - 50)

        # Crear pelota centrada en la pantalla
        self.balls = [Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]

        # Inicializar listas vacías para los objetos del juego
        self.bricks = []  # Lista de ladrillos
        self.power_ups = []  # Lista de power-ups activos

        # Crear la estructura de ladrillos para el nivel
        self.create_bricks()

    def create_bricks(self):
        """
        Crea la estructura de ladrillos para el nivel actual.
        Organiza los ladrillos en una cuadrícula colorida centrada en la pantalla.
        """
        self.bricks = []  # Empezar con lista vacía

        # Calcular posición inicial para centrar toda la cuadrícula
        start_x = (WINDOW_WIDTH - BRICK_COLS * BRICK_WIDTH) // 2
        start_y = 50  # Empezar 50 píxeles desde la parte superior

        # Crear ladrillos en una cuadrícula de filas y columnas
        for row in range(BRICK_ROWS):  # Para cada fila (0 a 7)
            for col in range(BRICK_COLS):  # Para cada columna (0 a 9)
                # Calcular posición exacta de este ladrillo
                x = start_x + col * BRICK_WIDTH  # Posición horizontal
                y = start_y + row * BRICK_HEIGHT  # Posición vertical

                # Asignar color basado en la fila (cicla a través de BRICK_COLORS)
                color = BRICK_COLORS[row % len(BRICK_COLORS)]

                # Crear y agregar el ladrillo a la lista
                brick = Brick(x, y, color)
                self.bricks.append(brick)

    def handle_events(self):
        """
        Maneja todos los eventos de entrada del usuario (teclado, cerrar ventana, etc.).
        Este método se ejecuta cada frame para procesar las acciones del usuario.

        Retorna:
        - bool: False si el usuario quiere salir del juego, True para continuar
        """
        # Procesar todos los eventos pendientes en la cola
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Usuario cerró la ventana
                return False
            elif event.type == pygame.KEYDOWN:  # Usuario presionó una tecla
                if event.key == pygame.K_SPACE:  # Tecla Espacio
                    if self.game_state == "menu":
                        self.game_state = "playing"  # Comenzar el juego
                    elif self.game_state == "game_over":
                        # Reiniciar completamente el juego
                        self.score = 0
                        self.lives = 3
                        self.level = 1
                        self.reset_game()
                        self.game_state = "playing"
                    elif self.game_state == "victory":
                        # Avanzar al siguiente nivel
                        self.level += 1
                        self.reset_game()
                        self.game_state = "playing"
                elif event.key == pygame.K_ESCAPE:  # Tecla Escape
                    return False  # Salir del juego
        return True  # Continuar ejecutando

    def update(self):
        """
        Actualiza toda la lógica del juego cada frame.
        Solo actualiza cuando estamos en estado 'playing'.
        """
        if self.game_state != "playing":
            return  # No actualizar si no estamos jugando

        # ==========================================
        # CONTROL DE LA PALETA
        # ==========================================
        # Verificar qué teclas están presionadas actualmente
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Flecha izquierda o A
            self.paddle.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Flecha derecha o D
            self.paddle.move_right()

        # ==========================================
        # MOVIMIENTO Y COLISIONES DE LAS PELOTAS
        # ==========================================
        balls_to_remove = []  # Lista de pelotas que salieron de la pantalla

        for i, ball in enumerate(self.balls):  # Para cada pelota activa
            ball.move()  # Mover la pelota

            # Verificar colisión con paredes
            if ball.check_wall_collision():
                balls_to_remove.append(i)  # Marcar para eliminar
                continue  # Pasar a la siguiente pelota

            # Verificar colisión con paleta
            ball.check_paddle_collision(self.paddle)

            # ==========================================
            # COLISIONES CON LADRILLOS
            # ==========================================
            ball_rect = ball.get_rect()  # Obtener rectángulo de la pelota

            for brick in self.bricks:  # Para cada ladrillo
                # Verificar si la pelota toca un ladrillo no destruido
                if not brick.destroyed and ball_rect.colliderect(brick.get_rect()):
                    brick.hit()  # Destruir el ladrillo
                    ball.bounce_y()  # Hacer rebotar la pelota
                    self.score += 10  # Aumentar puntuación

                    # Posibilidad de generar power-up (10% de probabilidad)
                    if random.random() < 0.1:
                        # Elegir tipo de power-up aleatoriamente
                        power_type = random.choice(
                            ["expand", "multi_ball", "slow_ball"]
                        )
                        # Crear power-up en la posición del ladrillo destruido
                        power_up = PowerUp(
                            brick.x + brick.width // 2, brick.y, power_type
                        )
                        self.power_ups.append(power_up)
                    break  # Solo un ladrillo por pelota por frame

        # Eliminar pelotas que salieron de la pantalla
        for i in reversed(balls_to_remove):  # Eliminar de atrás hacia adelante
            self.balls.pop(i)

        # ==========================================
        # VERIFICAR PÉRDIDA DE VIDA
        # ==========================================
        if not self.balls:  # Si no quedan pelotas
            self.lives -= 1  # Perder una vida
            if self.lives <= 0:
                self.game_state = "game_over"  # Fin del juego
            else:
                # Crear nueva pelota para continuar
                self.balls = [Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]

        # ==========================================
        # MOVIMIENTO Y COLISIÓN DE POWER-UPS
        # ==========================================
        power_ups_to_remove = []  # Lista de power-ups a eliminar

        for i, power_up in enumerate(self.power_ups):
            power_up.move()  # Mover power-up hacia abajo

            if not power_up.active:  # Si salió de la pantalla
                power_ups_to_remove.append(i)
            elif power_up.get_rect().colliderect(self.paddle.get_rect()):
                # Si la paleta tocó el power-up
                self.apply_power_up(power_up.power_type)  # Aplicar efecto
                power_ups_to_remove.append(i)  # Eliminar power-up

        # Eliminar power-ups inactivos o usados
        for i in reversed(power_ups_to_remove):
            self.power_ups.pop(i)

        # ==========================================
        # VERIFICAR VICTORIA
        # ==========================================
        # Si todos los ladrillos fueron destruidos
        if all(brick.destroyed for brick in self.bricks):
            self.game_state = "victory"

    def apply_power_up(self, power_type):
        """
        Aplica el efecto de un power-up cuando la paleta lo recoge.

        Parámetros:
        - power_type: tipo de power-up ('expand', 'multi_ball', 'slow_ball')
        """
        if power_type == "expand":
            # Expandir paleta (máximo 150 píxeles de ancho)
            self.paddle.width = min(150, self.paddle.width + 20)

        elif power_type == "multi_ball":
            # Agregar pelotas adicionales (máximo 5 pelotas)
            if len(self.balls) < 5:
                for _ in range(2):  # Agregar 2 pelotas nuevas
                    # Crear nueva pelota en la posición de una existente
                    new_ball = Ball(self.balls[0].x, self.balls[0].y)
                    # Asignar velocidad aleatoria
                    new_ball.speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
                    new_ball.speed_y = -BALL_SPEED
                    self.balls.append(new_ball)

        elif power_type == "slow_ball":
            # Reducir velocidad de todas las pelotas
            for ball in self.balls:
                ball.speed_x *= 0.7  # Reducir a 70% de la velocidad
                ball.speed_y *= 0.7

    def draw(self):
        """
        Dibuja todo el juego en la pantalla.
        Limpia la pantalla y dibuja según el estado actual del juego.
        """
        self.screen.fill(BLACK)  # Limpiar pantalla con color negro

        # Dibujar según el estado actual del juego
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "victory":
            self.draw_victory()

        pygame.display.flip()  # Actualizar la pantalla

    def draw_menu(self):
        """
        Dibuja la pantalla del menú principal.
        """
        # Título principal
        title = self.font.render("ARKANOID", True, WHITE)
        title_rect = title.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)
        )
        self.screen.blit(title, title_rect)

        # Instrucción para comenzar
        instruction = self.small_font.render(
            "Presiona ESPACIO para comenzar", True, WHITE
        )
        instruction_rect = instruction.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        self.screen.blit(instruction, instruction_rect)

        # Controles del juego
        controls = self.small_font.render(
            "Controles: ←/→ o A/D para mover", True, WHITE
        )
        controls_rect = controls.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        )
        self.screen.blit(controls, controls_rect)

    def draw_game(self):
        """
        Dibuja todos los elementos durante el juego activo.
        """
        # Dibujar paleta
        self.paddle.draw(self.screen)

        # Dibujar todas las pelotas
        for ball in self.balls:
            ball.draw(self.screen)

        # Dibujar todos los ladrillos
        for brick in self.bricks:
            brick.draw(self.screen)

        # Dibujar todos los power-ups activos
        for power_up in self.power_ups:
            power_up.draw(self.screen)

        # ==========================================
        # INTERFAZ DE USUARIO (UI)
        # ==========================================
        # Mostrar puntuación actual
        score_text = self.small_font.render(f"Puntuación: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Mostrar vidas restantes
        lives_text = self.small_font.render(f"Vidas: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 35))

        # Mostrar nivel actual
        level_text = self.small_font.render(f"Nivel: {self.level}", True, WHITE)
        self.screen.blit(level_text, (WINDOW_WIDTH - 100, 10))

    def draw_game_over(self):
        """
        Dibuja la pantalla de game over cuando el jugador pierde.
        """
        # Mensaje de game over
        game_over = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        self.screen.blit(game_over, game_over_rect)

        # Mostrar puntuación final
        score = self.small_font.render(f"Puntuación Final: {self.score}", True, WHITE)
        score_rect = score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(score, score_rect)

        # Instrucción para reiniciar
        restart = self.small_font.render("Presiona ESPACIO para reiniciar", True, WHITE)
        restart_rect = restart.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        )
        self.screen.blit(restart, restart_rect)

    def draw_victory(self):
        """
        Dibuja la pantalla de victoria cuando el jugador completa un nivel.
        """
        # Mensaje de victoria
        victory = self.font.render("¡NIVEL COMPLETADO!", True, GREEN)
        victory_rect = victory.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        self.screen.blit(victory, victory_rect)

        # Mostrar puntuación actual
        score = self.small_font.render(f"Puntuación: {self.score}", True, WHITE)
        score_rect = score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(score, score_rect)

        # Instrucción para continuar al siguiente nivel
        next_level = self.small_font.render(
            "Presiona ESPACIO para el siguiente nivel", True, WHITE
        )
        next_level_rect = next_level.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        )
        self.screen.blit(next_level, next_level_rect)

    def run(self):
        """
        Bucle principal del juego.
        Se ejecuta continuamente hasta que el usuario decida salir.
        Mantiene el juego funcionando a 60 frames por segundo.
        """
        running = True  # Variable para controlar si el juego sigue ejecutándose

        while running:  # Bucle infinito del juego
            # Procesar eventos del usuario (teclado, mouse, cerrar ventana)
            running = self.handle_events()

            # Actualizar lógica del juego (movimientos, colisiones, etc.)
            self.update()

            # Dibujar todo en la pantalla
            self.draw()

            # Mantener velocidad constante del juego (60 FPS)
            self.clock.tick(60)

        # Cuando salimos del bucle, cerrar pygame y terminar el programa
        pygame.quit()
        sys.exit()


# ==========================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================
if __name__ == "__main__":
    """
    Este bloque se ejecuta solo cuando el archivo se ejecuta directamente
    (no cuando se importa como módulo).

    Es la forma estándar en Python de tener código que solo se ejecute
    cuando el archivo es el programa principal.
    """
    # Crear una instancia del juego
    game = Game()

    # Iniciar el bucle principal del juego
    game.run()
