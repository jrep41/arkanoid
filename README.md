# Arkanoid - Juego en Python

Un juego completo de Arkanoid desarrollado en Python usando pygame.

## Características

- **Jugabilidad clásica**: Controla una paleta para hacer rebotar una pelota y destruir ladrillos
- **Múltiples niveles**: Avanza a través de niveles cada vez más desafiantes
- **Power-ups**: Recoge mejoras especiales:
  - 🟢 **E (Expand)**: Expande el tamaño de la paleta
  - 🟡 **M (Multi-ball)**: Agrega pelotas adicionales al juego
  - 🟣 **S (Slow)**: Reduce la velocidad de las pelotas
- **Efectos visuales**: Ladrillos con efecto 3D y animaciones suaves
- **Sistema de puntuación**: Gana puntos destruyendo ladrillos
- **Múltiples vidas**: Tienes 3 vidas para completar cada nivel

## Requisitos

- Python 3.7 o superior
- pygame

## Instalación

1. Clona o descarga este repositorio
2. Instala pygame:
   ```
   pip install pygame
   ```

## Cómo jugar

1. Ejecuta el juego:

   ```
   python arkanoid.py
   ```

2. **Controles**:

   - **Flecha izquierda** o **A**: Mover paleta a la izquierda
   - **Flecha derecha** o **D**: Mover paleta a la derecha
   - **Espacio**: Comenzar juego / Reiniciar / Siguiente nivel
   - **Esc**: Salir del juego

3. **Objetivo**:
   - Destruye todos los ladrillos para completar el nivel
   - No dejes que la pelota caiga fuera de la pantalla
   - Recoge power-ups para obtener ventajas especiales

## Mecánicas del juego

- **Rebote inteligente**: El ángulo de rebote de la pelota depende de dónde golpee la paleta
- **Colores de ladrillos**: Diferentes colores para hacer el juego más visualmente atractivo
- **Power-ups aleatorios**: 10% de probabilidad de que aparezca un power-up al destruir un ladrillo
- **Progresión de niveles**: Cada nivel completado aumenta la dificultad

## Estructura del código

- **Clase Game**: Maneja el estado del juego, eventos y renderizado
- **Clase Paddle**: Controla la paleta del jugador
- **Clase Ball**: Maneja el movimiento y colisiones de la pelota
- **Clase Brick**: Representa los ladrillos destructibles
- **Clase PowerUp**: Gestiona los power-ups especiales

## Características técnicas

- Framerate constante de 60 FPS
- Detección de colisiones precisas
- Física realista de rebote
- Menús interactivos
- Sistema de estados del juego

¡Disfruta jugando Arkanoid!
