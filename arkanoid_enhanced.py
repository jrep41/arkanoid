"""
ARKANOID - EDICIÓN MEJORADA
===========================
Un juego completo de Arkanoid desarrollado en Python usando pygame.
Este código está comentado para principiantes en Python.

Autor: GitHub Copilot
Fecha: Julio 2025
"""

# Importamos las librerías necesarias
import math  # Para cálculos matemáticos (ángulos, trigonometría)
import os
import random  # Para generar números aleatorios
import sys  # Para funciones del sistema como salir del programa

import pygame  # Librería principal para hacer juegos en Python

import sounds  # Módulo de efectos de sonido sintéticos

# Forzar el uso de PulseAudio / PipeWire / ALSA
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

# Inicializar Pygame - SIEMPRE necesario antes de usar pygame
pygame.init()  # Inicializa todos los módulos de pygame
pygame.mixer.init()  # Inicializa el sistema de sonido

# ==========================================
# CONSTANTES DEL JUEGO
# ==========================================
# Las constantes son valores que NO cambian durante el juego
# Se escriben en MAYÚSCULAS por convención en Python

# Dimensiones de la ventana del juego (en píxeles)
SCREEN_WIDTH = 1280  # Ancho de la ventana
SCREEN_HEIGHT = 860  # Alto de la ventana

# Zona de juego (la "pantalla" del mueble arcade) en coordenadas de juego
WINDOW_WIDTH = 540  # Ancho de la zona de juego
WINDOW_HEIGHT = 640  # Alto de la zona de juego

# Posición de la zona de juego dentro de la ventana (el mueble centrado)
PLAY_OFFSET_X = 370  # Esquina izquierda de la pantalla del mueble
PLAY_OFFSET_Y = 104  # Esquina superior de la pantalla del mueble

# Marco del mueble (bezel) y banner superior estilo synthwave
CABINET_RECT = (358, 92, 564, 664)
BANNER_RECT = (200, 14, 880, 74)

# Dimensiones de la paleta del jugador
PADDLE_WIDTH = 92  # Ancho de la paleta
PADDLE_HEIGHT = 12  # Alto de la paleta (cápsula neón)

# Propiedades de la pelota
BALL_SIZE = 10  # Tamaño de la pelota (diámetro) (50% más pequeña)

# Dimensiones de los ladrillos
BRICK_WIDTH = 48  # Ancho de cada ladrillo (píldora neón)
BRICK_HEIGHT = 20  # Alto de cada ladrillo
BRICK_ROWS = 8  # Número de filas de ladrillos
BRICK_COLS = 10  # Número de columnas de ladrillos

# Velocidades del juego (píxeles por frame)
PADDLE_SPEED = 6  # Qué tan rápido se mueve la paleta
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

# Colores neón synthwave (estilo retrowave de los 80)
NEON_CYAN = (0, 224, 255)
NEON_PINK = (255, 45, 149)
NEON_PURPLE = (170, 90, 255)
NEON_ORANGE = (255, 122, 50)
NEON_GREEN = (0, 255, 168)
NEON_YELLOW = (255, 226, 60)
NEON_RED = (255, 60, 110)

# Paleta synthwave "neon breakout": fondo púrpura profundo y neones rosa,
# cian y amarillo (mueble arcade estilo HYPERBRICK)
BG_TOP = (26, 10, 52)  # Púrpura profundo (parte superior del fondo)
BG_BOTTOM = (10, 4, 26)  # Casi negro violáceo (parte inferior del fondo)
TEXT_PRIMARY = (238, 232, 255)  # Color del texto principal (lavanda)
TEXT_DIM = (155, 132, 200)  # Color de etiquetas y texto secundario
ACCENT_CYAN = (0, 224, 255)  # Acento principal (paleta, nivel, acentos)
ACCENT_PINK = (255, 45, 149)  # Acento secundario (mueble, títulos, láser)

# Lista de colores para los ladrillos (una por tipo) - neones synthwave
BRICK_COLORS = [
    (240, 235, 255),  # Blanco lavanda
    (255, 122, 50),  # Naranja neón
    (0, 224, 255),  # Cian neón
    (0, 255, 168),  # Verde menta
    (255, 32, 110),  # Rosa chicle
    (110, 90, 255),  # Violeta
    (200, 60, 255),  # Púrpura neón
    (255, 226, 60),  # Amarillo neón
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
        self.life = 30  # Tiempo de vida en frames (30 frames = 0.5 segundos a60fps)
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
        Dibuja la partícula como una chispa con halo neón que se desvanece.
        """
        if self.life > 0:
            ratio = self.life / self.max_life
            radius = 1 + int(3 * ratio)
            draw_glow_dot(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                radius,
                alpha=int(255 * ratio),
            )


# ==========================================
# CLASE SCOREPOPUP (PUNTOS FLOTANTES)
# ==========================================
class ScorePopup:
    """
    Texto flotante que muestra los puntos ganados al destruir un ladrillo
    (+10, +20...) subiendo y desvaneciéndose, como en los arcade neon.
    """

    def __init__(self, x, y, text, color=(255, 235, 250)):
        self.x = x  # Posición horizontal del centro del texto
        self.y = y  # Posición vertical del centro del texto
        self.text = text  # Texto a mostrar (por ejemplo "+20")
        self.color = color  # Color del texto
        self.life = 45  # Tiempo de vida en frames
        self.max_life = 45  # Tiempo de vida máximo (para el desvanecido)

    def update(self):
        """Hace flotar el texto hacia arriba y reduce su tiempo de vida."""
        self.y -= 0.7
        self.life -= 1

    def draw(self, screen):
        """Dibuja el texto con transparencia según el tiempo de vida."""
        if self.life > 0:
            surf = render_text(
                self.text, 15, self.color, bold=True, cached=False, italic=True
            )
            surf.set_alpha(int(255 * self.life / self.max_life))
            screen.blit(surf, surf.get_rect(center=(int(self.x), int(self.y))))


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
        Principalmente, maneja la duración de los power-ups.
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
        # Aumentar ancho pero no más allá de 150 píxeles
        self.width = min(150, self.width + 30)

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
        Dibuja la paleta como una cápsula neón cian con extremos rosa
        (estilo synthwave) y resplandor bajo el cuerpo.
        """
        x = int(self.x)
        y = int(self.y)
        width = int(self.width)
        height = self.height
        radius = max(3, height // 2)
        end_cap_width = 16

        # Resplandor neón cian bajo la paleta
        halo = make_panel_surface(
            (width + 20, height + 16), (*ACCENT_CYAN, 40), radius + 8
        )
        screen.blit(halo, (x - 10, y - 6))

        # Cuerpo de la cápsula con degradado cian
        body = make_gradient_surface(
            (width, height),
            lerp_color(ACCENT_CYAN, (255, 255, 255), 0.35),
            shade(ACCENT_CYAN, 0.45),
            radius,
        )
        screen.blit(body, (x, y))

        # Extremos rosa neón (guiño a la Vaus)
        cap = make_gradient_surface(
            (end_cap_width, height),
            lerp_color(ACCENT_PINK, (255, 255, 255), 0.3),
            shade(ACCENT_PINK, 0.5),
            radius,
        )
        screen.blit(cap, (x, y))
        screen.blit(cap, (x + width - end_cap_width, y))

        # Línea de brillo central
        strip_x = x + end_cap_width + 4
        strip_width = max(8, width - (end_cap_width + 4) * 2)
        pygame.draw.line(
            screen,
            (235, 255, 255),
            (strip_x, y + 2),
            (strip_x + strip_width, y + 2),
            2,
        )

        # Cañones láser con resplandor pulsante
        if self.laser_active:
            pulse = 0.6 + 0.4 * abs(math.sin(pygame.time.get_ticks() * 0.01))
            cannon = make_gradient_surface((6, 10), WHITE, ACCENT_PINK, radius=3)
            for cannon_x in (x + width // 4, x + (width * 3) // 4):
                draw_glow_dot(
                    screen,
                    ACCENT_PINK,
                    (cannon_x, y - 2),
                    int(6 + 3 * pulse),
                    alpha=170,
                )
                screen.blit(cannon, (cannon_x - 3, y - 8))

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
        self.game_sound_manager: sounds.SoundManager | None = None

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
        return self.y >= WINDOW_HEIGHT  # La pelota se perdió si sale por el fondo

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
                self.game_sound_manager.play("paddle_hit")

            return True  # Hubo colisión
        return False  # No hubo colisión

    def draw(self, screen):
        """
        Dibuja la pelota como una esfera luminosa con rastro de energía.
        En modo destructor el resplandor se vuelve rojo.
        """
        # Color del halo y del rastro según el modo
        glow_color = ACCENT_PINK if self.destroyer_mode else ACCENT_CYAN

        # Rastro: puntos de brillo cada vez más tenues(255, 235, 170)
        total = max(1, len(self.trail))
        for index, (trail_x, trail_y) in enumerate(self.trail):
            ratio = (index + 1) / total
            draw_glow_dot(
                screen,
                glow_color,
                (int(trail_x), int(trail_y)),
                1 + int(3 * ratio),
                alpha=int(70 * ratio),
            )

        # Halo de la pelota
        draw_glow_dot(
            screen, glow_color, (int(self.x), int(self.y)), self.radius + 5, alpha=150
        )

        # Esfera con degradado radial (superficie pre-renderizada)
        screen.blit(
            make_ball_sprite(self.size + 2, self.destroyer_mode),
            (int(self.x) - self.radius - 1, int(self.y) - self.radius - 1),
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
    (240, 235, 255): 1,  # Blanco lavanda
    (255, 122, 50): 1,  # Naranja neón
    (0, 224, 255): 1,  # Cian neón
    (0, 255, 168): 2,  # Verde menta
    (255, 32, 110): 3,  # Rosa chicle
    (110, 90, 255): 2,  # Violeta
    (200, 60, 255): 2,  # Púrpura neón
    (255, 226, 60): 2,  # Amarillo neón
}

# Identidad visual de cada power-up: color, símbolo y duración (en frames)
POWER_UP_COLORS = {
    "expand": (0, 224, 255),
    "multi_ball": (255, 226, 60),
    "slow_ball": (170, 90, 255),
    "destroyer_ball": (255, 45, 149),
    "laser_shoot": (255, 122, 50),
}
POWER_UP_SYMBOLS = {
    "expand": "E",
    "multi_ball": "M",
    "slow_ball": "S",
    "destroyer_ball": "D",
    "laser_shoot": "L",
}
POWER_UP_DURATIONS = {
    "expand": 600,  # 10 segundos
    "multi_ball": 1800,  # 30 segundos
    "slow_ball": 1800,  # 30 segundos
    "destroyer_ball": 2000,  # 20 segundos (aprox.)
    "laser_shoot": 2000,  # 20 segundos
}


# ==========================================
# SISTEMA VISUAL MODERNO (NEÓN Y CRISTAL)
# ==========================================
# Funciones de apoyo para el aspecto actual del juego: degradados suaves,
# paneles de cristal translúcidos, halos neón difusos y tipografía limpia.
# Todas las superficies caras de crear se guardan en caché para no perder
# rendimiento (se crean una vez y se reutilizan en cada frame).

# Tipografías preferidas (se usa la primera que exista en el sistema)
PREFERRED_FONTS = [
    "Segoe UI",
    "Ubuntu",
    "Noto Sans",
    "DejaVu Sans",
    "Verdana",
    "Arial",
]

_font_cache = {}  # Caché de fuentes: (tamaño, negrita) -> fuente
_gradient_cache = {}  # Caché de superficies con degradado
_panel_cache = {}  # Caché de paneles de cristal
_glow_cache = {}  # Caché de halos neón
_text_cache = {}  # Caché de textos renderizados
_ball_cache = {}  # Caché de la esfera de la pelota


def get_font(size, bold=False, italic=False):
    """Devuelve una tipografía del juego (cacheada por tamaño y estilo)."""
    key = (size, bold, italic)
    if key not in _font_cache:
        path = None
        for name in PREFERRED_FONTS:
            path = pygame.font.match_font(name)
            if path:
                break
        if path:
            font = pygame.font.Font(path, size)
        else:
            font = pygame.font.Font(None, int(size * 1.4))
        font.set_bold(bold)
        font.set_italic(italic)
        _font_cache[key] = font
    return _font_cache[key]


def lerp_color(color_a, color_b, ratio):
    """Mezcla dos colores RGB. ratio=0 devuelve color_a y ratio=1 color_b."""
    ratio = max(0.0, min(1.0, ratio))
    return tuple(int(a + (b - a) * ratio) for a, b in zip(color_a, color_b))


def shade(color, factor):
    """Aclara (factor > 1) u oscurece (factor < 1) un color RGB."""
    return tuple(max(0, min(255, int(c * factor))) for c in color)


def make_gradient_surface(size, top_color, bottom_color, radius=0, gloss=True):
    """
    Crea una superficie con degradado vertical y esquinas redondeadas.
    Se guarda en caché porque recorrer los píxeles es costoso.
    """
    key = (size, top_color, bottom_color, radius, gloss)
    if key not in _gradient_cache:
        width, height = size
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        # Degradado vertical: el color superior se transforma en el inferior
        for i in range(height):
            row_color = lerp_color(top_color, bottom_color, i / max(1, height - 1))
            pygame.draw.line(surf, row_color, (0, i), (width, i))

        # Recorte de esquinas redondeadas (multiplicando el canal alfa)
        if radius > 0:
            mask = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(
                mask, (255, 255, 255, 255), (0, 0, width, height), border_radius=radius
            )
            surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Línea de brillo superior (efecto cristal)
        if gloss and height > 4 and width > 2 * radius:
            gloss_color = lerp_color(top_color, (255, 255, 255), 0.5)
            pygame.draw.line(surf, gloss_color, (radius, 1), (width - radius - 1, 1))

        _gradient_cache[key] = surf
    return _gradient_cache[key]


def make_panel_surface(size, color, radius=14, border_color=None):
    """
    Crea un panel de cristal: relleno translúcido con esquinas redondeadas
    y, opcionalmente, un borde fino iluminado.
    """
    key = (size, color, radius, border_color)
    if key not in _panel_cache:
        width, height = size
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        # Relleno translúcido recortado con esquinas redondeadas
        surf.fill(color)
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            mask, (255, 255, 255, 255), (0, 0, width, height), border_radius=radius
        )
        surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Borde fino con un toque de luz en la parte superior
        if border_color:
            pygame.draw.rect(
                surf, border_color, (0, 0, width, height), 1, border_radius=radius
            )
            if width > 2 * radius:
                highlight = lerp_color(tuple(border_color[:3]), (255, 255, 255), 0.45)
                pygame.draw.line(surf, highlight, (radius, 1), (width - radius - 1, 1))

        _panel_cache[key] = surf
    return _panel_cache[key]


def draw_panel(
    screen, rect, color=(16, 22, 44, 180), radius=14, border_color=None, shadow=True
):
    """Dibuja un panel de cristal con una sombra suave debajo."""
    x, y, width, height = rect
    if shadow:
        shadow_surf = make_panel_surface((width, height), (0, 0, 0, 110), radius)
        screen.blit(shadow_surf, (x + 3, y + 5))
    screen.blit(
        make_panel_surface((width, height), color, radius, border_color), (x, y)
    )


def make_glow_sprite(radius, color, alpha=255):
    """
    Crea un halo neón circular con decaimiento cuadrático (muy suave).
    El alfa se cuantiza en 16 niveles para mantener la caché pequeña.
    """
    radius = max(1, int(radius))
    alpha = max(0, min(255, (int(alpha) // 16) * 16))
    key = (radius, color, alpha)
    if key not in _glow_cache:
        size = radius * 2 + 2
        center = size // 2
        bright = lerp_color(color, (255, 255, 255), 0.35)
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        for y in range(size):
            for x in range(size):
                distance = math.hypot(x - center, y - center)
                if distance <= radius:
                    falloff = 1.0 - distance / radius
                    surf.set_at((x, y), (*bright, int(alpha * falloff * falloff)))
        _glow_cache[key] = surf
    return _glow_cache[key]


def draw_glow_dot(screen, color, center, radius, alpha=255):
    """Dibuja un punto luminoso con halo difuso (alpha = intensidad del brillo)."""
    sprite = make_glow_sprite(radius, color, alpha)
    offset_x = center[0] - sprite.get_width() // 2
    offset_y = center[1] - sprite.get_height() // 2
    screen.blit(sprite, (offset_x, offset_y))


def render_text(text, size, color, bold=False, spacing=0, cached=True, italic=False):
    """
    Renderiza un texto con la tipografía del juego (opcional en cursiva).
    Con spacing > 0 separa las letras (estilo logotipo).
    """
    key = (text, size, color, bold, spacing, italic)
    if not cached:
        return _render_text_now(text, size, color, bold, spacing, italic)
    if key not in _text_cache:
        _text_cache[key] = _render_text_now(text, size, color, bold, spacing, italic)
    return _text_cache[key]


def _render_text_now(text, size, color, bold, spacing, italic=False):
    """Renderiza un texto sin usar la caché (para valores que cambian)."""
    font = get_font(size, bold, italic)
    if spacing <= 0:
        return font.render(text, True, color)
    letters = [font.render(char, True, color) for char in text]
    width = sum(s.get_width() for s in letters) + spacing * max(0, len(letters) - 1)
    surf = pygame.Surface((max(1, width), font.get_height()), pygame.SRCALPHA)
    cursor = 0
    for letter in letters:
        surf.blit(letter, (cursor, 0))
        cursor += letter.get_width() + spacing
    return surf


def draw_text(
    screen,
    text,
    size,
    color,
    pos,
    align="topleft",
    bold=False,
    spacing=0,
    shadow=False,
    glow=0,
    cached=True,
    italic=False,
):
    """
    Dibuja un texto con alineación flexible.
    - shadow: dibuja una sombra sutil detrás del texto
    - glow: radio en píxeles del halo de color que lo rodea
    - cached: False para textos que cambian mucho (puntuaciones, timers)
    - italic: dibuja el texto en cursiva (estilo arcade synthwave)
    """
    surf = render_text(text, size, color, bold, spacing, cached, italic)
    rect = surf.get_rect()
    if align not in (
        "topleft",
        "topright",
        "midleft",
        "midright",
        "midtop",
        "midbottom",
        "center",
        "bottomleft",
        "bottomright",
    ):
        align = "topleft"
    setattr(rect, align, pos)

    # Halo de color alrededor del texto (simula el brillo neón)
    if glow > 0:
        halo_color = lerp_color(tuple(color[:3]), (8, 12, 28), 0.5)
        halo = render_text(text, size, halo_color, bold, spacing, cached, italic)
        for step_x, step_y in (
            (-glow, 0),
            (glow, 0),
            (0, -glow),
            (0, glow),
            (-glow, -glow),
            (glow, glow),
            (-glow, glow),
            (glow, -glow),
        ):
            screen.blit(halo, (rect.x + step_x, rect.y + step_y))

    # Sombra sutil detrás del texto
    if shadow:
        shadow_surf = render_text(text, size, (5, 8, 18), bold, spacing, cached, italic)
        screen.blit(shadow_surf, (rect.x + 1, rect.y + 2))

    screen.blit(surf, rect)


def draw_pill_button(screen, rect, label, color, pulse=0.0, font_size=22):
    """
    Dibuja un botón tipo píldora: cristal oscuro, borde luminoso,
    etiqueta centrada y un halo exterior que pulsa suavemente.
    """
    x, y, width, height = rect
    radius = max(6, height // 2)

    # Halo exterior pulsante (se cuantiza para no llenar la caché)
    halo_alpha = 25 + 15 * round(min(1.0, max(0.0, pulse)) * 2)
    halo = make_panel_surface(
        (width + 28, height + 24), (*color, halo_alpha), radius + 12
    )
    screen.blit(halo, (x - 14, y - 12))

    # Cuerpo de cristal con borde del color del acento
    draw_panel(
        screen,
        (x, y, width, height),
        (12, 18, 40, 215),
        radius,
        lerp_color(color, (255, 255, 255), 0.35),
    )

    # Etiqueta del botón
    draw_text(
        screen,
        label,
        font_size,
        color,
        (x + width // 2, y + height // 2),
        align="center",
        bold=True,
        spacing=2,
        glow=1,
        italic=True,
    )


def make_streak_surface(width, height, color, reverse=False):
    """
    Crea una ráfaga de velocidad horizontal (alfa decreciente hacia un
    extremo), como las líneas del banner de los carteles arcade.
    """
    key = ("streak", width, height, color, reverse)
    if key not in _gradient_cache:
        surf = pygame.Surface((max(1, width), max(1, height)), pygame.SRCALPHA)
        for x in range(width):
            ratio = x / max(1, width - 1)
            if reverse:
                ratio = 1.0 - ratio
            alpha = int(235 * (ratio**1.6))
            pygame.draw.line(surf, (*color, alpha), (x, 0), (x, height))
        _gradient_cache[key] = surf
    return _gradient_cache[key]


def render_styled_title(text, size, color_a, color_b, glow_color, spacing=3):
    """
    Renderiza un logotipo en cursiva con degradado letra a letra (de color_a
    a color_b) y resplandor de color detrás, estilo cartel arcade synthwave.
    """
    key = ("title", text, size, color_a, color_b, glow_color, spacing)
    if key not in _text_cache:
        font = get_font(size, bold=True, italic=True)
        margin = 10
        letters = [
            (
                font.render(char, True, lerp_color(color_a, color_b, index / max(1, len(text) - 1))),
                font.render(char, True, glow_color),
            )
            for index, char in enumerate(text)
        ]
        text_width = sum(glyph.get_width() for glyph, _ in letters) + spacing * max(
            0, len(letters) - 1
        )
        surf = pygame.Surface(
            (text_width + margin * 2, font.get_height() + margin * 2), pygame.SRCALPHA
        )

        # Varias pasadas desplazadas forman el resplandor neón rosa
        for step_x, step_y in (
            (-3, 0),
            (3, 0),
            (0, -3),
            (0, 3),
            (-2, -2),
            (2, 2),
            (-2, 2),
            (2, -2),
        ):
            cursor = margin
            for _, glow_glyph in letters:
                surf.blit(glow_glyph, (cursor + step_x, margin + step_y))
                cursor += glow_glyph.get_width() + spacing

        # Pasada final con el degradado de colores
        cursor = margin
        for glyph, _ in letters:
            surf.blit(glyph, (cursor, margin))
            cursor += glyph.get_width() + spacing

        _text_cache[key] = surf
    return _text_cache[key]


def make_sunset_surface(diameter):
    """
    Crea el sol synthwave: círculo con degradado amarillo -> naranja -> rosa
    y franjas horizontales transparentes que crecen hacia abajo.
    """
    key = ("sunset", diameter)
    if key not in _gradient_cache:
        surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        radius = diameter / 2
        top_color = (255, 240, 120)
        mid_color = (255, 150, 60)
        bottom_color = (255, 60, 130)

        # Disco con degradado vertical
        for y in range(diameter):
            ratio = y / max(1, diameter - 1)
            if ratio < 0.5:
                row_color = lerp_color(top_color, mid_color, ratio / 0.5)
            else:
                row_color = lerp_color(mid_color, bottom_color, (ratio - 0.5) / 0.5)
            for x in range(diameter):
                if math.hypot(x - radius + 0.5, y - radius + 0.5) <= radius:
                    surf.set_at((x, y), row_color)

        # Franjas horizontales: finas arriba y gruesas hacia el borde inferior
        stripe_y = diameter * 0.52
        gap = 3.0
        band = 2.0
        while stripe_y < diameter:
            for row in range(int(stripe_y), min(int(stripe_y + band), diameter)):
                pygame.draw.line(surf, (0, 0, 0, 0), (0, row), (diameter, row))
            stripe_y += band + gap
            gap += 1.5
            band += 1.0

        _gradient_cache[key] = surf
    return _gradient_cache[key]


def make_horizon_surface(width, height, color):
    """
    Crea la franja de neón del horizonte: brillante en el centro de la
    pantalla y suave hacia los bordes, con caída vertical suave.
    """
    key = ("horizon", width, height, color)
    if key not in _gradient_cache:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        half = height / 2
        for y in range(height):
            fall_y = max(0.0, 1.0 - abs(y - half) / half) ** 2
            for x in range(width):
                fall_x = max(0.0, 1.0 - abs(x / width - 0.5) * 1.5) ** 1.4
                alpha = int(230 * fall_x * fall_y)
                if alpha > 0:
                    surf.set_at((x, y), (*color, alpha))
        _gradient_cache[key] = surf
    return _gradient_cache[key]


def make_ball_sprite(size, destroyer_mode=False):
    """
    Pre-renderiza la pelota: una esfera con degradado radial
    (blanca en el centro, teñida en el borde).
    """
    key = (size, destroyer_mode)
    if key not in _ball_cache:
        edge_color = (255, 90, 150) if destroyer_mode else (255, 226, 120)
        radius = size / 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        for y in range(size):
            for x in range(size):
                offset_x, offset_y = x - radius + 0.5, y - radius + 0.5
                distance = math.hypot(offset_x, offset_y)
                if distance <= radius:
                    edge = min(1.0, distance / radius)
                    surf.set_at(
                        (x, y), lerp_color((255, 255, 255), edge_color, edge * 0.9)
                    )
        _ball_cache[key] = surf
    return _ball_cache[key]


# Las siguientes funciones mantienen la API antigua de efectos neón,
# ahora construidas sobre los halos cacheados del sistema moderno.
def draw_glow_circle(screen, color, center, radius, glow_radius=15):
    """Dibuja un círculo con halo neón difuso."""
    draw_glow_dot(screen, color, center, radius + max(2, glow_radius // 3), alpha=150)
    pygame.draw.circle(screen, lerp_color(color, (255, 255, 255), 0.3), center, radius)


def draw_glow_rect(screen, color, rect, glow_size=8):
    """Dibuja un rectángulo con halo neón difuso."""
    x, y, width, height = rect
    halo = make_panel_surface(
        (width + glow_size * 2, height + glow_size * 2), (*color, 60), glow_size * 2
    )
    screen.blit(halo, (x - glow_size, y - glow_size))
    pygame.draw.rect(screen, color, (x, y, width, height))


def draw_neon_line(screen, color, start, end, width=3, glow_size=10):
    """Dibuja una línea con efecto de brillo neón."""
    pygame.draw.line(screen, shade(color, 0.5), start, end, width + glow_size)
    pygame.draw.line(screen, color, start, end, width)
    pygame.draw.line(
        screen, lerp_color(color, (255, 255, 255), 0.6), start, end, max(1, width // 2)
    )


def draw_glow_polygon(screen, color, points, glow_size=8):
    """Dibuja un polígono con efecto de brillo neón."""
    center_x = sum(p[0] for p in points) / len(points)
    center_y = sum(p[1] for p in points) / len(points)
    scaled_points = []
    for point_x, point_y in points:
        offset_x, offset_y = point_x - center_x, point_y - center_y
        scale = 1 + glow_size / 40
        scaled_points.append((center_x + offset_x * scale, center_y + offset_y * scale))
    pygame.draw.polygon(screen, shade(color, 0.4), scaled_points)
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

        # Superficie pre-renderizada del ladrillo (por rendimiento)
        self.surface = None
        self._build_surface()

    def _build_surface(self):
        """
        Pre-renderiza el ladrillo como una píldora neón synthwave: halo de
        color, relleno oscuro translúcido y borde brillante.
        """
        self.margin = 6
        width = self.width + self.margin * 2
        height = self.height + self.margin * 2
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        radius = self.height // 2

        # Halo de color alrededor de la píldora (doble capa tipo neón)
        surf.blit(make_panel_surface((width, height), (*self.color, 26), height // 2), (0, 0))
        surf.blit(
            make_panel_surface(
                (self.width + 6, self.height + 6), (*self.color, 55), radius + 3
            ),
            (self.margin - 3, self.margin - 3),
        )

        # Cuerpo de la píldora: relleno oscuro y borde brillante
        bright = lerp_color(self.color, (255, 255, 255), 0.55)
        body = make_panel_surface(
            (self.width, self.height),
            (*shade(self.color, 0.45), 235),
            radius,
            bright,
        )
        surf.blit(body, (self.margin, self.margin))

        # Línea de brillo superior (efecto cristal)
        pygame.draw.line(
            surf,
            lerp_color(self.color, (255, 255, 255), 0.8),
            (self.margin + radius // 2, self.margin + 3),
            (self.margin + self.width - radius // 2, self.margin + 3),
            1,
        )

        self.surface = surf

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

            # Regenerar la superficie pre-renderizada con el nuevo color
            self._build_surface()

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
        Dibuja el ladrillo como píldora neón con halo, indicios de daño
        y destello de impacto.
        """
        if not self.destroyed:
            # Píldora con halo (superficie pre-renderizada)
            screen.blit(
                self.surface, (self.x - self.margin, self.y - self.margin)
            )

            # Borde fino que define la píldora
            radius = self.height // 2
            pygame.draw.rect(
                screen,
                lerp_color(self.color, (255, 255, 255), 0.55),
                (self.x, self.y, self.width, self.height),
                2,
                border_radius=radius,
            )

            # Grietas finas cuando el ladrillo ya ha recibido daño
            if self.max_hits > 1 and self.current_hits > 0:
                crack_color = shade(self.color, 0.25)
                center_x = self.x + self.width // 2
                center_y = self.y + self.height // 2
                pygame.draw.lines(
                    screen,
                    crack_color,
                    False,
                    [
                        (center_x - self.width // 4, self.y + 4),
                        (center_x - 2, center_y),
                        (center_x - self.width // 5, self.y + self.height - 4),
                    ],
                    1,
                )
                pygame.draw.lines(
                    screen,
                    crack_color,
                    False,
                    [
                        (center_x + self.width // 4, self.y + 4),
                        (center_x + 3, center_y),
                        (center_x + self.width // 5, self.y + self.height - 4),
                    ],
                    1,
                )

            # Destello blanco justo después de recibir un impacto
            if self.hit_animation > 0:
                flash_alpha = (min(160, self.hit_animation * 8) // 20) * 20
                flash = make_panel_surface(
                    (self.width, self.height), (255, 255, 255, flash_alpha),
                    self.height // 2,
                )
                screen.blit(flash, (self.x, self.y))

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
        Dibuja el power-up como una cápsula luminosa con degradado,
        halo de color y su letra identificativa.
        """
        if self.active:
            color = POWER_UP_COLORS.get(self.power_type, (200, 200, 200))
            symbol = POWER_UP_SYMBOLS.get(self.power_type, "?")

            # Balanceo vertical muy sutil para dar sensación de caída
            bob = int(math.sin(self.rotation * 0.12) * 2)
            x = int(self.x)
            y = int(self.y) + bob
            radius = self.height // 2

            # Halo de color alrededor de la cápsula
            halo = make_panel_surface(
                (self.width + 16, self.height + 14), (*color, 70), radius + 7
            )
            screen.blit(halo, (x - 8, y - 7))

            # Cuerpo con degradado y esquinas redondeadas
            body = make_gradient_surface(
                (self.width, self.height),
                lerp_color(color, (255, 255, 255), 0.45),
                shade(color, 0.55),
                radius,
            )
            screen.blit(body, (x, y))

            # Borde luminoso
            pygame.draw.rect(
                screen,
                lerp_color(color, (255, 255, 255), 0.6),
                (x, y, self.width, self.height),
                1,
                border_radius=radius,
            )

            # Letra identificativa en el centro
            draw_text(
                screen,
                symbol,
                15,
                WHITE,
                (x + self.width // 2, y + self.height // 2),
                align="center",
                bold=True,
                shadow=True,
            )

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
    El láser viajan hacia arriba y destruyen ladrillos al impactar.
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
        Dibuja el láser como un rayo de energía con halo y núcleo brillante.
        """
        if self.active:
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2

            # Rastro del proyectil (se desvanece hacia atrás)
            total = max(1, len(self.trail))
            for index, (trail_x, trail_y) in enumerate(self.trail):
                ratio = (index + 1) / total
                draw_glow_dot(
                    screen,
                    ACCENT_PINK,
                    (int(trail_x), int(trail_y)),
                    2,
                    alpha=int(80 * ratio),
                )

            # Halo del proyectil
            draw_glow_dot(screen, ACCENT_PINK, (center_x, center_y), 8, alpha=170)

            # Núcleo: degradado blanco -> rosa
            core = make_gradient_surface(
                (self.width + 2, self.height + 4), WHITE, ACCENT_PINK, radius=2
            )
            screen.blit(core, (self.x - 1, self.y - 2))

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
def load_high_score():
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
    except (OSError, ValueError):
        # Si el archivo no existe, no se puede leer o tiene un formato incorrecto
        return 0  # Devolver 0 como puntuación por defecto


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
        self.lasers = None
        self.power_ups = None
        self.bricks = None
        self.balls = None
        self.paddle = None
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED,
            vsync=1,
        )
        pygame.display.set_caption("Arkanoid · Neon Breakout")
        self.clock = pygame.time.Clock()  # Para controlar framerate (60 FPS)

        # Superficie de fondo cacheada (se dibuja una sola vez por rendimiento)
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_surface.fill(BLACK)

        # Superficie intermedia de la zona de juego (permite aplicar el temblor)
        self.world_surface = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
        )

        # Variables del estado del juego
        self.score = 0  # Puntuación actual del jugador
        self.lives = (
            3  # Vidas restantes del jugador (aumentadas para facilitar el juego)
        )
        self.level = 1  # Nivel actual del juego
        self.high_score = load_high_score()  # Puntuación máxima guardada

        # Tipografías modernas del juego (cacheadas por tamaño y grosor)
        self.font = get_font(30)  # Fuente mediana
        self.small_font = get_font(18)  # Fuente pequeña
        self.big_font = get_font(56, bold=True)  # Fuente grande

        # Controles que se muestran en el menú: (tecla, descripción)
        self.menu_controls = [
            ("ESPACIO", "Comenzar / Lanzar"),
            ("RATÓN", "Mover la paleta"),
            ("← → A D", "Mover la paleta"),
            ("CLIC", "Lanzar / Disparar"),
            ("B", "Pelota extra"),
            ("P", "Pausar"),
            ("L", "Cañones láser"),
            ("E", "Paleta ancha"),
            ("M", "Multibola"),
            ("S", "Bola lenta"),
            ("D", "Bola destructora"),
            ("N", "Silenciar sonido"),
        ]

        # Estados y efectos visuales
        self.game_state = (
            "menu"  # Estado actual: 'menu', 'playing', 'game_over', 'victory'
        )
        self.paore_popups = []  # Textos flotantes de puntos ganados (+20...)
        self.scrticles = []  # Lista de partículas para efectos visuales
        self.screen_shake = 0  # Contador para efecto de temblor de pantalla

        # Estado de pausa
        self.paused = False  # Indica si el juego está pausado

        # Power-ups activos (tipo -> tiempo restante en frames)
        self.active_power_ups = {
            "expand": 0,
            "multi_ball": 0,
            "slow_ball": 0,
            "destroyer_ball": 0,
            "laser_shoot": 0,
        }

        # Control del juego
        self.mouse_control = True  # Control con ratón habilitado por defecto
        self.control_mode = (
            "mouse"  # Último método de control usado: 'mouse' o 'keyboard'
        )
        self.waiting_for_ball_release = False  # Si estamos esperando liberar la pelota

        # Sistema de sonido
        self.sound_manager = sounds.get_sound_manager()

        # Construir el fondo synthwave (banner, sol, rejilla y mueble)
        # una sola vez por rendimiento
        self.build_background()

        # Inicializar el juego
        self.reset_game()

        # Capturar el mouse al inicio
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mouse_captured = True

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
        self.score_popups = []  # Lista vacía de textos flotantes
        self.lasers = []  # Lista vacía de láser

        # Resetear power-ups activos
        self.active_power_ups = {
            "expand": 0,
            "multi_ball": 0,
            "slow_ball": 0,
            "destroyer_ball": 0,
            "laser_shoot": 0,
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
        start_y = 44  # Dejar sitio al sol synthwave del fondo

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
                        self.sound_manager.play("power_up")
                    elif self.game_state == "playing" and self.waiting_for_ball_release:
                        # Liberar la pelota pegada
                        for ball in self.balls:
                            if ball.stuck_to_paddle:
                                ball.release()
                        self.waiting_for_ball_release = False
                    elif self.game_state == "game_over":
                        # Reiniciar completamente el juego
                        self.score = 0
                        self.lives = 3  # Reiniciar con 10 vidas
                        self.level = 1
                        BALL_SPEED = INITIAL_BALL_SPEED  # Resetear velocidad de pelota
                        self.reset_game()
                        self.game_state = "playing"
                    elif self.game_state == "victory":
                        self.level += 1
                        # Reproducir sonido de nivel completado
                        self.sound_manager.play("level_complete")
                        # Aumentar dificultad gradualmente
                        BALL_SPEED += 0.05  # Incremento muy suave de velocidad
                        self.reset_game()
                        self.game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    return False
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
                            new_ball.destroyer_timer = self.active_power_ups[
                                "destroyer_ball"
                            ]
                        self.balls.append(new_ball)
                        # Efectos visuales
                        self.add_particles(new_ball.x, new_ball.y, WHITE, 8)
                elif event.key == pygame.K_p:  # Tecla P para pausar/reanudar
                    if self.game_state == "playing":
                        self.paused = not self.paused  # Alternar estado de pausa
                elif event.key == pygame.K_n:  # Tecla N para silenciar/activar sonido
                    self.sound_manager.toggle()
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
                elif (
                    event.key == pygame.K_d and self.game_state == "playing"
                ):  # Tecla D -> power-up destroyer_ball
                    self.apply_power_up("destroyer_ball")
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.game_state == "playing"
            ):  # Usuario hizo clic izquierdo
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
        if self.game_state != "playing" or (
            self.game_state == "playing" and self.paused
        ):
            return

        # Actualizar paleta
        self.paddle.update()

        # Mover paleta con teclado (flechas o A/D)
        keys = pygame.key.get_pressed()
        key_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        key_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if key_left:
            self.paddle.move_left()
            self.control_mode = "keyboard"
        if key_right:
            self.paddle.move_right()
            self.control_mode = "keyboard"

        # Actualizar posición de la paleta con el ratón
        # Solo si el control con ratón está habilitado y el último control fue el ratón
        if self.mouse_control and self.control_mode == "mouse":
            mouse_x, _ = pygame.mouse.get_pos()
            self.paddle.update_mouse_position(mouse_x - PLAY_OFFSET_X)

        # Si el usuario mueve el ratón, volver al control con ratón
        if self.mouse_control and self.control_mode == "keyboard":
            mouse_x, _ = pygame.mouse.get_pos()
            mouse_dx, mouse_dy = pygame.mouse.get_rel()
            if mouse_dx != 0 or mouse_dy != 0:
                self.control_mode = "mouse"
                self.paddle.update_mouse_position(mouse_x - PLAY_OFFSET_X)

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
                self.sound_manager.play("laser")

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
                                # Texto flotante con los puntos ganados
                                self.score_popups.append(
                                    ScorePopup(
                                        brick.x + brick.width // 2,
                                        brick.y,
                                        f"+{brick.points}",
                                    )
                                )
                                # Reproducir sonido de destrucción
                                self.sound_manager.play("brick_destroy")
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
                                self.sound_manager.play("brick_hit")
                        break

        # Remover pelotas que salieron
        for i in reversed(balls_to_remove):
            self.balls.pop(i)

        # Si no quedan pelotas, perder vida
        if not self.balls:
            self.lives -= 1
            self.screen_shake = 15
            # Reproducir sonido de perder vida
            self.sound_manager.play("life_lost")
            if self.lives <= 0:
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                self.game_state = "game_over"
                # Reproducir sonido de game over
                self.sound_manager.play("game_over")
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
                self.sound_manager.play("power_up")

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
                        # Texto flotante con los puntos ganados
                        self.score_popups.append(
                            ScorePopup(
                                brick.x + brick.width // 2,
                                brick.y,
                                f"+{brick.points}",
                            )
                        )
                        # Reproducir sonido de destrucción por láser
                        self.sound_manager.play("brick_destroy")

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
                        self.sound_manager.play("brick_hit")
                    break


        # Actualizar textos flotantes de puntos
        self.score_popups = [p for p in self.score_popups if p.life > 0]
        for popup in self.score_popups:
            popup.update()
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
            self.sound_manager.play("victory")

    def sync_ball_speeds(self):
        """
        Sincroniza las velocidades de todas las pelotas para que tengan la misma velocidad.
        Usa la velocidad de la primera pelota como referencia.
        """
        if len(self.balls) > 1:
            # Usar la velocidad de la primera pelota como referencia
            reference_speed = math.sqrt(
                self.balls[0].speed_x ** 2 + self.balls[0].speed_y ** 2
            )

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
            if 0 < len(self.balls) < 5:  # Verificar que hay pelotas y no exceder máximo
                for _ in range(2):
                    new_ball = Ball(self.balls[0].x, self.balls[0].y)
                    angle = random.uniform(-math.pi / 4, math.pi / 4)
                    speed = BALL_SPEED
                    new_ball.speed_x = speed * math.sin(angle)
                    new_ball.speed_y = -speed * math.cos(angle)
                    # Si destroyer_ball está activo, aplicar modo destructor a la nueva pelota
                    if self.active_power_ups.get("destroyer_ball", 0) > 0:
                        new_ball.destroyer_mode = True
                        new_ball.destroyer_timer = self.active_power_ups[
                            "destroyer_ball"
                        ]
                    self.balls.append(new_ball)
                    # Asignar referencia del gestor de sonidos
                    new_ball.game_sound_manager = self.sound_manager
            self.active_power_ups["multi_ball"] = (
                1800  # 30 segundos (tiempo arbitrario)
            )
            # Reproducir sonido específico de multi_ball
            self.sound_manager.play("multi_ball")
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
                    if (
                        current_speed > 0
                    ):  # Evitar división por cero si la pelota está quieta
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

    def build_background(self):
        """
        Dibuja una sola vez el fondo synthwave completo: cielo púrpura con
        estrellas, gran disco detrás del mueble, líneas neón en el horizonte
        y el banner superior. Se cachea en self.background_surface.
        """
        surface = self.background_surface

        # Degradado vertical: púrpura profundo arriba, violáceo casi negro abajo
        surface.blit(
            make_gradient_surface(
                (SCREEN_WIDTH, SCREEN_HEIGHT), BG_TOP, BG_BOTTOM, radius=0, gloss=False
            ),
            (0, 0),
        )

        # Campo de estrellas con brillo variable (mismo resultado en cada partida)
        stars = random.Random(20250715)
        for _ in range(150):
            star_x = stars.randint(0, SCREEN_WIDTH - 1)
            star_y = stars.randint(0, SCREEN_HEIGHT - 1)
            brightness = stars.randint(50, 150)
            star_size = 1 if stars.random() < 0.85 else 2
            pygame.draw.circle(
                surface,
                (brightness, brightness - 10, min(255, brightness + 25)),
                (star_x, star_y),
                star_size,
            )

        # Gran disco oscuro detrás del mueble (decorado retrowave)
        pygame.draw.circle(surface, (33, 13, 62), (SCREEN_WIDTH // 2, 480), 350)
        pygame.draw.circle(surface, (42, 18, 76), (SCREEN_WIDTH // 2, 480), 350, 2)

        # Líneas neón del horizonte (a la altura de la rejilla del mueble)
        horizon_y = PLAY_OFFSET_Y + 372
        surface.blit(
            make_horizon_surface(SCREEN_WIDTH, 26, (255, 45, 149)),
            (0, horizon_y - 13),
        )
        pygame.draw.line(
            surface, (255, 120, 195), (0, horizon_y), (SCREEN_WIDTH, horizon_y), 2
        )
        pygame.draw.line(
            surface,
            (255, 200, 230),
            (SCREEN_WIDTH // 2 - 320, horizon_y),
            (SCREEN_WIDTH // 2 + 320, horizon_y),
            1,
        )
        surface.blit(
            make_horizon_surface(SCREEN_WIDTH, 12, (255, 45, 149)),
            (0, horizon_y + 26),
        )

        # Banner superior estilo arcade: marco rosa y logotipo con degradado
        bx, by, bw, bh = BANNER_RECT
        draw_panel(surface, BANNER_RECT, (24, 10, 48, 235), 18, (255, 45, 149, 200))

        # Líneas de velocidad cian a ambos lados del logotipo
        streak_specs = [
            (70, 3, (0, 224, 255)),
            (52, 2, (0, 190, 220)),
            (62, 2, (0, 224, 255)),
            (40, 1, (140, 245, 255)),
        ]
        for index, (length, thick, color) in enumerate(streak_specs):
            streak_y = by + 18 + index * 10
            surface.blit(make_streak_surface(length, thick, color), (bx + 30, streak_y))
            surface.blit(
                make_streak_surface(length, thick, color, reverse=True),
                (bx + bw - 24 - length, streak_y),
            )

        # Logotipo con degradado cian -> verde y resplandor rosa
        title = render_styled_title(
            "ARKANOID", 44, (0, 235, 255), (170, 255, 90), (255, 30, 120), spacing=2
        )
        title_pos = (bx + 140, by + (bh - title.get_height()) // 2)
        surface.blit(title, title_pos)

        # Subtítulo cursiva junto al logotipo
        draw_text(
            surface,
            "Neon breakout · cabinet no. 38",
            14,
            (120, 235, 235),
            (title_pos[0] + title.get_width() - 24, by + bh // 2 + 2),
            align="midleft",
            italic=True,
            spacing=1,
        )

        # El resto de piezas cacheadas del decorado
        self.build_field_background()
        self.build_cabinet()

        # Máscara para las esquinas redondeadas de la pantalla del mueble
        self.field_mask = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.field_mask,
            (255, 255, 255, 255),
            (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            border_radius=16,
        )

    def build_field_background(self):
        """
        Pre-renderiza el fondo de la zona de juego: cielo nocturno, sol
        synthwave con franjas, montañas con neón cian y rejilla en
        perspectiva (el clásico horizonte retrowave).
        """
        width, height = WINDOW_WIDTH, WINDOW_HEIGHT
        horizon_y = 372
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Cielo: degradado azul violáceo profundo
        surface.blit(
            make_gradient_surface(
                (width, height), (30, 16, 62), (12, 6, 30), gloss=False
            ),
            (0, 0),
        )

        # Estrellas tenues en la zona superior
        stars = random.Random(88038)
        for _ in range(55):
            star_x = stars.randint(2, width - 3)
            star_y = stars.randint(2, 250)
            brightness = stars.randint(90, 200)
            surface.set_at(
                (star_x, star_y), (brightness, brightness, min(255, brightness + 30))
            )

        # Sol synthwave con franjas horizontales
        surface.blit(make_sunset_surface(192), (width // 2 - 96, 212))

        # Montañas con contorno neón cian a ambos lados del sol
        mountains = [
            [(0, horizon_y), (48, 302), (92, 348), (140, 292), (196, horizon_y)],
            [(344, horizon_y), (400, 296), (448, 350), (496, 306), (width, horizon_y)],
        ]
        for points in mountains:
            pygame.draw.polygon(
                surface,
                (28, 13, 56),
                points + [(points[-1][0], horizon_y + 2), (points[0][0], horizon_y + 2)],
            )
            for index in range(len(points) - 1):
                start, end = points[index], points[index + 1]
                pygame.draw.line(surface, (0, 140, 170), start, end, 4)
                pygame.draw.line(surface, (0, 235, 255), start, end, 2)

        # Suelo oscuro bajo el horizonte
        pygame.draw.rect(
            surface, (14, 6, 32), (0, horizon_y, width, height - horizon_y)
        )

        # Rejilla en perspectiva (líneas magenta que convergen en el horizonte)
        rows = 12
        for index in range(1, rows + 1):
            ratio = (index / rows) ** 1.9
            line_y = int(horizon_y + (height - horizon_y) * ratio)
            pygame.draw.line(surface, (255, 45, 149), (0, line_y), (width, line_y), 2)
            pygame.draw.line(
                surface, (255, 150, 205), (0, line_y), (width, line_y), 1
            )

        # Líneas verticales hacia el punto de fuga
        vanish_x = width // 2
        for step in range(-6, 7):
            bottom_x = vanish_x + step * 84
            pygame.draw.line(
                surface, (255, 45, 149), (vanish_x, horizon_y), (bottom_x, height), 2
            )

        # Línea del horizonte
        pygame.draw.line(
            surface, (255, 226, 60), (0, horizon_y), (width, horizon_y), 1
        )

        self.field_background = surface

    def build_cabinet(self):
        """Pre-renderiza el marco del mueble: resplandor rosa, bisel y línea amarilla."""
        _, _, width, height = CABINET_RECT
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        # Resplandor rosa exterior
        surf.blit(
            make_panel_surface((width + 30, height + 30), (*ACCENT_PINK, 30), 44),
            (-15, -15),
        )

        # Bisel del mueble
        pygame.draw.rect(
            surf, (255, 70, 165), (4, 4, width - 8, height - 8), 8, border_radius=26
        )
        pygame.draw.rect(
            surf, (255, 180, 220), (8, 8, width - 16, height - 16), 2, border_radius=22
        )

        # Línea amarilla interior que encuadra la zona de juego
        pygame.draw.rect(
            surf,
            (255, 226, 60),
            (11, 11, width - 22, height - 22),
            1,
            border_radius=20,
        )

        self.cabinet_surface = surf

    def draw_background(self):
        """Dibuja el fondo completo cacheado (cielo, banner y decorado)."""
        self.screen.blit(self.background_surface, (0, 0))

    def draw(self):
        # El fondo completo (cielo, banner y decorado) está cacheado; la zona
        # de juego se dibuja en una superficie intermedia para poder aplicar
        # el temblor de pantalla cuando la pelota golpea con fuerza
        self.screen.blit(self.background_surface, (0, 0))

        world = self.world_surface
        world.blit(self.field_background, (0, 0))

        if self.game_state != "menu":
            self.draw_game(world)

        # Recorte de esquinas redondeadas de la pantalla del mueble
        world.blit(self.field_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Temblor de pantalla: desplaza la escena un par de píxeles al azar
        offset_x = offset_y = 0
        if self.screen_shake > 0:
            shake_power = min(self.screen_shake, 8)
            offset_x = random.randint(-shake_power, shake_power)
            offset_y = random.randint(-shake_power, shake_power)

        self.screen.blit(
            world, (PLAY_OFFSET_X + offset_x, PLAY_OFFSET_Y + offset_y)
        )

        # Marco del mueble, paneles laterales y botones inferiores
        self.screen.blit(self.cabinet_surface, (CABINET_RECT[0], CABINET_RECT[1]))
        self.draw_side_panels(self.screen)
        self.draw_bottom_buttons(self.screen)

        # Capas de estado: menú, pausa o pantallas de resultado
        if self.game_state == "menu":
            self.draw_menu(self.screen)
        elif self.game_state == "playing" and self.paused:
            self.draw_pause(self.screen)
        elif self.game_state == "game_over":
            self.draw_game_over(self.screen)
        elif self.game_state == "victory":
            self.draw_victory(self.screen)

        pygame.display.flip()

    def draw_menu(self, screen):
        """Dibuja la tarjeta de controles del menú sobre la pantalla del mueble."""
        center_x = PLAY_OFFSET_X + WINDOW_WIDTH // 2
        now = pygame.time.get_ticks()

        # Tarjeta translúcida sobre la zona de juego
        card_x, card_y, card_w, card_h = 386, 150, 508, 470
        draw_panel(
            screen, (card_x, card_y, card_w, card_h), (22, 10, 46, 225), 20,
            (255, 45, 149, 170),
        )
        draw_text(
            screen,
            "CONTROLES",
            15,
            TEXT_DIM,
            (center_x, card_y + 28),
            align="center",
            spacing=10,
            italic=True,
        )

        # Dos columnas de controles (tecla + descripción)
        for index, (key_name, description) in enumerate(self.menu_controls):
            column = index // 6
            row = index % 6
            key_x = card_x + 24 + column * 244
            key_y = card_y + 58 + row * 38

            # Tecla con aspecto de cristal y borde neón
            label = render_text(key_name, 12, ACCENT_CYAN, bold=True, spacing=1, italic=True)
            key_width = max(44, label.get_width() + 18)
            keycap = make_panel_surface(
                (key_width, 24), (30, 16, 60, 235), 7, (*ACCENT_CYAN, 140)
            )
            screen.blit(keycap, (key_x, key_y))
            screen.blit(
                label,
                (
                    key_x + (key_width - label.get_width()) // 2,
                    key_y + (24 - label.get_height()) // 2,
                ),
            )

            # Descripción del control
            draw_text(
                screen,
                description,
                13,
                TEXT_PRIMARY,
                (key_x + key_width + 10, key_y + 12),
                align="midleft",
            )

        # Botón principal pulsante
        pulse = (math.sin(now * 0.005) + 1) / 2
        draw_pill_button(
            screen,
            (center_x - 205, card_y + 310, 410, 50),
            "PULSA ESPACIO PARA JUGAR",
            ACCENT_PINK,
            pulse,
            font_size=17,
        )

        # Puntuación máxima
        draw_text(
            screen,
            "RÉCORD",
            14,
            TEXT_DIM,
            (center_x - 14, card_y + 395),
            align="midright",
            spacing=5,
            italic=True,
        )
        draw_text(
            screen,
            f"{self.high_score:06d}",
            24,
            NEON_YELLOW,
            (center_x + 14, card_y + 395),
            align="midleft",
            bold=True,
            italic=True,
            cached=False,
        )

        # Información de la edición
        draw_text(
            screen,
            "36 NIVELES · 5 POWER-UPS · FÍSICA DE REBOTE POR ÁNGULOS",
            10,
            TEXT_DIM,
            (center_x, card_y + 435),
            align="center",
            spacing=1,
            italic=True,
        )

    def draw_game(self, screen):
        """Dibuja los elementos del juego dentro de la zona de juego."""
        # Elementos del juego (los ladrillos quedan detrás del resto)
        for brick in self.bricks:
            brick.draw(screen)

        self.paddle.draw(screen)

        for ball in self.balls:
            ball.draw(screen)

        for power_up in self.power_ups:
            power_up.draw(screen)

        for laser in self.lasers:
            laser.draw(screen)

        # Partículas de efectos y textos flotantes de puntos
        for particle in self.particles:
            particle.draw(screen)

        for popup in self.score_popups:
            popup.draw(screen)

        # Aviso de pelota lista para lanzar
        if self.waiting_for_ball_release:
            pulse = (math.sin(pygame.time.get_ticks() * 0.006) + 1) / 2
            draw_pill_button(
                screen,
                (WINDOW_WIDTH // 2 - 190, WINDOW_HEIGHT - 165, 380, 46),
                "CLIC O ESPACIO PARA LANZAR",
                ACCENT_PINK,
                pulse,
                font_size=18,
            )

            # Flecha animada apuntando a la pelota pegada
            for ball in self.balls:
                if ball.stuck_to_paddle:
                    bob = int(math.sin(pygame.time.get_ticks() * 0.01) * 3)
                    arrow_y = int(ball.y) - 32 + bob
                    draw_glow_dot(
                        screen, ACCENT_PINK, (int(ball.x), arrow_y + 6), 8, alpha=120
                    )
                    pygame.draw.polygon(
                        screen,
                        ACCENT_PINK,
                        [
                            (int(ball.x) - 9, arrow_y),
                            (int(ball.x) + 9, arrow_y),
                            (int(ball.x), arrow_y + 12),
                        ],
                    )

    def draw_side_panels(self, screen):
        """Paneles laterales estilo retro: puntos, récord, nivel, vidas,
        velocidad, power-ups y controles (como un mueble arcade)."""
        # ---- Columna izquierda ----
        self._draw_info_panel(
            screen, (54, 240, 250, 92), "PUNTOS", f"{self.score:06d}", (255, 84, 175)
        )
        self._draw_info_panel(
            screen,
            (54, 344, 250, 92),
            "HI-SCORE",
            f"{self.high_score:06d}",
            (255, 84, 175),
        )

        # Nivel: número grande + nombre del patrón
        draw_panel(screen, (54, 448, 250, 112), (22, 10, 44, 210), 16, (255, 45, 149, 150))
        draw_text(screen, "NIVEL", 13, TEXT_DIM, (78, 466), spacing=6, italic=True)
        draw_text(
            screen,
            f"{self.level:02d}",
            40,
            ACCENT_CYAN,
            (78, 482),
            bold=True,
            italic=True,
            cached=False,
            glow=2,
        )
        pattern_name = LEVEL_NAMES[(self.level - 1) % len(LEVEL_NAMES)].upper()
        draw_text(
            screen,
            pattern_name,
            12,
            (255, 110, 195),
            (78, 534),
            italic=True,
            spacing=1,
        )

        # Vidas: pequeñas cápsulas cian
        draw_panel(screen, (54, 572, 250, 80), (22, 10, 44, 210), 16, (255, 45, 149, 150))
        draw_text(screen, "VIDAS", 13, TEXT_DIM, (78, 590), spacing=6, italic=True)
        for index in range(min(self.lives, 5)):
            pill = make_gradient_surface(
                (32, 14),
                lerp_color(ACCENT_CYAN, (255, 255, 255), 0.35),
                shade(ACCENT_CYAN, 0.5),
                7,
            )
            screen.blit(pill, (78 + index * 42, 614))

        # ---- Columna derecha ----
        # Velocidad: multiplicador + barra (estilo indicador arcade)
        speed_ratio = 0.0
        if self.balls and not self.waiting_for_ball_release:
            ball_speed = math.sqrt(
                self.balls[0].speed_x ** 2 + self.balls[0].speed_y ** 2
            )
            speed_ratio = ball_speed / INITIAL_BALL_SPEED
        self._draw_info_panel(
            screen,
            (976, 240, 250, 92),
            "VELOCIDAD",
            f"×{max(0.0, speed_ratio):.1f}",
            NEON_YELLOW,
        )
        pygame.draw.rect(screen, (50, 30, 90), (1000, 312, 202, 6), border_radius=3)
        fill_width = int(202 * min(1.0, speed_ratio / 2.0))
        if fill_width > 0:
            bar = make_gradient_surface(
                (fill_width, 6), NEON_YELLOW, ACCENT_PINK, 3, gloss=False
            )
            screen.blit(bar, (1000, 312))

        self._draw_power_ups(screen)
        self._draw_controls_panel(screen)

    def _draw_info_panel(self, screen, rect, label, value, value_color, value_size=34):
        """Panel de estadística: etiqueta pequeña y valor grande cursiva con brillo."""
        x, y, _, _ = rect
        draw_panel(screen, rect, (22, 10, 44, 210), 16, (255, 45, 149, 150))
        draw_text(screen, label, 13, TEXT_DIM, (x + 24, y + 16), spacing=6, italic=True)
        draw_text(
            screen,
            value,
            value_size,
            value_color,
            (x + 24, y + 34),
            bold=True,
            italic=True,
            cached=False,
            glow=2,
        )

    def _draw_power_ups(self, screen):
        """Panel derecho con la leyenda de power-ups y sus temporizadores."""
        draw_panel(screen, (976, 344, 250, 232), (22, 10, 44, 210), 16, (255, 45, 149, 150))
        draw_text(screen, "POWER-UPS", 13, TEXT_DIM, (1000, 362), spacing=6, italic=True)

        names = {
            "expand": "Paleta ancha",
            "multi_ball": "Multibola",
            "slow_ball": "Bola lenta",
            "destroyer_ball": "Bola destructora",
            "laser_shoot": "Láser doble",
        }
        for index, (power_type, timer) in enumerate(self.active_power_ups.items()):
            color = POWER_UP_COLORS.get(power_type, WHITE)
            symbol = POWER_UP_SYMBOLS.get(power_type, "?")
            row_y = 392 + index * 36
            active = timer > 0

            # Cápsula con la letra del power-up
            pill_color = color if active else shade(color, 0.35)
            pill = make_gradient_surface(
                (28, 16),
                lerp_color(pill_color, (255, 255, 255), 0.3),
                shade(pill_color, 0.5),
                8,
            )
            screen.blit(pill, (1000, row_y))
            draw_text(
                screen,
                symbol,
                11,
                WHITE if active else (170, 160, 190),
                (1014, row_y + 8),
                align="center",
                bold=True,
                shadow=True,
            )

            # Nombre del power-up (atenuado si no está activo)
            name_color = TEXT_PRIMARY if active else TEXT_DIM
            draw_text(
                screen,
                names[power_type],
                13,
                name_color,
                (1038, row_y + 8),
                align="midleft",
                italic=True,
            )

            # Barra de tiempo restante
            pygame.draw.rect(screen, (50, 30, 90), (1038, row_y + 20, 160, 4), border_radius=2)
            if active:
                ratio = timer / max(1, POWER_UP_DURATIONS.get(power_type, 1))
                bar_width = int(160 * min(1.0, ratio))
                pygame.draw.rect(
                    screen, color, (1038, row_y + 20, bar_width, 4), border_radius=2
                )

    def _draw_controls_panel(self, screen):
        """Panel derecho con los controles resumidos (teclas + descripción)."""
        draw_panel(screen, (976, 588, 250, 152), (22, 10, 44, 210), 16, (255, 45, 149, 150))
        draw_text(screen, "CONTROLES", 13, TEXT_DIM, (1000, 606), spacing=6, italic=True)

        rows = [
            ("← →", "o ratón · mover"),
            ("ESPACIO", "lanzar"),
            ("P", "pausa"),
            ("B", "bola extra"),
            ("N", "sonido"),
        ]
        for index, (key_name, description) in enumerate(rows):
            row_y = 634 + index * 21
            label = render_text(key_name, 10, ACCENT_CYAN, bold=True, spacing=1)
            key_width = max(34, label.get_width() + 14)
            keycap = make_panel_surface(
                (key_width, 16), (30, 16, 60, 235), 5, (*ACCENT_CYAN, 130)
            )
            screen.blit(keycap, (1000, row_y))
            screen.blit(
                label,
                (
                    1000 + (key_width - label.get_width()) // 2,
                    row_y + (16 - label.get_height()) // 2,
                ),
            )
            draw_text(
                screen,
                description,
                12,
                TEXT_PRIMARY,
                (1000 + key_width + 10, row_y + 8),
                align="midleft",
                italic=True,
            )

    def draw_bottom_buttons(self, screen):
        """Botones inferiores estilo máquina recreativa (sonido, modo y pausa)."""
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
        sound_label = "♪ SONIDO" if self.sound_manager.enabled else "♪ SILENCIO"
        draw_pill_button(
            screen, (331, 782, 180, 46), sound_label, ACCENT_CYAN, pulse, font_size=16
        )
        draw_pill_button(
            screen, (535, 782, 210, 46), "FREE PLAY", (255, 170, 60), pulse, font_size=17
        )
        pause_label = "▶ SEGUIR" if self.paused else "II PAUSA"
        draw_pill_button(
            screen, (769, 782, 180, 46), pause_label, ACCENT_PINK, pulse, font_size=16
        )

    def draw_pause(self, screen):
        """Dibuja el aviso de pausa con una tarjeta de cristal."""
        # Fondo atenuado
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 4, 26, 190))
        screen.blit(overlay, (0, 0))

        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        # Tarjeta de cristal
        draw_panel(
            screen,
            (center_x - 220, center_y - 115, 440, 230),
            (22, 10, 46, 235),
            22,
            (255, 45, 149, 160),
        )

        # Título y aviso
        draw_text(
            screen,
            "PAUSA",
            52,
            ACCENT_PINK,
            (center_x, center_y - 45),
            align="center",
            bold=True,
            spacing=10,
            glow=2,
            italic=True,
        )
        draw_text(
            screen,
            "El juego está esperando",
            19,
            TEXT_DIM,
            (center_x, center_y + 10),
            align="center",
            italic=True,
        )

        # Botón de reanudar
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
        draw_pill_button(
            screen,
            (center_x - 155, center_y + 40, 310, 46),
            "P PARA REANUDAR",
            ACCENT_CYAN,
            pulse,
            font_size=18,
        )

    def draw_result_screen(
        self, screen, title, title_color, rows, button_label, badge=None
    ):
        """
        Pantalla de resultados (derrota o victoria): fondo atenuado,
        tarjeta de cristal con las estadísticas y un botón pulsante.
        """
        # Fondo atenuado
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 4, 26, 205))
        screen.blit(overlay, (0, 0))

        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        # Tarjeta de cristal
        draw_panel(
            screen,
            (center_x - 280, center_y - 170, 560, 340),
            (22, 10, 46, 235),
            22,
            (255, 45, 149, 160),
        )

        # Título con halo neón (el tamaño se adapta para no desbordar)
        title_size = 44
        while (
            title_size > 28
            and render_text(title, title_size, title_color, True, 5).get_width() > 500
        ):
            title_size -= 2
        draw_text(
            screen,
            title,
            title_size,
            title_color,
            (center_x, center_y - 112),
            align="center",
            bold=True,
            spacing=5,
            glow=2,
            italic=True,
        )

        # Filas de estadísticas (etiqueta a la izquierda, valor a la derecha)
        row_y = center_y - 44
        for label, value, value_color in rows:
            draw_text(
                screen,
                label,
                14,
                TEXT_DIM,
                (center_x - 215, row_y + 12),
                align="midleft",
                spacing=4,
                italic=True,
            )
            draw_text(
                screen,
                value,
                25,
                value_color,
                (center_x + 215, row_y + 12),
                align="midright",
                bold=True,
                cached=False,
                italic=True,
            )
            pygame.draw.line(
                screen,
                (90, 45, 120),
                (center_x - 215, row_y + 32),
                (center_x + 215, row_y + 32),
                1,
            )
            row_y += 46

        # Insignia de récord (opcional)
        if badge:
            draw_text(
                screen,
                badge,
                17,
                NEON_YELLOW,
                (center_x, center_y + 52),
                align="center",
                bold=True,
                spacing=4,
                glow=1,
                italic=True,
            )

        # Botón de acción
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
        draw_pill_button(
            screen,
            (center_x - 195, center_y + 92, 390, 50),
            button_label,
            ACCENT_CYAN,
            pulse,
            font_size=18,
        )

    def draw_game_over(self, screen):
        """Dibuja la pantalla de derrota con tarjeta de cristal."""
        rows = [
            ("PUNTUACIÓN FINAL", f"{self.score:06d}", NEON_YELLOW),
            ("RÉCORD", f"{self.high_score:06d}", TEXT_PRIMARY),
        ]
        badge = None
        if self.score > 0 and self.score == self.high_score:
            badge = "¡NUEVO RÉCORD!"
        self.draw_result_screen(
            screen,
            "GAME OVER",
            ACCENT_PINK,
            rows,
            "ESPACIO · REINTENTAR",
            badge,
        )

    def draw_victory(self, screen):
        """Dibuja la pantalla de nivel completado con tarjeta de cristal."""
        next_pattern_name = LEVEL_NAMES[self.level % len(LEVEL_NAMES)].upper()
        rows = [
            ("PUNTUACIÓN", f"{self.score:06d}", NEON_YELLOW),
            ("SIGUIENTE NIVEL", next_pattern_name, ACCENT_CYAN),
        ]
        self.draw_result_screen(
            screen,
            "¡NIVEL SUPERADO!",
            NEON_YELLOW,
            rows,
            "ESPACIO · SIGUIENTE NIVEL",
        )

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
