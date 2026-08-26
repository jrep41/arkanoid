# Guía de Instalación - Arkanoid

## Instalación Rápida

### Paso 1: Verificar Python

Asegúrate de tener Python 3.7 o superior instalado:

```bash
python --version
```

### Paso 2: Instalar Dependencias

```bash
pip install pygame
```

### Paso 3: Ejecutar el Juego

```bash
python arkanoid.py
```

## Instalación Detallada

### Opción 1: Usar el entorno virtual (Recomendado)

Ya está configurado en este proyecto. Solo ejecuta:

```bash
# Windows
run_game.bat
# o
powershell -ExecutionPolicy Bypass -File run_game.ps1
```

### Opción 2: Instalación manual

1. Abre una terminal en la carpeta del proyecto
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:

   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

4. Instala pygame:
   ```bash
   pip install -r requirements.txt
   ```
5. Ejecuta el juego:
   ```bash
   python arkanoid.py
   ```

## Versiones Disponibles

### arkanoid.py (Versión Básica)

- ✅ Gameplay completo de Arkanoid
- ✅ Power-ups básicos
- ✅ Sistema de puntuación
- ✅ Múltiples niveles
- ✅ Control con teclado

### arkanoid_enhanced.py (Versión Mejorada)

- ✅ Todo lo de la versión básica
- ✅ Efectos de partículas
- ✅ Rastro de la pelota
- ✅ Temblor de pantalla
- ✅ Fondo animado con estrellas
- ✅ Puntuación máxima guardada
- ✅ Animaciones mejoradas
- ✅ Power-ups con efectos visuales

## Controles del Juego

- **Flecha Izquierda** o **A**: Mover paleta a la izquierda
- **Flecha Derecha** o **D**: Mover paleta a la derecha
- **Espacio**: Comenzar juego / Reiniciar / Siguiente nivel
- **Escape**: Salir del juego

## Power-ups Disponibles

- 🟢 **E (Expand)**: Expande el tamaño de la paleta
- 🟡 **M (Multi-ball)**: Agrega pelotas adicionales
- 🟣 **S (Slow)**: Reduce la velocidad de las pelotas
- 🔴 **F (Fast Paddle)**: Aumenta la velocidad de la paleta (solo en versión mejorada)

## Solución de Problemas

### Error: "No module named 'pygame'"

```bash
pip install pygame
```

### Error: "python no se reconoce como comando"

- Asegúrate de que Python esté instalado y en el PATH del sistema
- En Windows, reinstala Python marcando "Add to PATH"

### El juego va muy lento

- Cierra otros programas para liberar recursos
- Actualiza los drivers de tu tarjeta gráfica

### No se escucha sonido (versión futura)

- Verifica que el audio del sistema esté activado
- Asegúrate de que los archivos de sonido estén en la carpeta correcta

## Archivos del Proyecto

```
arkanoid/
├── arkanoid.py              # Versión básica del juego
├── arkanoid_enhanced.py     # Versión mejorada con efectos
├── requirements.txt         # Dependencias de Python
├── README.md               # Documentación principal
├── INSTALACION.md          # Esta guía de instalación
├── EXTENSIONES.md          # Ideas para futuras mejoras
├── run_game.bat            # Script de Windows para ejecutar
├── run_game.ps1            # Script de PowerShell para ejecutar
└── high_score.txt          # Puntuación máxima (se crea automáticamente)
```

## Requisitos del Sistema

- **Sistema Operativo**: Windows, macOS, Linux
- **Python**: 3.7 o superior
- **RAM**: Mínimo 512 MB
- **Espacio en disco**: 50 MB
- **Resolución**: Mínimo 800x600

¡Disfruta jugando Arkanoid!
