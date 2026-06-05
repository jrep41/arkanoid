"""
ARKANOID - EDICIÓN MEJORADA
===========================
Un juego completo de Arkanoid desarrollado en Python usando pygame.
Este código está comentado para principiantes en Python.

Autor: GitHub Copilot
Fecha: Julio 2025
"""

# Importamos las librerías necesarias
import pygame  # Librería principal para hacer juegos en Python
import sys  # Para funciones del sistema como salir del programa
import math  # Para cálculos matemáticos (ángulos, trigonometría)
import random  # Para generar números aleatorios
import os  # Para operaciones con archivos y sistema operativo
import sounds  # Módulo de efectos de sonido sintéticos

# Inicializar Pygame - SIEMPRE necesario antes de usar pygame
pygame.init()  # Inicializa todos los módulos de pygame
pygame.mixer.init()  # Inicializa el sistema de sonido

# ==========================================
# CONSTANTES DEL JUEGO
# ==========================================
# Las constantes son valores que NO cambian durante el juego
# Se escriben en MAYÚSCULAS por convención en Python

# Dimensiones de la ventana del juego (en píxeles)
WINDOW_WIDTH = 1000  # Ancho de la ventana
WINDOW_HEIGHT = 700  # Alto de la ventana

# Dimensiones de la paleta del jugador
PADDLE_WIDTH = 130  # Ancho de la paleta
PADDLE_HEIGHT = 10  # Alto de la paleta (50% más fina)

# Propiedades de la pelota
BALL_SIZE = 10  # Tamaño de la pelota (diámetro) (50% más pequeña)

# Dimensiones de los ladrillos
BRICK_WIDTH = 90  # Ancho de cada ladrillo
BRICK_HEIGHT = 25  # Alto de cada ladrillo
BRICK_ROWS = 8  # Número de filas de ladrillos
BRICK_COLS = 10  # Número de columnas de ladrillos

# Velocidades del juego (píxeles por frame)
PADDLE_SPEED = 8  # Qué tan rápido se mueve la paleta
BALL_SPEED = 3  # Velocidad inicial de la pelota (reducida para facilitar el juego)
INITIAL_BALL_SPEED = 3  # Velocidad inicial constante para resets
MIN_BALL_SPEED = 2  # Velocidad mínima de la pelota (límite para slow_ball)

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
CYAN = (0, 255, 255)  # Cian (verde + azul)
DARK_BLUE = (0, 0, 139)  # Azul oscuro
DARKER_BLUE = (10, 10, 40)  # Azul muy oscuro para fondo

# Neon colors for professional glow effects
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 0, 128)
NEON_PURPLE = (180, 0, 255)
NEON_ORANGE = (255, 100, 0)
NEON_GREEN = (0, 255, 100)
NEON_YELLOW = (255, 255, 0)
NEON_RED = (255, 50, 50)

# Lista de colores para los ladrillos (una por fila) - paleta metálica oscura
BRICK_COLORS = [
    (180, 40, 40),    # Rojo oscuro metálico
    (180, 100, 30),    # Naranja oxidado
    (160, 150, 50),   # Oro antiguo
    (40, 140, 60),    # Verde bronce
    (40, 100, 180),    # Azul acero
    (120, 40, 160),    # Púrpura oscuro
    (180, 60, 120),   # Rosa oxidado
    (50, 140, 160),   # Cian oscuro
]

# ==========================================
# PATRONES DE NIVELES ORIGINALES DEL ARKANOID
# ==========================================
# Cada nivel está representado como una matriz donde:
# 0 = espacio vacío, 1-8 = ladrillo de color correspondiente al índice en BRICK_COLORS

ORIGINAL_LEVELS = [
    # NIVEL 1 - Rectángulo clásico
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
        [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 6, 6, 6, 6, 6, 6, 6, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 2 - Pirámide
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 3 - Rombo
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [0, 0, 5, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 0, 6, 6, 6, 6, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 4 - Torres laterales
    [
        [1, 1, 0, 0, 0, 0, 0, 0, 8, 8],
        [1, 1, 0, 0, 0, 0, 0, 0, 8, 8],
        [2, 2, 0, 3, 3, 3, 3, 0, 7, 7],
        [2, 2, 0, 3, 3, 3, 3, 0, 7, 7],
        [3, 3, 0, 4, 4, 4, 4, 0, 6, 6],
        [3, 3, 0, 4, 4, 4, 4, 0, 6, 6],
        [4, 4, 0, 0, 0, 0, 0, 0, 5, 5],
        [4, 4, 0, 0, 0, 0, 0, 0, 5, 5],
    ],
    # NIVEL 5 - Escalera
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
        [6, 6, 6, 6, 6, 6, 0, 0, 0, 0],
        [7, 7, 7, 7, 7, 7, 7, 0, 0, 0],
        [8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
    ],
    # NIVEL 6 - Cruz
    [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 6, 6, 6, 6, 0, 0, 0],
        [0, 0, 0, 7, 7, 7, 7, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
    ],
    # NIVEL 7 - Círculos concéntricos
    [
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
        [1, 2, 3, 4, 4, 4, 4, 3, 2, 1],
        [1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
        [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 8 - Patrón zigzag
    [
        [1, 1, 0, 0, 0, 0, 0, 0, 2, 2],
        [0, 1, 1, 0, 0, 0, 0, 2, 2, 0],
        [0, 0, 3, 3, 0, 0, 4, 4, 0, 0],
        [0, 0, 0, 3, 3, 4, 4, 0, 0, 0],
        [0, 0, 0, 5, 5, 6, 6, 0, 0, 0],
        [0, 0, 7, 7, 0, 0, 8, 8, 0, 0],
        [0, 7, 7, 0, 0, 0, 0, 8, 8, 0],
        [7, 7, 0, 0, 0, 0, 0, 0, 8, 8],
    ],
    # NIVEL 9 - Patrón lateral
    [
        [1, 0, 2, 0, 3, 0, 4, 0, 5, 0],
        [0, 6, 0, 7, 0, 8, 0, 1, 0, 2],
        [3, 0, 4, 0, 5, 0, 6, 0, 7, 0],
        [0, 8, 0, 1, 0, 2, 0, 3, 0, 4],
        [5, 0, 6, 0, 7, 0, 8, 0, 1, 0],
        [0, 2, 0, 3, 0, 4, 0, 5, 0, 6],
        [7, 0, 8, 0, 1, 0, 2, 0, 3, 0],
        [0, 4, 0, 5, 0, 6, 0, 7, 0, 8],
    ],
    # NIVEL 10 - Espiral
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [1, 0, 3, 3, 3, 3, 3, 0, 2, 0],
        [1, 0, 3, 0, 0, 0, 4, 0, 2, 0],
        [1, 0, 3, 0, 5, 5, 4, 0, 2, 0],
        [1, 0, 3, 4, 4, 4, 4, 0, 2, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    ],
    # NIVEL 11 - Laberinto
    [
        [1, 1, 1, 0, 0, 0, 0, 2, 2, 2],
        [1, 0, 0, 0, 3, 3, 0, 0, 0, 2],
        [1, 0, 4, 4, 4, 4, 4, 4, 0, 2],
        [1, 0, 4, 0, 0, 0, 0, 4, 0, 2],
        [1, 0, 4, 0, 5, 5, 0, 4, 0, 2],
        [1, 0, 4, 0, 5, 5, 0, 4, 0, 2],
        [1, 0, 4, 4, 4, 4, 4, 4, 0, 2],
        [1, 1, 1, 0, 0, 0, 0, 2, 2, 2],
    ],
    # NIVEL 12 - Ondas
    [
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
        [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
        [0, 4, 0, 4, 0, 4, 0, 4, 0, 4],
        [5, 0, 5, 0, 5, 0, 5, 0, 5, 0],
        [0, 6, 0, 6, 0, 6, 0, 6, 0, 6],
        [7, 0, 7, 0, 7, 0, 7, 0, 7, 0],
        [0, 8, 0, 8, 0, 8, 0, 8, 0, 8],
    ],
    # NIVEL 13 - Arco
    [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 2, 2, 0, 0],
        [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    ],
    # NIVEL 14 - Estrella
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 2, 2, 0, 0],
        [0, 3, 3, 0, 0, 0, 0, 3, 3, 0],
        [4, 4, 0, 0, 5, 5, 0, 0, 4, 4],
        [4, 4, 0, 0, 5, 5, 0, 0, 4, 4],
        [0, 3, 3, 0, 0, 0, 0, 3, 3, 0],
        [0, 0, 2, 2, 2, 2, 2, 2, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ],
    # NIVEL 15 - Escalera doble
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [2, 2, 0, 0, 0, 0, 0, 0, 7, 7],
        [3, 3, 3, 0, 0, 0, 0, 6, 6, 6],
        [4, 4, 4, 4, 0, 0, 5, 5, 5, 5],
        [4, 4, 4, 4, 0, 0, 5, 5, 5, 5],
        [3, 3, 3, 0, 0, 0, 0, 6, 6, 6],
        [2, 2, 0, 0, 0, 0, 0, 0, 7, 7],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    ],
    # NIVEL 16 - Diamante
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [0, 0, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ],
    # NIVEL 17 - Pared lateral
    [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 3, 0, 0, 4, 4, 4, 4, 4],
        [4, 4, 4, 0, 0, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 6, 6, 6, 6, 6],
        [6, 6, 6, 0, 0, 7, 7, 7, 7, 7],
        [7, 7, 7, 0, 0, 8, 8, 8, 8, 8],
        [8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 18 - Círculos separados
    [
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        [1, 2, 2, 2, 1, 1, 2, 2, 2, 1],
        [1, 2, 3, 2, 1, 1, 2, 3, 2, 1],
        [1, 2, 2, 2, 1, 1, 2, 2, 2, 1],
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 19 - Líneas paralelas
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 1, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 3, 4, 5, 6, 7, 8, 1, 2, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 4, 5, 6, 7, 8, 1, 2, 3, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 5, 6, 7, 8, 1, 2, 3, 4, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 20 - Castillo
    [
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [0, 3, 0, 3, 3, 3, 3, 0, 3, 0],
        [0, 3, 0, 3, 3, 3, 3, 0, 3, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    ],
    # NIVEL 21 - Mariposa
    [
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [2, 2, 2, 0, 0, 0, 0, 2, 2, 2],
        [3, 3, 3, 3, 0, 0, 3, 3, 3, 3],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [3, 3, 3, 3, 0, 0, 3, 3, 3, 3],
        [2, 2, 2, 0, 0, 0, 0, 2, 2, 2],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    ],
    # NIVEL 22 - Túnel
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [3, 0, 4, 4, 4, 4, 4, 4, 0, 3],
        [4, 0, 5, 0, 0, 0, 0, 5, 0, 4],
        [4, 0, 5, 0, 0, 0, 0, 5, 0, 4],
        [3, 0, 4, 4, 4, 4, 4, 4, 0, 3],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    # NIVEL 23 - Corazón
    [
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [1, 2, 2, 1, 0, 0, 1, 2, 2, 1],
        [1, 2, 2, 2, 1, 1, 2, 2, 2, 1],
        [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [0, 0, 1, 2, 2, 2, 2, 1, 0, 0],
        [0, 0, 0, 1, 2, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 24 - Pirámide invertida
    [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
        [0, 0, 6, 6, 6, 6, 6, 6, 0, 0],
        [0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 25 - Cuadrados concéntricos
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
        [1, 2, 3, 4, 4, 4, 4, 3, 2, 1],
        [1, 2, 3, 4, 4, 4, 4, 3, 2, 1],
        [1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    # NIVEL 26 - Flecha
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [0, 0, 0, 6, 6, 6, 6, 0, 0, 0],
        [0, 0, 0, 7, 7, 7, 7, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 8, 0, 0, 0],
    ],
    # NIVEL 27 - Rompecabezas
    [
        [1, 1, 0, 2, 2, 3, 3, 0, 4, 4],
        [1, 1, 0, 2, 2, 3, 3, 0, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 0, 6, 6, 7, 7, 0, 8, 8],
        [5, 5, 0, 6, 6, 7, 7, 0, 8, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 2, 2, 3, 3, 0, 4, 4],
        [1, 1, 0, 2, 2, 3, 3, 0, 4, 4],
    ],
    # NIVEL 28 - Ondas verticales
    [
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [2, 0, 0, 2, 2, 2, 2, 0, 0, 2],
        [3, 3, 0, 0, 3, 3, 0, 0, 3, 3],
        [4, 4, 0, 0, 4, 4, 0, 0, 4, 4],
        [5, 5, 5, 0, 0, 0, 0, 5, 5, 5],
        [6, 6, 6, 0, 0, 0, 0, 6, 6, 6],
        [7, 7, 7, 7, 0, 0, 7, 7, 7, 7],
        [8, 8, 8, 8, 0, 0, 8, 8, 8, 8],
    ],
    # NIVEL 29 - Rejilla
    [
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 4, 0, 4, 0, 4, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # NIVEL 30 - Templo
    [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 2, 2, 0, 0],
        [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [5, 0, 5, 0, 5, 5, 0, 5, 0, 5],
        [6, 0, 6, 0, 6, 6, 0, 6, 0, 6],
        [7, 0, 7, 0, 7, 7, 0, 7, 0, 7],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    ],
    # NIVEL 31 - Fortaleza
    [
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 0, 3, 3, 3, 3, 3, 3, 0, 3],
        [3, 0, 0, 4, 4, 4, 4, 0, 0, 3],
        [3, 0, 0, 4, 5, 5, 4, 0, 0, 3],
        [3, 0, 0, 4, 4, 4, 4, 0, 0, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ],
    # NIVEL 32 - Galaxia
    [
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        [0, 1, 2, 2, 1, 1, 2, 2, 1, 0],
        [1, 2, 3, 3, 2, 2, 3, 3, 2, 1],
        [1, 2, 3, 4, 3, 3, 4, 3, 2, 1],
        [1, 2, 3, 4, 3, 3, 4, 3, 2, 1],
        [1, 2, 3, 3, 2, 2, 3, 3, 2, 1],
        [0, 1, 2, 2, 1, 1, 2, 2, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    ],
    # NIVEL 33 - Pirámide maya
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [6, 0, 6, 0, 6, 6, 0, 6, 0, 6],
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    ],
    # NIVEL 34 - Caleidoscopio
    [
        [1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
        [2, 3, 4, 5, 6, 6, 5, 4, 3, 2],
        [3, 4, 5, 6, 7, 7, 6, 5, 4, 3],
        [4, 5, 6, 7, 8, 8, 7, 6, 5, 4],
        [4, 5, 6, 7, 8, 8, 7, 6, 5, 4],
        [3, 4, 5, 6, 7, 7, 6, 5, 4, 3],
        [2, 3, 4, 5, 6, 6, 5, 4, 3, 2],
        [1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
    ],
    # NIVEL 35 - Cruz doble
    [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 2, 0, 0],
        [3, 3, 3, 3, 0, 0, 3, 3, 3, 3],
        [4, 4, 4, 4, 0, 0, 4, 4, 4, 4],
        [5, 5, 5, 5, 0, 0, 5, 5, 5, 5],
        [0, 0, 6, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 8, 0, 0, 0, 0, 8, 0, 0],
    ],
    # NIVEL 36 - Final épico
    [
        [1, 1, 2, 2, 3, 3, 2, 2, 1, 1],
        [1, 4, 4, 5, 5, 5, 5, 4, 4, 1],
        [2, 4, 6, 6, 7, 7, 6, 6, 4, 2],
        [2, 5, 6, 8, 8, 8, 8, 6, 5, 2],
        [3, 5, 7, 8, 1, 1, 8, 7, 5, 3],
        [3, 5, 7, 8, 1, 1, 8, 7, 5, 3],
        [2, 5, 6, 8, 8, 8, 8, 6, 5, 2],
        [2, 4, 6, 6, 7, 7, 6, 6, 4, 2],
    ],
]

# Nombres descriptivos para cada patrón de nivel
LEVEL_NAMES = [
    "Rectángulo Clásico",  # 1
    "Pirámide",  # 2
    "Rombo",  # 3
    "Torres Laterales",  # 4
    "Escalera",  # 5
    "Cruz",  # 6
    "Círculos Concéntricos",  # 7
    "Zigzag",  # 8
    "Patrón Lateral",  # 9
    "Espiral",  # 10
    "Laberinto",  # 11
    "Ondas",  # 12
    "Arco",  # 13
    "Estrella",  # 14
    "Escalera Doble",  # 15
    "Diamante",  # 16
    "Pared Lateral",  # 17
    "Círculos Separados",  # 18
    "Líneas Paralelas",  # 19
    "Castillo",  # 20
    "Mariposa",  # 21
    "Túnel",  # 22
    "Corazón",  # 23
    "Pirámide Invertida",  # 24
    "Cuadrados Concéntricos",  # 25
    "Flecha",  # 26
    "Rompecabezas",  # 27
    "Ondas Verticales",  # 28
    "Rejilla",  # 29
    "Templo",  # 30
    "Fortaleza",  # 31
    "Galaxia",  # 32
    "Pirámide Maya",  # 33
    "Caleidoscopio",  # 34
    "Cruz Doble",  # 35
    "Final Épico",  # 36
]


# ==========================================
# CLASE PARTICLE (PARTÍCULA)
# ==========================================
class Particle:
    """
    Clase que representa una partícula visual.
    Las partículas son pequeños efectos que aparecen cuando se destruye un ladrillo.
    Dan un efecto visual más impresionante al juego.
    """

    def __init__(self, x, y, color):
        """
        Constructor de la partícula.
        Se ejecuta automáticamente cuando creamos una nueva partícula.

        Parámetros:
        - x: posición horizontal inicial (píxeles)
        - y: posición vertical inicial (píxeles)
        - color: color de la partícula (tupla RGB)
        """
        self.x = x  # Posición horizontal actual
        self.y = y  # Posición vertical actual

        # Velocidad aleatoria en X (izquierda-derecha)
        # random.uniform(a, b) genera un número decimal aleatorio entre a y b
        self.vx = random.uniform(-3, 3)  # Entre -3 y 3 píxeles por frame

        # Velocidad aleatoria en Y (arriba-abajo)
        # Negativo significa que va hacia arriba inicialmente
        self.vy = random.uniform(-6, -2)  # Entre -6 y -2 píxeles por frame

        self.color = color  # Color de la partícula
        self.life = 30  # Tiempo de vida en frames (30 frames = 0.5 segundos a 60fps)
        self.max_life = 30  # Tiempo de vida máximo (para calcular transparencia)

    def update(self):
        """
        Actualiza la posición y estado de la partícula cada frame.
        Este método se llama 60 veces por segundo.
        """
        # Mover la partícula según su velocidad
        self.x += self.vx  # Nueva posición X = posición actual + velocidad X
        self.y += self.vy  # Nueva posición Y = posición actual + velocidad Y

        # Simular gravedad: acelerar hacia abajo
        self.vy += 0.2  # Aumentar velocidad vertical (hacia abajo)

        # Reducir tiempo de vida
        self.life -= 1  # La partícula vive un frame menos

    def draw(self, screen):
        """
        Dibuja la partícula en la pantalla con efecto de brillo neón.
        """
        if self.life > 0:
            size = max(1, int(3 * (self.life / self.max_life)))
            bright_color = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.circle(screen, bright_color, (int(self.x), int(self.y)), size)


# ==========================================
# CLASE PADDLE (PALETA)
# ==========================================
class Paddle:
    """
    Clase que representa la paleta del jugador.
    La paleta es el rectángulo azul que controla el jugador para rebotar la pelota.
    """

    def __init__(self, x, y):
        """
        Constructor de la paleta.

        Parámetros:
        - x: posición horizontal inicial (píxeles)
        - y: posición vertical inicial (píxeles)
        """
        self.x = x  # Posición horizontal (esquina izquierda)
        self.y = y  # Posición vertical (esquina superior)

        # Dimensiones de la paleta
        self.width = PADDLE_WIDTH  # Ancho actual de la paleta
        self.height = PADDLE_HEIGHT  # Alto de la paleta (no cambia)

        # Velocidad de movimiento
        self.speed = PADDLE_SPEED  # Píxeles que se mueve por frame

        # Para el power-up de expansión
        self.original_width = PADDLE_WIDTH  # Ancho original (para restaurar)
        self.expand_timer = 0  # Contador para duración del power-up

        # Para el power-up de disparo láser
        self.laser_active = False  # Si puede disparar láser
        self.laser_timer = 0  # Duración del power-up de láser
        self.laser_cooldown = 0  # Tiempo entre disparos

    def update_mouse_position(self, mouse_x):
        """
        Actualiza la posición de la paleta basada en la posición del ratón.

        Parámetros:
        - mouse_x: posición horizontal del ratón
        """
        # Centrar la paleta en la posición del ratón
        self.x = mouse_x - self.width // 2

        # Verificar límites de la pantalla
        if self.x < 0:
            self.x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width

    def update(self):
        """
        Actualiza el estado de la paleta cada frame.
        Principalmente maneja la duración de los power-ups.
        """
        # Si la paleta está expandida, contar hacia atrás
        if self.expand_timer > 0:
            self.expand_timer -= 1  # Reducir el contador

            # Si el tiempo se acabó, restaurar tamaño original
            if self.expand_timer <= 0:
                self.width = self.original_width

        # Manejar power-up de láser
        if self.laser_timer > 0:
            self.laser_timer -= 1
            self.laser_active = True

            # Si el tiempo se acabó, desactivar láser
            if self.laser_timer <= 0:
                self.laser_active = False

        # Reducir cooldown de disparo
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

    def move_left(self):
        """
        Mueve la paleta hacia la izquierda.
        Incluye verificación para no salirse de la pantalla.
        """
        # Solo mover si no estamos en el borde izquierdo
        if self.x > 0:
            self.x -= self.speed  # Mover hacia la izquierda

    def move_right(self):
        """
        Mueve la paleta hacia la derecha.
        Incluye verificación para no salirse de la pantalla.
        """
        # Solo mover si no estamos en el borde derecho
        # (posición + ancho) no debe ser mayor que el ancho de la ventana
        if self.x < WINDOW_WIDTH - self.width:
            self.x += self.speed  # Mover hacia la derecha

    def expand(self):
        """
        Activa el power-up de expansión de la paleta.
        Hace la paleta más grande por un tiempo limitado.
        """
        # Aumentar ancho pero no más allá de 200 píxeles
        self.width = min(200, self.width + 30)

        # Establecer duración del power-up
        # 600 frames = 10 segundos a 60 FPS
        self.expand_timer = 600

    def activate_laser(self):
        """
        Activa el power-up de disparo láser.
        Permite a la paleta disparar proyectiles por un tiempo limitado.
        """
        # activar láser si pulsamos la tecla l
        
        self.laser_active = True
        # 2000 frames = 20 segundos a 60 FPS (reducido)
        self.laser_timer = 2000

    def can_shoot(self):
        """
        Verifica si la paleta puede disparar en este momento.

        Retorna:
        - bool: True si puede disparar, False si no
        """
        return self.laser_active and self.laser_cooldown <= 0

    def shoot(self):
        """
        Crea dos proyectiles láser desde ambos lados de la paleta.

        Retorna:
        - list: lista con dos objetos láser o lista vacía si no puede disparar
        """
        if self.can_shoot():
            # Crear láser izquierdo (desde el lado izquierdo de la paleta)
            laser_left_x = self.x + self.width // 4 - 1  # Posición izquierda
            laser_left_y = self.y - 10  # Un poco arriba de la paleta

            # Crear láser derecho (desde el lado derecho de la paleta)
            laser_right_x = self.x + (self.width * 3) // 4 - 1  # Posición derecha
            laser_right_y = self.y - 10  # Un poco arriba de la paleta

            # Establecer cooldown entre disparos (30 frames = 0.5 segundos)
            self.laser_cooldown = 30

            return [
                Laser(laser_left_x, laser_left_y),
                Laser(laser_right_x, laser_right_y),
            ]
        return []

    def draw(self, screen):
        """
        Dibuja la paleta en la pantalla con efectos de brillo neón profesionales.
        """
        main_color = NEON_CYAN
        laser_color = NEON_RED

        # Efecto de brillo exterior (glow muy fino, sin superposición)
        glow_time = pygame.time.get_ticks() * 0.003
        glow_intensity = 0.15 + 0.1 * math.sin(glow_time)

        # Solo glow exterior fino
        glow_color = tuple(min(255, c + 30) for c in main_color)
        glow_alpha = int(150 * glow_intensity)
        pygame.draw.rect(
            screen,
            glow_color,
            (self.x - 1, self.y - 1, self.width + 2, self.height + 2),
            1
        )

        # Crear efecto de gradiente profesional
        for i in range(self.height):
            ratio = i / self.height
            color = (
                int(20 + 30 * (1 - ratio)),
                int(50 + 100 * (1 - ratio)),
                int(200 + 55 * (1 - ratio)),
            )
            pygame.draw.rect(screen, color, (self.x, self.y + i, self.width, 1))

        # Borde brillante con efecto neón
        if self.laser_active:
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.015)) * 0.5 + 0.5
            laser_color = (int(255 * pulse), int(50 * pulse), int(50 * pulse))
            pygame.draw.rect(
                screen, laser_color, (self.x, self.y, self.width, self.height), 1
            )
        else:
            pygame.draw.rect(
                screen, main_color, (self.x, self.y, self.width, self.height), 1
            )

        # Línea de brillo superior
        highlight_color = (150, 220, 255)
        pygame.draw.rect(screen, highlight_color, (self.x + 1, self.y + 1, self.width - 2, 1))

        # Dibujar cañones láser si está activo
        if self.laser_active:
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.02)) * 0.3 + 0.7

            # Cañón izquierdo con brillo
            cannon_left_x = self.x + self.width // 4
            cannon_left_y = self.y - 3

            # Glow del cañón
            pygame.draw.rect(
                screen, (int(100 * pulse), 0, 0), (cannon_left_x - 4, cannon_left_y - 2, 8, 10)
            )
            pygame.draw.rect(
                screen, laser_color, (cannon_left_x - 2, cannon_left_y, 4, 6)
            )
            # Punta brillante
            pygame.draw.circle(screen, (255, 100, 100), (cannon_left_x, cannon_left_y), 4)

            # Cañón derecho con brillo
            cannon_right_x = self.x + (self.width * 3) // 4
            cannon_right_y = self.y - 3

            pygame.draw.rect(
                screen, (int(100 * pulse), 0, 0), (cannon_right_x - 4, cannon_right_y - 2, 8, 10)
            )
            pygame.draw.rect(
                screen, laser_color, (cannon_right_x - 2, cannon_right_y, 4, 6)
            )
            pygame.draw.circle(screen, (255, 100, 100), (cannon_right_x, cannon_right_y), 4)

    def get_rect(self):
        """
        Devuelve un rectángulo pygame que representa la paleta.
        Útil para detección de colisiones.

        Retorna:
        - pygame.Rect: rectángulo con posición y dimensiones de la paleta
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ==========================================
# CLASE BALL (PELOTA)
# ==========================================
class Ball:
    """
    Clase que representa la pelota del juego.
    La pelota rebota por la pantalla, destruye ladrillos y debe ser mantenida
    en juego por la paleta del jugador.
    """

    def __init__(self, x, y, stuck_to_paddle=False):
        """
        Constructor de la pelota.

        Parámetros:
        - x: posición horizontal inicial (píxeles)
        - y: posición vertical inicial (píxeles)
        - stuck_to_paddle: si la pelota empieza pegada a la paleta
        """
        self.x = x  # Posición horizontal del centro de la pelota
        self.y = y  # Posición vertical del centro de la pelota

        # Propiedades físicas
        self.size = BALL_SIZE  # Diámetro de la pelota
        self.radius = BALL_SIZE // 2  # Radio (para cálculos de colisión)

        # Velocidad de movimiento (píxeles por frame)
        self.speed_x = BALL_SPEED  # Velocidad horizontal (positivo = derecha)
        self.speed_y = -BALL_SPEED  # Velocidad vertical (negativo = arriba)

        # Estado de la pelota pegada
        self.stuck_to_paddle = stuck_to_paddle  # Si está pegada a la paleta
        self.offset_from_paddle = 0  # Desplazamiento desde el centro de la paleta

        # Efecto visual del rastro
        self.trail = []  # Lista de posiciones anteriores
        self.trail_length = 10  # Máximo de posiciones a recordar

        # Modo destructor
        self.destroyer_mode = False  # Si puede destruir ladrillos de un golpe
        self.destroyer_timer = 0  # Tiempo restante del modo destructor

        # Sistema de cooldown para evitar múltiples hits
        self.collision_cooldown = 0  # Frames restantes de cooldown
        self.last_hit_brick = None  # Último ladrillo golpeado

        # Referencia al gestor de sonidos (se asigna al crear la pelota)
        self.game_sound_manager: 'sounds.SoundManager | None' = None

    def release(self, angle=None):
        """
        Libera la pelota de la paleta con un ángulo específico.

        Parámetros:
        - angle: ángulo de lanzamiento (None para ángulo aleatorio suave)
        """
        self.stuck_to_paddle = False

        # Si no se especifica ángulo, usar uno aleatorio suave
        if angle is None:
            import random

            angle = random.uniform(-math.pi / 6, math.pi / 6)  # ±30 grados

        # Calcular velocidades basadas en el ángulo
        speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        self.speed_x = speed * math.sin(angle)
        self.speed_y = -abs(speed * math.cos(angle))  # Siempre hacia arriba

    def update_stuck_position(self, paddle):
        """
        Actualiza la posición de la pelota cuando está pegada a la paleta.

        Parámetros:
        - paddle: objeto Paddle al que está pegada la pelota
        """
        if self.stuck_to_paddle:
            # Mantener la pelota centrada en la paleta
            self.x = paddle.x + paddle.width // 2 + self.offset_from_paddle
            self.y = paddle.y - self.radius - 2  # Un poco arriba de la paleta

    def move(self):
        """
        Mueve la pelota según su velocidad actual.
        También mantiene el rastro visual de movimiento.
        No se mueve si está pegada a la paleta.
        """
        # No mover si está pegada a la paleta
        if self.stuck_to_paddle:
            return

        # Guardar posición actual en el rastro para efecto visual
        self.trail.append((self.x, self.y))

        # Limitar el tamaño del rastro para no consumir demasiada memoria
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)  # Eliminar la posición más antigua

        # Mover la pelota según su velocidad
        self.x += self.speed_x  # Nueva posición X = actual + velocidad
        self.y += self.speed_y  # Nueva posición Y = actual + velocidad

        # Actualizar cooldown de colisión
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        # Actualizar timer del modo destructor
        if self.destroyer_timer > 0:
            self.destroyer_timer -= 1
            if self.destroyer_timer <= 0:
                self.destroyer_mode = False

    def bounce_x(self):
        """
        Invierte la dirección horizontal de la pelota.
        Se usa cuando rebota en paredes laterales.
        """
        self.speed_x = -self.speed_x  # Cambiar dirección horizontal

    def bounce_y(self):
        """
        Invierte la dirección vertical de la pelota.
        Se usa cuando rebota en paredes, paleta o ladrillos.
        """
        self.speed_y = -self.speed_y  # Cambiar dirección vertical

    def check_wall_collision(self):
        """
        Verifica si la pelota colisiona con las paredes de la pantalla.
        Hace rebotar la pelota automáticamente en paredes laterales y superior.

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
        Verifica si la pelota colisiona con la paleta del jugador.
        Implementa física realista de rebote basada en dónde golpea la paleta.

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

        # Verificar colisión solo si la pelota va hacia abajo
        if ball_rect.colliderect(paddle_rect) and self.speed_y > 0:
            # Calcular dónde golpeó la pelota en la paleta (0 = izquierda, 1 = derecha)
            hit_pos = (self.x - paddle.x) / paddle.width

            # Convertir posición de golpe a ángulo de rebote
            # hit_pos - 0.5 da un rango de -0.5 a 0.5
            # Multiplicar por π/3 da un ángulo máximo de 60 grados
            angle = (hit_pos - 0.5) * math.pi / 3

            # Calcular velocidad total (hipotenusa del triángulo de velocidades)
            speed = math.sqrt(self.speed_x**2 + self.speed_y**2)

            # Aplicar nueva dirección basada en el ángulo
            self.speed_x = speed * math.sin(angle)  # Componente horizontal
            self.speed_y = -abs(
                speed * math.cos(angle)
            )  # Componente vertical (hacia arriba)

            # Reproducir sonido de rebote en paleta
            if self.game_sound_manager:
                self.game_sound_manager.play('paddle_hit')

            return True  # Hubo colisión
        return False  # No hubo colisión

    def draw(self, screen):
        """
        Dibuja la pelota en la pantalla con efectos de brillo neón profesionales.
        """
        # Color de la pelota según el modo
        if self.destroyer_mode:
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.02)) * 0.4 + 0.6
            main_color = (int(255 * pulse), int(50 * pulse), int(50 * pulse))
            glow_color = NEON_RED
            outer_color = (255, 100, 50)
        else:
            main_color = WHITE
            glow_color = NEON_CYAN
            outer_color = (100, 200, 255)

        # Dibujar rastro de la pelota (simplificado, sin glow)
        for i, (trail_x, trail_y) in enumerate(self.trail):
            ratio = i / len(self.trail) if len(self.trail) > 0 else 0
            trail_radius = max(1, int(self.radius * ratio * 0.6))
            if trail_radius > 0:
                trail_color = tuple(int(c * ratio * 0.7) for c in main_color)
                pygame.draw.circle(
                    screen, trail_color, (int(trail_x), int(trail_y)), trail_radius
                )

        # Glow exterior fino (solo un círculo)
        glow_c = tuple(min(255, c + 40) for c in glow_color)
        pygame.draw.circle(
            screen, glow_c, (int(self.x), int(self.y)), self.radius + 1, 1
        )

        # Pelota principal
        pygame.draw.circle(screen, main_color, (int(self.x), int(self.y)), self.radius)

        # Núcleo brillante (efecto de luz)
        core_color = tuple(min(255, c + 100) for c in main_color)
        pygame.draw.circle(
            screen, core_color, (int(self.x) - 2, int(self.y) - 2), max(2, self.radius // 3)
        )

        # Destruidor: anillo pulsante adicional
        if self.destroyer_mode:
            pulse_radius = self.radius + 3 + int(2 * math.sin(pygame.time.get_ticks() * 0.01))
            pygame.draw.circle(
                screen, (255, 150, 100), (int(self.x), int(self.y)), pulse_radius, 1
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
# CONFIGURACIÓN DE RESISTENCIA DE LADRILLOS
# ==========================================
# Mapeo de colores a resistencia (hits necesarios para destruir)
# Sistema simplificado: solo 1, 2 o 3 golpes máximo
BRICK_RESISTANCE = {
    (180, 40, 40): 3,    # Rojo oscuro metálico
    (180, 100, 30): 3,    # Naranja oxidado
    (160, 150, 50): 2,    # Oro antiguo
    (40, 140, 60): 2,     # Verde bronce
    (40, 100, 180): 1,    # Azul acero
    (120, 40, 160): 2,    # Púrpura oscuro
    (180, 60, 120): 1,    # Rosa oxidado
    (50, 140, 160): 1,    # Cian oscuro
}


# ==========================================
# FUNCIONES DE EFECTOS DE NEON
# ==========================================
def draw_glow_circle(screen, color, center, radius, glow_radius=15):
    """Dibuja un círculo con efecto de brillo neón"""
    # Capa de brillo exterior (difuminado)
    for i in range(glow_radius, 0, -1):
        alpha = int(80 * (1 - i / glow_radius))
        glow_color = tuple(min(255, c + 50) for c in color)
        pygame.draw.circle(
            screen,
            glow_color,
            center,
            radius + i,
            2
        )
    # Círculo principal
    pygame.draw.circle(screen, color, center, radius)


def draw_glow_rect(screen, color, rect, glow_size=8):
    """Dibuja un rectángulo con efecto de brillo neón"""
    x, y, width, height = rect
    # Capa de brillo exterior
    for i in range(glow_size, 0, -1):
        alpha = int(60 * (1 - i / glow_size))
        glow_color = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(
            screen,
            glow_color,
            (x - i, y - i, width + i * 2, height + i * 2),
            2
        )
    # Rectángulo principal
    pygame.draw.rect(screen, color, (x, y, width, height))


def draw_neon_line(screen, color, start, end, width=3, glow_size=10):
    """Dibuja una línea con efecto de brillo neón"""
    # Brillo exterior
    for i in range(glow_size, 0, -1):
        glow_color = tuple(min(255, c + 30) for c in color)
        pygame.draw.line(
            screen,
            glow_color,
            start,
            end,
            width + i * 2
        )
    # Línea principal
    pygame.draw.line(screen, color, start, end, width)
    # Línea central brillante
    bright_color = tuple(min(255, c + 100) for c in color)
    pygame.draw.line(screen, bright_color, start, end, max(1, width // 2))


def draw_glow_polygon(screen, color, points, glow_size=8):
    """Dibuja un polígono con efecto de brillo neón"""
    # Brillo exterior
    for i in range(glow_size, 0, -1):
        glow_color = tuple(min(255, c + 40) for c in color)
        scaled_points = []
        center_x = sum(p[0] for p in points) / len(points)
        center_y = sum(p[1] for p in points) / len(points)
        for px, py in points:
            dx, dy = px - center_x, py - center_y
            scale = 1 + i / 20
            scaled_points.append((center_x + dx * scale, center_y + dy * scale))
        pygame.draw.polygon(screen, glow_color, scaled_points, 2)
    # Polígono principal
    pygame.draw.polygon(screen, color, points)


# ==========================================
# CLASE BRICK (LADRILLO)
# ==========================================
class Brick:
    """
    Clase que representa un ladrillo destructible.
    Los ladrillos forman la estructura que el jugador debe destruir
    para completar el nivel.
    """

    def __init__(self, x, y, color, points=10):
        """
        Constructor del ladrillo.

        Parámetros:
        - x: posición horizontal (píxeles)
        - y: posición vertical (píxeles)
        - color: color del ladrillo (tupla RGB)
        - points: puntos que otorga al ser destruido (por defecto 10)
        """
        self.x = x  # Posición horizontal (esquina izquierda)
        self.y = y  # Posición vertical (esquina superior)

        # Dimensiones del ladrillo
        self.width = BRICK_WIDTH  # Ancho del ladrillo
        self.height = BRICK_HEIGHT  # Alto del ladrillo

        # Propiedades del juego
        self.color = color  # Color para dibujar el ladrillo
        self.destroyed = False  # Si el ladrillo fue destruido
        self.points = points  # Puntos que otorga al jugador

        # Sistema de resistencia
        self.max_hits = BRICK_RESISTANCE.get(color, 1)  # Resistencia según color
        self.current_hits = 0  # Hits recibidos actualmente
        self.original_color = color  # Color original para efectos visuales

        # Efecto visual cuando es golpeado
        self.hit_animation = 0  # Contador para animación de golpe

    def hit(self):
        """
        Registra un impacto en el ladrillo y verifica si debe ser destruido.

        Retorna:
        - bool: True si el ladrillo fue destruido, False si aún resiste
        """
        if not self.destroyed:  # Solo si no estaba ya destruido
            self.current_hits += 1  # Incrementar hits recibidos
            self.hit_animation = 20  # Iniciar animación de golpe

            # Actualizar color basado en el daño recibido
            self.update_color_by_damage()

            # Verificar si debe ser destruido
            if self.current_hits >= self.max_hits:
                self.destroyed = True  # Marcar como destruido
                return True  # Confirmar que fue destruido

            return False  # Aún no destruido, pero fue golpeado
        return False  # Ya estaba destruido

    def update_color_by_damage(self):
        """
        Actualiza el color del ladrillo basado en el daño recibido.
        Los ladrillos se oscurecen progresivamente conforme reciben daño.
        """
        if self.current_hits > 0 and self.max_hits > 1:
            # Calcular porcentaje de daño (0.0 a 1.0)
            damage_ratio = self.current_hits / self.max_hits

            # Oscurecer el color progresivamente
            darken_factor = 1.0 - (damage_ratio * 0.6)  # Oscurecer hasta 60%

            self.color = tuple(
                max(30, int(c * darken_factor)) for c in self.original_color
            )

    def update(self):
        """
        Actualiza el estado del ladrillo cada frame.
        Principalmente maneja la animación de destrucción.
        """
        # Reducir contador de animación si está activo
        if self.hit_animation > 0:
            self.hit_animation -= 1

    def draw(self, screen):
        """
        Dibuja el ladrillo con aspecto metálico profesional.
        """
        if not self.destroyed:
            # Efecto de pulso cuando es golpeado
            pulse = 1.0
            if self.hit_animation > 0:
                pulse = 1.0 + 0.15 * (self.hit_animation / 20)

            width = int(self.width * pulse)
            height = int(self.height * pulse)
            x = self.x - (width - self.width) // 2
            y = self.y - (height - self.height) // 2

            # Convertir color a tonalidad metálica (más oscuro con reflejos)
            base_r, base_g, base_b = self.color

            # Mezclar con gris para efecto metálico (40% color, 60% gris)
            metallic_factor = 0.4
            metal_r = int(base_r * metallic_factor + 60)
            metal_g = int(base_g * metallic_factor + 60)
            metal_b = int(base_b * metallic_factor + 60)

            # Gradiente vertical metálico (de arriba a abajo)
            for i in range(height):
                ratio = i / height
                # Brillo máximo en la parte superior, sombra en la inferior
                if ratio < 0.3:
                    # Parte superior brillante
                    brightness = 1.0 + (0.3 - ratio) * 0.8
                elif ratio > 0.7:
                    # Parte inferior oscura
                    brightness = 1.0 - (ratio - 0.7) * 1.2
                else:
                    brightness = 1.0

                # Añadir reflejos horizontales sutiles
                reflection = 0.0
                if 0.1 < ratio < 0.15 or 0.4 < ratio < 0.45:
                    reflection = 0.15

                r = min(255, int((metal_r + 40) * brightness + reflection * 80))
                g = min(255, int((metal_g + 40) * brightness + reflection * 80))
                b = min(255, int((metal_b + 40) * brightness + reflection * 80))

                pygame.draw.line(screen, (r, g, b), (x, y + i), (x + width - 1, y + i))

            # Borde exterior oscuro (marco metálico)
            dark_edge = (max(0, metal_r - 40), max(0, metal_g - 40), max(0, metal_b - 40))
            pygame.draw.rect(screen, dark_edge, (x - 1, y - 1, width + 2, height + 2), 1)

            # Borde superior e izquierdo brillante (reflejo de luz)
            light_edge = (min(255, metal_r + 80), min(255, metal_g + 80), min(255, metal_b + 80))
            pygame.draw.line(screen, light_edge, (x, y), (x + width - 1, y))
            pygame.draw.line(screen, light_edge, (x, y), (x, y + height - 1))

            # Borde inferior y derecho oscuro
            dark_line = (max(0, metal_r - 30), max(0, metal_g - 30), max(0, metal_b - 30))
            pygame.draw.line(screen, dark_line, (x, y + height - 1), (x + width - 1, y + height - 1))
            pygame.draw.line(screen, dark_line, (x + width - 1, y), (x + width - 1, y + height - 1))

            # Reflejos horizontales brillantes (líneas de拉伸 metálico)
            highlight_y = [int(height * 0.12), int(height * 0.42)]
            for hy in highlight_y:
                if hy < height - 1:
                    highlight_intensity = 0.3 if hy > 0 else 0.5
                    hr = min(255, int(metal_r + 100 * highlight_intensity))
                    hg = min(255, int(metal_g + 100 * highlight_intensity))
                    hb = min(255, int(metal_b + 100 * highlight_intensity))
                    pygame.draw.line(screen, (hr, hg, hb), (x + 2, y + hy), (x + width - 3, y + hy))

            # Indicador de resistencia
            if self.max_hits > 1:
                life_percentage = (self.max_hits - self.current_hits) / self.max_hits
                bar_width = int((width - 8) * life_percentage)
                bar_height = 3
                bar_x = x + 4
                bar_y = y + height - bar_height - 2

                # Fondo de la barra metálico
                pygame.draw.rect(screen, (40, 40, 50), (bar_x - 1, bar_y - 1, width - 6, bar_height + 2))

                # Barra de vida
                if life_percentage > 0.6:
                    bar_color = (150, 220, 150)
                elif life_percentage > 0.3:
                    bar_color = (220, 220, 100)
                else:
                    bar_color = (220, 100, 100)

                if bar_width > 0:
                    # Borde brillante de la barra
                    pygame.draw.rect(screen, (min(255, bar_color[0] + 50), min(255, bar_color[1] + 50), min(255, bar_color[2] + 50)),
                                    (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
                    pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width, bar_height))

                # Número de hits restantes
                if self.max_hits <= 8:
                    hits_left = self.max_hits - self.current_hits
                    font = pygame.font.Font(None, 14)
                    text_color = (min(255, metal_r + 80), min(255, metal_g + 80), min(255, metal_b + 80))
                    text_surface = font.render(str(hits_left), True, text_color)
                    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2 - 3))
                    screen.blit(text_surface, text_rect)

    def get_rect(self):
        """
        Devuelve un rectángulo pygame que representa el ladrillo.
        Útil para detección de colisiones.

        Retorna:
        - pygame.Rect: rectángulo con posición y dimensiones del ladrillo
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ==========================================
# CLASE POWERUP (MEJORA ESPECIAL)
# ==========================================
class PowerUp:
    """
    Clase que representa los power-ups (mejoras especiales) del juego.
    Los power-ups aparecen aleatoriamente cuando se destruyen ladrillos
    y otorgan habilidades temporales al jugador.
    """

    def __init__(self, x, y, power_type):
        """
        Constructor del power-up.

        Parámetros:
        - x: posición horizontal inicial (píxeles)
        - y: posición vertical inicial (píxeles)
        - power_type: tipo de mejora ('expand', 'multi_ball', 'slow_ball', 'fast_paddle')
        """
        self.x = x  # Posición horizontal (centro)
        self.y = y  # Posición vertical (centro)

        # Dimensiones del power-up
        self.width = 30  # Ancho del power-up
        self.height = 15  # Alto del power-up

        # Propiedades de movimiento
        self.speed = 3  # Velocidad de caída (píxeles por frame)
        self.rotation = 0  # Ángulo de rotación para efecto visual

        # Propiedades del juego
        self.power_type = power_type  # Tipo de mejora que otorga
        self.active = True  # Si el power-up sigue activo en pantalla

    def move(self):
        """
        Mueve el power-up hacia abajo y lo rota para efecto visual.
        Desactiva el power-up si sale de la pantalla.
        """
        self.y += self.speed  # Mover hacia abajo
        self.rotation += 5  # Incrementar rotación para animación

        # Desactivar si sale de la pantalla por abajo
        if self.y > WINDOW_HEIGHT:
            self.active = False

    def draw(self, screen):
        """
        Dibuja el power-up en la pantalla con efectos de brillo neón profesionales.
        """
        if self.active:
            # Diccionario de colores neón para cada tipo de power-up
            colors = {
                "expand": NEON_GREEN,
                "multi_ball": NEON_YELLOW,
                "slow_ball": NEON_PURPLE,
                "destroyer_ball": NEON_RED,
                "laser_shoot": NEON_ORANGE,
            }
            color = colors.get(self.power_type, NEON_CYAN)

            # Diccionario de símbolos para cada tipo
            symbols = {
                "expand": "E",
                "multi_ball": "M",
                "slow_ball": "S",
                "destroyer_ball": "D",
                "laser_shoot": "L",
            }
            symbol = symbols.get(self.power_type, "?")

            # Centro del power-up
            center_x, center_y = self.x + self.width // 2, self.y + self.height // 2

            # Glow exterior fino (solo un polígono)
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.005 + self.rotation * 0.1)) * 0.3 + 0.7
            glow_color = tuple(min(255, c + 40) for c in color)
            glow_points = []
            for j in range(6):
                angle = math.radians(self.rotation + j * 60)
                px = center_x + math.cos(angle) * 16
                py = center_y + math.sin(angle) * 12
                glow_points.append((px, py))
            pygame.draw.polygon(screen, glow_color, glow_points, 1)

            # Crear hexágono principal
            points = []
            for i in range(6):
                angle = math.radians(self.rotation + i * 60)
                px = center_x + math.cos(angle) * 14
                py = center_y + math.sin(angle) * 10
                points.append((px, py))

            # Dibujar hexágono con brillo
            bright_color = tuple(min(255, c + 50) for c in color)
            pygame.draw.polygon(screen, bright_color, points)

            # Borde exterior
            pygame.draw.polygon(screen, color, points, 1)

            # Interior oscuro
            inner_points = []
            for i in range(6):
                angle = math.radians(self.rotation + i * 60)
                px = center_x + math.cos(angle) * 9
                py = center_y + math.sin(angle) * 6
                inner_points.append((px, py))
            dark_color = tuple(max(0, c - 30) for c in color)
            pygame.draw.polygon(screen, dark_color, inner_points)

            # Dibujar símbolo identificativo en el centro
            font = pygame.font.Font(None, 20)
            text = font.render(symbol, True, BLACK)
            text_rect = text.get_rect(center=(center_x, center_y))
            # Borde brillante del texto (más fino)
            pygame.draw.circle(screen, bright_color, (center_x, center_y), 9)
            screen.blit(text, text_rect)

    def get_rect(self):
        """
        Devuelve un rectángulo pygame que representa el power-up.
        Útil para detección de colisiones con la paleta.

        Retorna:
        - pygame.Rect: rectángulo con posición y dimensiones del power-up
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ==========================================
# CLASE LASER (PROYECTIL LÁSER)
# ==========================================
class Laser:
    """
    Clase que representa un proyectil láser disparado por la paleta.
    Los láser viajan hacia arriba y destruyen ladrillos al impactar.
    """

    def __init__(self, x, y):
        """
        Constructor del láser.

        Parámetros:
        - x: posición horizontal inicial (píxeles)
        - y: posición vertical inicial (píxeles)
        """
        self.x = x  # Posición horizontal del láser
        self.y = y  # Posición vertical del láser

        # Dimensiones del láser
        self.width = 3  # Ancho del láser (delgado)
        self.height = 10  # Alto del láser

        # Velocidad de movimiento
        self.speed = 8  # Velocidad hacia arriba (píxeles por frame)

        # Estado del láser
        self.active = True  # Si el láser sigue activo

        # Efectos visuales
        self.trail = []  # Rastro visual del láser
        self.trail_length = 5  # Longitud del rastro

        # Nuevo código sugerido
        self.collision_cooldown = 0  # Timer de cooldown
        self.last_hit_brick = None  # Último ladrillo golpeado

    def move(self):
        """
        Mueve el láser hacia arriba y mantiene el rastro visual.
        """
        # Guardar posición actual en el rastro
        self.trail.append((self.x + self.width // 2, self.y + self.height // 2))

        # Limitar el tamaño del rastro
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

        # Mover el láser hacia arriba
        self.y -= self.speed

        # Desactivar si sale de la pantalla
        if self.y < 0:
            self.active = False

    def draw(self, screen):
        """
        Dibuja el láser en la pantalla con efectos de brillo neón profesionales.
        """
        if self.active:
            laser_color = NEON_RED
            bright_color = (255, 150, 150)

            # Glow exterior fino
            center_x = self.x + self.width // 2
            glow_color = tuple(min(255, c + 30) for c in laser_color)
            pygame.draw.rect(
                screen, glow_color,
                (center_x - 1, self.y - 1, 3, self.height + 2),
                1
            )

            # Láser principal
            pygame.draw.rect(
                screen, laser_color, (self.x, self.y, self.width, self.height)
            )

            # Núcleo brillante
            pygame.draw.rect(
                screen, bright_color, (self.x + 1, self.y, 1, self.height)
            )

            # Punto de energía en la punta
            pygame.draw.circle(
                screen, bright_color, (center_x, self.y), 2
            )

    def get_rect(self):
        """
        Devuelve un rectángulo pygame que representa el láser.
        Útil para detección de colisiones.

        Retorna:
        - pygame.Rect: rectángulo con posición y dimensiones del láser
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ==========================================
# CLASE GAME (JUEGO PRINCIPAL)
# ==========================================
class Game:
    """
    Clase principal que maneja todo el juego de Arkanoid.
    Controla el estado del juego, los objetos, la lógica y el renderizado.
    Esta es la clase más importante - coordina todo lo demás.
    """

    def __init__(self):
        """
        Constructor del juego. Inicializa pygame y configura el estado inicial.
        """
        # Configurar ventana del juego
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Arkanoid - Edición Mejorada")
        self.clock = pygame.time.Clock()  # Para controlar framerate (60 FPS)

        # Variables del estado del juego
        self.score = 0  # Puntuación actual del jugador
        self.lives = (
            10  # Vidas restantes del jugador (aumentadas para facilitar el juego)
        )
        self.level = 1  # Nivel actual del juego
        self.high_score = self.load_high_score()  # Puntuación máxima guardada

        # Configurar fuentes para el texto en pantalla
        self.font = pygame.font.Font(None, 36)  # Fuente mediana
        self.small_font = pygame.font.Font(None, 24)  # Fuente pequeña
        self.big_font = pygame.font.Font(None, 48)  # Fuente grande

        # Estados y efectos visuales
        self.game_state = (
            "menu"  # Estado actual: 'menu', 'playing', 'game_over', 'victory'
        )
        self.particles = []  # Lista de partículas para efectos visuales
        self.screen_shake = 0  # Contador para efecto de temblor de pantalla

        # Estado de pausa
        self.paused = False  # Indica si el juego está pausado

        # Power-ups activos (tipo -> tiempo restante en frames)
        self.active_power_ups = {
            "expand": 0,
            "multi_ball": 0,
            "slow_ball": 0,
            "destroyer_ball": 0,
            "laser_shoot": 0
        }

        # Control del juego
        self.mouse_control = True  # Control con ratón habilitado por defecto
        self.waiting_for_ball_release = False  # Si estamos esperando liberar la pelota

        # Sistema de sonido
        self.sound_manager = sounds.get_sound_manager()

        # Crear estrellas de fondo aleatoriamente
        self.background_stars = [
            (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            for _ in range(50)  # 50 estrellas en posiciones aleatorias
        ]

        # Inicializar el juego
        self.reset_game()

        # Capturar el mouse al inicio
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mouse_captured = True

    def load_high_score(self):
        """
        Carga la puntuación máxima desde un archivo.
        Si el archivo no existe, devuelve 0.

        Retorna:
        - int: puntuación máxima guardada
        """
        try:
            # Intentar abrir y leer el archivo de puntuación máxima
            with open("high_score.txt", "r") as f:
                return int(f.read().strip())  # Leer y convertir a entero
        except:
            # Si hay cualquier error (archivo no existe, formato incorrecto, etc.)
            return 0  # Devolver 0 como puntuación por defecto

    def save_high_score(self):
        """
        Guarda la puntuación máxima actual en un archivo.
        """
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))  # Escribir puntuación como texto

    def reset_game(self):
        """
        Reinicia el juego a su estado inicial.
        Crea nuevos objetos para empezar un nivel limpio.
        """
        # Crear paleta centrada en la parte inferior
        self.paddle = Paddle(WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, WINDOW_HEIGHT - 55)

        # Crear una pelota pegada a la paleta
        ball_x = self.paddle.x + self.paddle.width // 2
        ball_y = self.paddle.y - BALL_SIZE // 2 - 2
        self.balls = [Ball(ball_x, ball_y, stuck_to_paddle=True)]
        self.balls[0].game_sound_manager = self.sound_manager
        self.waiting_for_ball_release = True

        # Limpiar listas de objetos
        self.bricks = []  # Lista vacía de ladrillos
        self.power_ups = []  # Lista vacía de power-ups
        self.particles = []  # Lista vacía de partículas
        self.lasers = []  # Lista vacía de láser

        # Resetear power-ups activos
        self.active_power_ups = {
            "expand": 0,
            "multi_ball": 0,
            "slow_ball": 0,
            "destroyer_ball": 0,
            "laser_shoot": 0
        }

        # Resetear paleta a estado normal
        self.paddle.width = PADDLE_WIDTH  # Tamaño normal
        self.paddle.expand_timer = 0  # Sin expansión
        self.paddle.laser_active = False  # Sin láser
        self.paddle.laser_timer = 0  # Sin timer de láser

        # Resetear estado de pelotas
        for ball in self.balls:
            ball.destroyer_mode = False  # Desactivar modo destructor
            ball.destroyer_timer = 0  # Sin timer de destructor

        # Crear la estructura de ladrillos para el nivel
        self.create_bricks()

    def create_new_ball(self):
        """
        Crea una nueva pelota pegada a la paleta cuando se pierde una vida.
        """
        ball_x = self.paddle.x + self.paddle.width // 2
        ball_y = self.paddle.y - BALL_SIZE // 2 - 2
        new_ball = Ball(ball_x, ball_y, stuck_to_paddle=True)
        new_ball.game_sound_manager = self.sound_manager
        self.balls = [new_ball]
        self.waiting_for_ball_release = True

    def create_bricks(self):
        """
        Crea la estructura de ladrillos para el nivel actual usando patrones originales.
        Cada nivel tiene un patrón único inspirado en el Arkanoid original.
        """
        self.bricks = []  # Empezar con lista vacía

        # Obtener el patrón del nivel actual (cicla si excede los niveles disponibles)
        level_index = (self.level - 1) % len(ORIGINAL_LEVELS)
        level_pattern = ORIGINAL_LEVELS[level_index]

        # Calcular posición inicial para centrar la cuadrícula de ladrillos
        start_x = (WINDOW_WIDTH - BRICK_COLS * BRICK_WIDTH) // 2
        start_y = 60  # Empezar 60 píxeles desde arriba

        # Crear ladrillos según el patrón del nivel
        for row in range(len(level_pattern)):  # Para cada fila en el patrón
            for col in range(len(level_pattern[row])):  # Para cada columna en la fila
                brick_type = level_pattern[row][col]  # Obtener tipo de ladrillo (0-8)

                # Solo crear ladrillo si no es espacio vacío (0)
                if brick_type > 0:
                    # Calcular posición del ladrillo
                    x = start_x + col * BRICK_WIDTH  # Posición horizontal
                    y = start_y + row * BRICK_HEIGHT  # Posición vertical

                    # Asignar color basado en el tipo de ladrillo
                    color = BRICK_COLORS[(brick_type - 1) % len(BRICK_COLORS)]

                    # Asignar puntos basados en el tipo de ladrillo y nivel
                    # Los ladrillos superiores (menor número de fila) dan más puntos
                    base_points = brick_type * 10
                    level_bonus = self.level * 5  # Bonus por nivel
                    points = base_points + level_bonus

                    # Crear y agregar el ladrillo a la lista
                    brick = Brick(x, y, color, points)
                    self.bricks.append(brick)

    def add_particles(self, x, y, color, count=10):
        """
        Agrega partículas en una posición específica para efectos visuales.

        Parámetros:
        - x: posición horizontal donde crear las partículas
        - y: posición vertical donde crear las partículas
        - color: color de las partículas (tupla RGB)
        - count: número de partículas a crear (por defecto 10)
        """
        for _ in range(count):
            # Crear una nueva partícula en la posición especificada
            self.particles.append(Particle(x, y, color))

    def handle_events(self):
        """
        Maneja todos los eventos de entrada del usuario (teclado, ratón, cerrar ventana, etc.).

        Retorna:
        - bool: False si el usuario quiere salir del juego, True si continúa
        """
        global BALL_SPEED  # Declarar global para poder modificar la velocidad de la pelota
        # Procesar todos los eventos en la cola
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Usuario cerró la ventana
                return False
            elif event.type == pygame.KEYDOWN:  # Usuario presionó una tecla
                if event.key == pygame.K_SPACE:  # Tecla Espacio
                    if self.game_state == "menu":
                        self.game_state = "playing"  # Empezar juego
                        # Reproducir sonido de inicio
                        self.sound_manager.play('power_up')
                    elif self.game_state == "playing" and self.waiting_for_ball_release:
                        # Liberar la pelota pegada
                        for ball in self.balls:
                            if ball.stuck_to_paddle:
                                ball.release()
                        self.waiting_for_ball_release = False
                    elif self.game_state == "game_over":
                        # Reiniciar completamente el juego
                        self.score = 0
                        self.lives = 10  # Reiniciar con 10 vidas
                        self.level = 1
                        BALL_SPEED = INITIAL_BALL_SPEED  # Resetear velocidad de pelota
                        self.reset_game()
                        self.game_state = "playing"
                    elif self.game_state == "victory":
                        self.level += 1
                        # Reproducir sonido de nivel completado
                        self.sound_manager.play('level_complete')
                        # Aumentar dificultad gradualmente
                        BALL_SPEED += 0.05  # Incremento muy suave de velocidad
                        self.reset_game()
                        self.game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    if self.mouse_captured:
                        pygame.event.set_grab(False)
                        pygame.mouse.set_visible(True)
                        self.mouse_captured = False
                    else:
                        pygame.event.set_grab(True)
                        pygame.mouse.set_visible(False)
                        self.mouse_captured = True
                elif event.key == pygame.K_b:  # Tecla B para agregar pelota
                    if self.game_state == "playing" and len(self.balls) < 5:
                        # Crear nueva pelota en posición aleatoria segura
                        new_ball = Ball(
                            random.randint(100, WINDOW_WIDTH - 100),
                            random.randint(200, WINDOW_HEIGHT // 2),
                        )
                        # Asignar velocidad aleatoria
                        angle = random.uniform(-math.pi / 3, math.pi / 3)
                        new_ball.speed_x = BALL_SPEED * math.sin(angle)
                        new_ball.speed_y = -BALL_SPEED * math.cos(angle)
                        # Asignar referencia del gestor de sonidos
                        new_ball.game_sound_manager = self.sound_manager
                        # Si destroyer_ball está activo, aplicar modo destructor a la nueva pelota
                        if self.active_power_ups.get("destroyer_ball", 0) > 0:
                            new_ball.destroyer_mode = True
                            new_ball.destroyer_timer = self.active_power_ups["destroyer_ball"]
                        self.balls.append(new_ball)
                        # Efectos visuales
                        self.add_particles(new_ball.x, new_ball.y, WHITE, 8)
                elif event.key == pygame.K_p:  # Tecla P para pausar/reanudar
                    if self.game_state == "playing":
                        self.paused = not self.paused  # Alternar estado de pausa
                elif event.key == pygame.K_l:  # Tecla L para activar láser temporal
                    if self.game_state == "playing":
                        self.paddle.activate_laser()  # Activar láser por tiempo limitado
                elif event.key == pygame.K_e:  # Tecla E -> power-up expand
                    if self.game_state == "playing":
                        self.apply_power_up("expand")
                elif event.key == pygame.K_m:  # Tecla M -> power-up multi_ball
                    if self.game_state == "playing":
                        self.apply_power_up("multi_ball")
                elif event.key == pygame.K_s:  # Tecla S -> power-up slow_ball
                    if self.game_state == "playing":
                        self.apply_power_up("slow_ball")
                elif event.key == pygame.K_d:  # Tecla D -> power-up destroyer_ball
                    if self.game_state == "playing":
                        self.apply_power_up("destroyer_ball")
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Usuario hizo clic
                if event.button == 1:  # Clic izquierdo
                    if self.game_state == "playing":
                        # Liberar la pelota pegada si hay alguna
                        if self.waiting_for_ball_release:
                            for ball in self.balls:
                                if ball.stuck_to_paddle:
                                    ball.release()
                            self.waiting_for_ball_release = False

                        # Disparar láser si está disponible
                        if self.paddle.can_shoot():
                            new_lasers = self.paddle.shoot()
                            if new_lasers:
                                self.lasers.extend(new_lasers)
        return True

    def update(self):
        # No actualizar lógica del juego si no estamos jugando o si está pausado
        if self.game_state != "playing" or (self.game_state == "playing" and self.paused):
            return

        # Actualizar posición de la paleta con el ratón
        if self.mouse_control:
            mouse_x, _ = pygame.mouse.get_pos()
            self.paddle.update_mouse_position(mouse_x)

        # Actualizar paleta
        self.paddle.update()

        # Mover paleta con teclado (por compatibilidad)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move_right()

        # Disparar láser con barra espaciadora
        if keys[pygame.K_SPACE] and self.paddle.can_shoot():
            # Si hay pelota pegada, también la liberamos al disparar
            if self.waiting_for_ball_release:
                for ball in self.balls:
                    if ball.stuck_to_paddle:
                        ball.release()
                self.waiting_for_ball_release = False

            new_lasers = self.paddle.shoot()
            if new_lasers:
                self.lasers.extend(new_lasers)  # Agregar todos los láser a la lista
                # Reproducir sonido de láser
                self.sound_manager.play('laser')

        # Disparar láser con ratón (disparo continuo)
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.paddle.can_shoot():  # Botón izquierdo presionado
            new_lasers = self.paddle.shoot()
            if new_lasers:
                self.lasers.extend(new_lasers)

        # Actualizar posición de pelotas pegadas a la paleta
        for ball in self.balls:
            if ball.stuck_to_paddle:
                ball.update_stuck_position(self.paddle)

        # Mover pelotas
        balls_to_remove = []
        for i, ball in enumerate(self.balls):
            ball.move()

            # Colisión con paredes
            if ball.check_wall_collision():
                balls_to_remove.append(i)
                continue

            # Colisión con paleta (solo si no está pegada)
            if not ball.stuck_to_paddle and ball.check_paddle_collision(self.paddle):
                self.add_particles(ball.x, ball.y, BLUE, 5)

            # Colisión con ladrillos (solo si no está pegada)
            if not ball.stuck_to_paddle:
                ball_rect = ball.get_rect()
                for brick in self.bricks:
                    if not brick.destroyed and ball_rect.colliderect(brick.get_rect()):
                        # Solo procesar hit si no hay cooldown o es un ladrillo diferente
                        if ball.collision_cooldown <= 0 or ball.last_hit_brick != brick:
                            # Establecer cooldown ANTES de procesar el hit
                            ball.collision_cooldown = (
                                30  # 30 frames de cooldown (0.5 segundos)
                            )
                            ball.last_hit_brick = brick

                            # Procesar el hit al ladrillo
                            if ball.destroyer_mode:
                                # En modo destructor, destruir ladrillo inmediatamente
                                brick.destroyed = True
                                brick_destroyed = True
                                ball.bounce_y()
                                self.screen_shake = 8  # Más sacudida para efecto visual
                            else:
                                # Comportamiento normal
                                brick_destroyed = brick.hit()
                                ball.bounce_y()
                                self.screen_shake = 5

                            # Efectos de partículas
                            self.add_particles(
                                brick.x + brick.width // 2,
                                brick.y + brick.height // 2,
                                brick.color,
                                15,
                            )

                            # Solo dar puntos y generar power-up si el ladrillo fue destruido
                            if brick_destroyed:
                                self.score += brick.points
                                # Reproducir sonido de destrucción
                                self.sound_manager.play('brick_destroy')
                                # Posibilidad de generar power-up (reducida)
                                if (
                                    random.random() < 0.15
                                ):  # 15% de probabilidad (reducida desde 35%)
                                    power_types = [
                                        "expand",
                                        "multi_ball",
                                        "slow_ball",
                                        "destroyer_ball",  # Nuevo power-up bola destructora
                                        "laser_shoot",  # Power-up de disparo
                                    ]
                                    power_type = random.choice(power_types)
                                    power_up = PowerUp(
                                        brick.x + brick.width // 2, brick.y, power_type
                                    )
                                    self.power_ups.append(power_up)
                            else:
                                # Sonido de rebote en ladrillo
                                self.sound_manager.play('brick_hit')
                        break

        # Remover pelotas que salieron
        for i in reversed(balls_to_remove):
            self.balls.pop(i)

        # Si no quedan pelotas, perder vida
        if not self.balls:
            self.lives -= 1
            self.screen_shake = 15
            # Reproducir sonido de perder vida
            self.sound_manager.play('life_lost')
            if self.lives <= 0:
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                self.game_state = "game_over"
                # Reproducir sonido de game over
                self.sound_manager.play('game_over')
            else:
                # Crear nueva pelota pegada a la paleta
                self.create_new_ball()

        # Actualizar ladrillos
        for brick in self.bricks:
            brick.update()

        # Mover power-ups
        power_ups_to_remove = []
        for i, power_up in enumerate(self.power_ups):
            power_up.move()
            if not power_up.active:
                power_ups_to_remove.append(i)
            elif power_up.get_rect().colliderect(self.paddle.get_rect()):
                self.apply_power_up(power_up.power_type)
                power_ups_to_remove.append(i)
                self.add_particles(power_up.x, power_up.y, GREEN, 8)
                # Reproducir sonido de power-up
                self.sound_manager.play('power_up')

        for i in reversed(power_ups_to_remove):
            self.power_ups.pop(i)

        # Mover láser y detectar colisiones
        lasers_to_remove = []
        for i, laser in enumerate(self.lasers):
            laser.move()

            # Remover láser si sale de pantalla
            if not laser.active:
                lasers_to_remove.append(i)
                continue

            # Colisión de láser con ladrillos
            laser_rect = laser.get_rect()
            for brick in self.bricks:
                if not brick.destroyed and laser_rect.colliderect(brick.get_rect()):
                    if brick.hit():
                        # Destruir láser al impactar
                        lasers_to_remove.append(i)

                        # Añadir puntos
                        self.score += brick.points
                        # Reproducir sonido de destrucción por láser
                        self.sound_manager.play('brick_destroy')

                        # Efectos de partículas
                        self.add_particles(
                            brick.x + brick.width // 2,
                            brick.y + brick.height // 2,
                            brick.color,
                            10,
                        )

                        # Posibilidad de generar power-up
                        if random.random() < 0.15:
                            power_types = [
                                "expand",
                                "multi_ball",
                                "slow_ball",
                                "destroyer_ball",
                                "laser_shoot",
                            ]
                            power_type = random.choice(power_types)
                            power_up = PowerUp(
                                brick.x + brick.width // 2, brick.y, power_type
                            )
                            self.power_ups.append(power_up)
                    else:
                        # Sonido de impacto de láser en ladrillo
                        self.sound_manager.play('brick_hit')
                    break

        # Remover láser destruidos
        for i in reversed(lasers_to_remove):
            self.lasers.pop(i)

        # Actualizar partículas
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()

        # Reducir temblor de pantalla
        if self.screen_shake > 0:
            self.screen_shake -= 1

        # Decrementar timers de power-ups activos
        for power_type in self.active_power_ups:
            if self.active_power_ups[power_type] > 0:
                self.active_power_ups[power_type] -= 1

        # Sincronizar velocidades de todas las pelotas cada cierto tiempo
        if pygame.time.get_ticks() % 60 == 0:  # Cada segundo aproximadamente
            self.sync_ball_speeds()

        # Verificar victoria
        if all(brick.destroyed for brick in self.bricks):
            self.game_state = "victory"
            # Reproducir sonido de victoria
            self.sound_manager.play('victory')

    def sync_ball_speeds(self):
        """
        Sincroniza las velocidades de todas las pelotas para que tengan la misma velocidad.
        Usa la velocidad de la primera pelota como referencia.
        """
        if len(self.balls) > 1:
            # Usar la velocidad de la primera pelota como referencia
            reference_speed = math.sqrt(self.balls[0].speed_x**2 + self.balls[0].speed_y**2)

            for ball in self.balls[1:]:  # Empezar desde la segunda pelota
                current_speed = math.sqrt(ball.speed_x**2 + ball.speed_y**2)
                if current_speed > 0 and abs(current_speed - reference_speed) > 0.1:
                    # Ajustar velocidad si hay diferencia significativa (>0.1 píxeles/frame)
                    factor = reference_speed / current_speed
                    ball.speed_x *= factor
                    ball.speed_y *= factor

    def apply_power_up(self, power_type):
        if power_type == "expand":
            self.paddle.expand()
            self.active_power_ups["expand"] = 600  # 10 segundos
        elif power_type == "multi_ball":
            if len(self.balls) > 0 and len(self.balls) < 5:  # Verificar que hay pelotas y no exceder máximo
                for _ in range(2):
                    new_ball = Ball(self.balls[0].x, self.balls[0].y)
                    angle = random.uniform(-math.pi / 4, math.pi / 4)
                    speed = BALL_SPEED
                    new_ball.speed_x = speed * math.sin(angle)
                    new_ball.speed_y = -speed * math.cos(angle)
                    # Si destroyer_ball está activo, aplicar modo destructor a la nueva pelota
                    if self.active_power_ups.get("destroyer_ball", 0) > 0:
                        new_ball.destroyer_mode = True
                        new_ball.destroyer_timer = self.active_power_ups["destroyer_ball"]
                    self.balls.append(new_ball)
                    # Asignar referencia del gestor de sonidos
                    new_ball.game_sound_manager = self.sound_manager
            self.active_power_ups["multi_ball"] = 1800  # 30 segundos (tiempo arbitrario)
            # Reproducir sonido específico de multi_ball
            self.sound_manager.play('multi_ball')
        elif power_type == "slow_ball":
            # Calcular la velocidad promedio de todas las pelotas para mantener consistencia
            if self.balls:
                total_speed = 0
                for ball in self.balls:
                    ball_speed = math.sqrt(ball.speed_x**2 + ball.speed_y**2)
                    total_speed += ball_speed
                avg_speed = total_speed / len(self.balls)

                # Aplicar relentización manteniendo la dirección
                new_speed = max(avg_speed * 0.7, MIN_BALL_SPEED)

                for ball in self.balls:
                    current_speed = math.sqrt(ball.speed_x**2 + ball.speed_y**2)
                    if current_speed > 0:  # Evitar división por cero si la pelota está quieta
                        factor = new_speed / current_speed
                        ball.speed_x *= factor
                        ball.speed_y *= factor
            self.active_power_ups["slow_ball"] = 1800  # 30 segundos (tiempo arbitrario)
        elif power_type == "destroyer_ball":
            # Activar modo destructor para todas las pelotas por 10 segundos
            for ball in self.balls:
                ball.destroyer_mode = True
                ball.destroyer_timer = 2000  # 20 segundos a 60 FPS
            self.active_power_ups["destroyer_ball"] = 2000  # 20 segundos
        elif power_type == "laser_shoot":
            self.paddle.activate_laser()
            self.active_power_ups["laser_shoot"] = 2000  # 20 segundos

    def draw_background(self):
        """Dibuja el fondo con efecto de rejilla neón cyberpunk."""
        # Fondo oscuro base
        self.screen.fill(DARKER_BLUE)

        # Dibujar líneas de rejilla neón
        grid_color = (20, 20, 60)  # Color sutil de la rejilla
        grid_spacing = 40  # Espacio entre líneas

        # Líneas horizontales
        for y in range(0, WINDOW_HEIGHT, grid_spacing):
            pygame.draw.line(
                self.screen,
                grid_color,
                (0, y),
                (WINDOW_WIDTH, y),
                1
            )

        # Líneas verticales
        for x in range(0, WINDOW_WIDTH, grid_spacing):
            pygame.draw.line(
                self.screen,
                grid_color,
                (x, 0),
                (x, WINDOW_HEIGHT),
                1
            )

        # Efecto de brillo en el horizonte (línea horizontal brillante)
        horizon_y = WINDOW_HEIGHT - 100
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.001)) * 0.3 + 0.5
        horizon_color = (0, int(80 * pulse), int(100 * pulse))
        pygame.draw.line(
            self.screen,
            horizon_color,
            (0, horizon_y),
            (WINDOW_WIDTH, horizon_y),
            2
        )

        # Dibujar algunas estrellas brillantes
        for star_x, star_y in self.background_stars:
            # Solo dibujar algunas estrellas (no todas)
            if hash((star_x, star_y)) % 3 == 0:
                # Efecto de brillo pulsante
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.002 + star_x * 0.1)) * 0.5 + 0.5
                brightness = int(100 + 100 * pulse)
                color = (brightness // 2, brightness // 2, brightness)
                pygame.draw.circle(self.screen, color, (star_x, star_y), 1 + int(pulse))

        # Efecto de temblor de pantalla
        if self.screen_shake > 0:
            offset_x = random.randint(-self.screen_shake, self.screen_shake)
            offset_y = random.randint(-self.screen_shake, self.screen_shake)
            # Aplicar offset a todos los elementos (simplificado)

    def draw(self):
        self.draw_background()

        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "victory":
            self.draw_victory()

        pygame.display.flip()

    def draw_menu(self):
        """Dibuja el menú con efectos neón profesionales."""
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.003)) * 0.3 + 0.7

        # Título con efecto de brillo neón (posicionado más arriba)
        title_y = 80
        title_glow = self.big_font.render("ARKANOID", True, (int(100 * pulse), int(255 * pulse), int(255 * pulse)))
        title_glow_rect = title_glow.get_rect(
            center=(WINDOW_WIDTH // 2 + 2, title_y + 2)
        )
        self.screen.blit(title_glow, title_glow_rect)

        title = self.big_font.render("ARKANOID", True, NEON_CYAN)
        title_rect = title.get_rect(
            center=(WINDOW_WIDTH // 2, title_y)
        )
        self.screen.blit(title, title_rect)

        # Subtítulo
        subtitle_y = title_y + 50
        subtitle = self.font.render("EDICIÓN MEJORADA", True, WHITE)
        subtitle_rect = subtitle.get_rect(
            center=(WINDOW_WIDTH // 2, subtitle_y)
        )
        subtitle_glow = self.font.render("EDICIÓN MEJORADA", True, NEON_PURPLE)
        self.screen.blit(subtitle_glow, (subtitle_rect.x + 1, subtitle_rect.y + 1))
        self.screen.blit(subtitle, subtitle_rect)

        # Línea decorativa
        line_y = subtitle_y + 30
        line_color = tuple(int(c * pulse) for c in NEON_CYAN)
        pygame.draw.line(
            self.screen,
            line_color,
            (WINDOW_WIDTH // 2 - 150, line_y),
            (WINDOW_WIDTH // 2 + 150, line_y),
            1
        )

        # Instrucciones (organizadas en columnas)
        start_y = line_y + 25
        spacing = 22

        instructions = [
            ("ESPACIO - Comenzar", NEON_GREEN),
            ("Ratón o ←/→/A/D - Mover", WHITE),
            ("CLIC/ESPACIO - Lanzar", WHITE),
            ("CLIC sostenido - Disparar", WHITE),
            ("B - Pelota extra", WHITE),
            ("P - Pausar", WHITE),
            ("L - Activar láser", WHITE),
            ("E - Expandir paleta", NEON_GREEN),
            ("M - Multiplicar pelotas", NEON_YELLOW),
            ("S - Ralentizar", NEON_PURPLE),
            ("D - Modo destructor", NEON_RED),
        ]

        for i, (instruction, color) in enumerate(instructions):
            text = self.small_font.render(instruction, True, color)
            text_rect = text.get_rect(
                center=(WINDOW_WIDTH // 2, start_y + i * spacing)
            )
            self.screen.blit(text, text_rect)

        # Información adicional
        info_y = start_y + len(instructions) * spacing + 15
        info_text = self.small_font.render("36 niveles - Recoge power-ups", True, WHITE)
        info_rect = info_text.get_rect(center=(WINDOW_WIDTH // 2, info_y))
        self.screen.blit(info_text, info_rect)

        # Puntuación máxima
        score_text = self.small_font.render(f"Récord: {self.high_score}", True, NEON_YELLOW)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, info_y + 25))
        self.screen.blit(score_text, score_rect)

    def draw_game(self):
        """Dibuja el juego con UI neón profesional."""
        # Dibujar elementos del juego
        self.paddle.draw(self.screen)

        for ball in self.balls:
            ball.draw(self.screen)

        for brick in self.bricks:
            brick.draw(self.screen)

        for power_up in self.power_ups:
            power_up.draw(self.screen)

        for laser in self.lasers:
            laser.draw(self.screen)

        # Dibujar partículas
        for particle in self.particles:
            particle.draw(self.screen)

        # Panel de UI con borde neón
        ui_panel_x, ui_panel_y = 5, 5
        ui_panel_width, ui_panel_height = 180, 80

        # Borde brillante del panel
        pygame.draw.rect(self.screen, (30, 30, 60), (ui_panel_x, ui_panel_y, ui_panel_width, ui_panel_height), border_radius=5)
        pygame.draw.rect(self.screen, NEON_CYAN, (ui_panel_x, ui_panel_y, ui_panel_width, ui_panel_height), 2, border_radius=5)

        # UI con colores neón
        score_text = self.small_font.render(f"PUNTOS: {self.score}", True, NEON_GREEN)
        self.screen.blit(score_text, (15, 12))

        lives_text = self.small_font.render(f"VIDAS: {self.lives}", True, NEON_RED)
        self.screen.blit(lives_text, (15, 35))

        level_text = self.small_font.render(f"NIVEL: {self.level}", True, WHITE)
        self.screen.blit(level_text, (15, 58))

        # Panel derecho
        right_panel_x = WINDOW_WIDTH - 200
        pygame.draw.rect(self.screen, (30, 30, 60), (right_panel_x, 5, 195, 80), border_radius=5)
        pygame.draw.rect(self.screen, NEON_PURPLE, (right_panel_x, 5, 195, 80), 2, border_radius=5)

        # Mostrar patrón del nivel actual
        pattern_name = LEVEL_NAMES[(self.level - 1) % len(LEVEL_NAMES)]
        pattern_text = self.small_font.render(f"{pattern_name}", True, NEON_PINK)
        self.screen.blit(pattern_text, (right_panel_x + 10, 12))

        high_score_text = self.small_font.render(
            f"MÁXIMA: {self.high_score}", True, NEON_YELLOW
        )
        self.screen.blit(high_score_text, (right_panel_x + 10, 35))

        # ==========================================
        # MOSTRAR POWER-UPS ACTIVOS
        # ==========================================
        active_letters = []
        power_colors = {
            "expand": NEON_GREEN,
            "multi_ball": NEON_YELLOW,
            "slow_ball": NEON_PURPLE,
            "destroyer_ball": NEON_RED,
            "laser_shoot": NEON_ORANGE
        }

        for power_type, timer in self.active_power_ups.items():
            if timer > 0:
                letter = power_type[0].upper()
                active_letters.append((letter, power_colors.get(power_type, WHITE)))

        # Dibujar letras de power-ups activos
        if active_letters:
            # Panel para power-ups
            pw_panel_x = WINDOW_WIDTH // 2 - 80
            pygame.draw.rect(self.screen, (30, 30, 60), (pw_panel_x - 5, 5, 170, 30), border_radius=5)
            pygame.draw.rect(self.screen, NEON_CYAN, (pw_panel_x - 5, 5, 170, 30), 1, border_radius=5)

            start_x = pw_panel_x + 5
            for i, (letter, color) in enumerate(active_letters):
                # Fondo del carácter
                pygame.draw.circle(self.screen, color, (start_x + i * 25 + 8, 20), 10)
                letter_text = self.small_font.render(letter, True, BLACK)
                letter_rect = letter_text.get_rect(center=(start_x + i * 25 + 8, 20))
                self.screen.blit(letter_text, letter_rect)

        # ==========================================
        # MOSTRAR VELOCIDAD DE LAS PELOTAS
        # ==========================================
        if self.balls and not self.waiting_for_ball_release:
            ball_speed = math.sqrt(self.balls[0].speed_x**2 + self.balls[0].speed_y**2)
            speed_text = self.small_font.render(f"VEL: {ball_speed:.1f}", True, NEON_CYAN)
            self.screen.blit(speed_text, (WINDOW_WIDTH // 2 - 60, 45))

        # Indicador visual para pelota lista para lanzar
        if self.waiting_for_ball_release:
            flash_time = pygame.time.get_ticks() // 400
            if flash_time % 2 == 0:
                # Efecto de brillo en el texto
                ready_text = self.font.render("CLIC o ESPACIO para lanzar", True, NEON_GREEN)
                ready_rect = ready_text.get_rect(
                    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80)
                )
                # Glow effect
                glow_text = self.font.render("CLIC o ESPACIO para lanzar", True, tuple(min(255, c + 50) for c in NEON_GREEN))
                self.screen.blit(glow_text, (ready_rect.x + 1, ready_rect.y + 1))
                self.screen.blit(ready_text, ready_rect)

            # Flecha parpadeante apuntando a la pelota pegada
            for ball in self.balls:
                if ball.stuck_to_paddle:
                    arrow_color = NEON_CYAN if flash_time % 2 == 0 else WHITE
                    arrow_points = [
                        (ball.x - 10, ball.y - 25),
                        (ball.x + 10, ball.y - 25),
                        (ball.x, ball.y - 15),
                    ]
                    pygame.draw.polygon(self.screen, arrow_color, arrow_points)

        # ==========================================
        # MENSAJE DE PAUSA
        # ==========================================
        if self.paused and self.game_state == "playing":
            # Fondo semi-transparente para el mensaje de pausa
            pause_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            pause_overlay.set_alpha(128)  # Semi-transparente
            pause_overlay.fill(BLACK)
            self.screen.blit(pause_overlay, (0, 0))

            # Mensaje de pausa
            pause_text = self.font.render("JUEGO PAUSADO", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(pause_text, pause_rect)

            # Instrucción para reanudar
            resume_text = self.small_font.render("Presiona P para reanudar", True, WHITE)
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(resume_text, resume_rect)

    def draw_game_over(self):
        """Dibuja la pantalla de game over con efectos neón."""
        # Panel de fondo (centrado verticalmente)
        panel_width, panel_height = 420, 230
        panel_x = WINDOW_WIDTH // 2 - panel_width // 2
        panel_y = WINDOW_HEIGHT // 2 - panel_height // 2 - 50

        pygame.draw.rect(self.screen, (20, 10, 30), (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(self.screen, NEON_RED, (panel_x, panel_y, panel_width, panel_height), 3, border_radius=10)

        # Título con efecto de brillo
        title_y = panel_y + 40
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
        glow_color = (int(200 * pulse), int(50 * pulse), int(50 * pulse))
        game_over_glow = self.big_font.render("GAME OVER", True, glow_color)
        game_over_glow_rect = game_over_glow.get_rect(
            center=(WINDOW_WIDTH // 2 + 2, title_y + 2)
        )
        self.screen.blit(game_over_glow, game_over_glow_rect)

        game_over = self.big_font.render("GAME OVER", True, NEON_RED)
        game_over_rect = game_over.get_rect(
            center=(WINDOW_WIDTH // 2, title_y)
        )
        self.screen.blit(game_over, game_over_rect)

        # Puntuación
        score_y = title_y + 60
        score = self.font.render(f"Puntuación Final: {self.score}", True, WHITE)
        score_rect = score.get_rect(center=(WINDOW_WIDTH // 2, score_y))
        self.screen.blit(score, score_rect)

        # Récord
        if self.score == self.high_score:
            record_y = score_y + 35
            new_record = self.font.render("¡NUEVO RÉCORD!", True, NEON_YELLOW)
            record_rect = new_record.get_rect(
                center=(WINDOW_WIDTH // 2, record_y)
            )
            glow_record = self.font.render("¡NUEVO RÉCORD!", True, (255, 255, 150))
            self.screen.blit(glow_record, (record_rect.x + 1, record_rect.y + 1))
            self.screen.blit(new_record, record_rect)

        # Instrucción
        instr_y = score_y + 75
        restart = self.small_font.render("Presiona ESPACIO para reiniciar", True, NEON_CYAN)
        restart_rect = restart.get_rect(
            center=(WINDOW_WIDTH // 2, instr_y)
        )
        self.screen.blit(restart, restart_rect)

    def draw_victory(self):
        """Dibuja la pantalla de victoria con efectos neón."""
        # Panel de fondo (centrado verticalmente)
        panel_width, panel_height = 420, 230
        panel_x = WINDOW_WIDTH // 2 - panel_width // 2
        panel_y = WINDOW_HEIGHT // 2 - panel_height // 2 - 50

        pygame.draw.rect(self.screen, (10, 20, 30), (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(self.screen, NEON_GREEN, (panel_x, panel_y, panel_width, panel_height), 3, border_radius=10)

        # Título con efecto de brillo (centrado)
        title_y = panel_y + 40
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
        glow_color = (int(50 * pulse), int(255 * pulse), int(100 * pulse))
        victory_glow = self.big_font.render("¡NIVEL COMPLETADO!", True, glow_color)
        victory_glow_rect = victory_glow.get_rect(
            center=(WINDOW_WIDTH // 2 + 2, title_y + 2)
        )
        self.screen.blit(victory_glow, victory_glow_rect)

        victory = self.big_font.render("¡NIVEL COMPLETADO!", True, NEON_GREEN)
        victory_rect = victory.get_rect(
            center=(WINDOW_WIDTH // 2, title_y)
        )
        self.screen.blit(victory, victory_rect)

        # Puntuación
        score_y = title_y + 60
        score = self.font.render(f"Puntuación: {self.score}", True, WHITE)
        score_rect = score.get_rect(center=(WINDOW_WIDTH // 2, score_y))
        self.screen.blit(score, score_rect)

        # Siguiente nivel
        next_y = score_y + 35
        next_pattern_name = LEVEL_NAMES[(self.level) % len(LEVEL_NAMES)]
        level_info = self.font.render(
            f"Siguiente: {next_pattern_name}", True, NEON_PINK
        )
        level_info_rect = level_info.get_rect(
            center=(WINDOW_WIDTH // 2, next_y)
        )
        self.screen.blit(level_info, level_info_rect)

        # Instrucción
        instr_y = next_y + 45
        next_level = self.small_font.render(
            "Presiona ESPACIO para continuar", True, NEON_CYAN
        )
        next_level_rect = next_level.get_rect(
            center=(WINDOW_WIDTH // 2, instr_y)
        )
        self.screen.blit(next_level, next_level_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
