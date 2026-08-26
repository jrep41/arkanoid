# Arkanoid - Edición Mejorada

Un juego completo de Arkanoid desarrollado en Python usando pygame con características avanzadas y 36 niveles originales.

## 🎮 Características Principales

### **Jugabilidad Clásica Mejorada**

- **36 niveles originales**: Patrones únicos inspirados en el Arkanoid clásico
- **Control dual**: Ratón (recomendado) o teclado para máxima precisión
- **Sistema de vidas extendido**: 10 vidas para una experiencia más relajada
- **Física realista**: Rebote inteligente basado en el punto de impacto en la paleta

### **Sistema de Power-ups Avanzado**

- 🟢 **E (Expand)**: Expande el tamaño de la paleta temporalmente
- 🟡 **M (Multi-ball)**: Agrega 2 pelotas adicionales (máximo 5 simultáneas)
- 🟣 **S (Slow)**: Reduce la velocidad de todas las pelotas
- 🔴 **D (Destroyer)**: Las pelotas destruyen ladrillos de un golpe (10 segundos)
- 🔴 **L (Laser)**: Activa cañones láser duales (10 segundos)

### **Sistema de Resistencia de Ladrillos**

- **Resistencia simplificada**: 1, 2 o 3 golpes máximo
- **Indicadores visuales**: Números que muestran golpes restantes
- **Colores optimizados**: Texto con contraste automático para máxima legibilidad
- **Mapeo de resistencia**:
  - Rojo/Naranja: 3 golpes (máxima resistencia)
  - Amarillo/Magenta/Cian/Verde: 2 golpes (resistencia media)
  - Azul/Gris: 1 golpe (baja resistencia)

### **Controles Avanzados**

- **Control de ratón**: Captura/liberación automática con tecla ESC
- **Cañones láser duales**: Disparo continuo con clic izquierdo sostenido
- **Pelota pegajosa**: La pelota se adhiere a la paleta al inicio de cada vida
- **Pelota extra**: Tecla B para agregar pelotas adicionales

## 🎯 Requisitos

- Python 3.7 o superior
- pygame 2.0 o superior

## 📦 Instalación

1. Clona o descarga este repositorio
2. Instala pygame:

   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Cómo Jugar

1. Ejecuta el juego:

   ```bash
   python arkanoid_enhanced.py
   ```

2. **Controles**:

   - **Ratón**: Movimiento de la paleta (recomendado)
   - **Flechas** o **A/D**: Movimiento alternativo con teclado
   - **Clic izquierdo** o **Espacio**: Lanzar pelota / Disparar láser
   - **Mantener clic izquierdo**: Disparo láser continuo
   - **B**: Agregar pelota extra (máximo 5)
   - **ESC**: Alternar captura del ratón
   - **Espacio**: Comenzar/Reiniciar/Siguiente nivel

3. **Objetivo**:
   - Destruye todos los ladrillos para completar el nivel
   - Recoge power-ups para obtener ventajas especiales
   - Progresa a través de los 36 niveles únicos

## 🛠️ Mecánicas Avanzadas

### **Sistema de Colisiones Inteligente**

- **Cooldown de colisión**: Previene hits múltiples no deseados
- **Detección precisa**: Sistema de rectángulos optimizado
- **Rebote realista**: Ángulo basado en la posición de impacto

### **Efectos Visuales**

- **Rastros de movimiento**: Efectos de trail para pelotas y láser
- **Partículas dinámicas**: Explosiones al destruir ladrillos
- **Temblor de pantalla**: Feedback visual en impactos importantes
- **Efectos de brillo**: Resaltado en pelotas y power-ups
- **Modo destructor visual**: Pelota roja pulsante con anillo dorado

### **Sistema de Balance**

- **Probabilidad de power-ups**: 15% (optimizada desde 35%)
- **Duración de láser**: 10 segundos (balanceada desde 24s)
- **Velocidad de pelota**: Incremento gradual por nivel
- **Sistema de puntuación**: Bonificaciones por nivel y tipo de ladrillo

## 🏗️ Estructura del Código

### **Clases Principales**

- **`Game`**: Controlador principal del juego y estados
- **`Paddle`**: Paleta con cañones láser duales y expansión
- **`Ball`**: Pelota con modo destructor y física avanzada
- **`Brick`**: Ladrillos con sistema de resistencia y efectos visuales
- **`PowerUp`**: Power-ups con rotación y símbolos identificativos
- **`Laser`**: Proyectiles láser con rastros y colisiones
- **`Particle`**: Sistema de partículas para efectos visuales

### **Características Técnicas**

- **60 FPS constantes**: Framerate estable y suave
- **Física realista**: Cálculos trigonométricos precisos
- **Gestión de memoria**: Limpieza automática de objetos
- **Sistema de estados**: Menú, juego, victoria y game over
- **Guardado automático**: Puntuación máxima persistente

## 🎨 Niveles y Patrones

El juego incluye 36 patrones únicos inspirados en el Arkanoid original:

- Rectángulo Clásico, Pirámide, Rombo, Torres Laterales
- Escalera, Cruz, Círculos Concéntricos, Zigzag
- Patrón Lateral, Espiral, Laberinto, Ondas
- Arco, Estrella, Escalera Doble, Diamante
- Y muchos más patrones únicos y desafiantes...

## 🏆 Características de Accesibilidad

- **Contraste automático**: Texto visible en todos los colores de ladrillos
- **Múltiples métodos de control**: Ratón y teclado
- **Indicadores visuales claros**: Flechas, contadores y símbolos
- **Feedback audiovisual**: Efectos de pantalla y partículas

## 🔄 Actualizaciones Recientes

### Versión 2.0 - Edición Mejorada

- ✅ Implementados 36 niveles originales con patrones únicos
- ✅ Sistema de control dual (ratón + teclado)
- ✅ Cañones láser duales con disparo continuo
- ✅ Power-up "Destroyer Ball" para destrucción instantánea
- ✅ Sistema de resistencia simplificado (1-3 golpes)
- ✅ Mejoras de accesibilidad visual
- ✅ Balance de gameplay optimizado
- ✅ Efectos visuales avanzados

¡Disfruta de la experiencia completa de Arkanoid con todas las mejoras modernas!
