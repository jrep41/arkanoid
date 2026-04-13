"""
MÓDULO DE SONIDOS PARA ARKANOID
===============================
Genera efectos de sonido sintéticos usando pygame.
No requiere archivos de audio externos ni numpy.

Autor: Claude
Fecha: Abril 2026
"""

import pygame
import math
import struct

# Inicializar mixer si no está ya inicializado
try:
    pygame.mixer.init()
except pygame.error:
    pass


def generate_beep(frequency, duration, volume=0.3, fadeout=50):
    """
    Genera un beep simple usando pygame.
    """
    sample_rate = 22050
    n_samples = int(sample_rate * duration / 1000)

    # Crear datos de sonido
    samples = []
    attack_samples = int(sample_rate * 0.02)
    decay_samples = int(sample_rate * fadeout / 1000)

    for i in range(n_samples):
        # Generar onda sinusoidal
        t = i / sample_rate
        value = math.sin(2 * math.pi * frequency * t)

        # Envolvente
        if i < attack_samples:
            value *= i / attack_samples
        elif i > n_samples - decay_samples:
            value *= (n_samples - i) / decay_samples

        samples.append(int(value * volume * 32767))

    # Crear array de bytes (16-bit, mono)
    sound_bytes = struct.pack(f'<{n_samples}h', *samples)

    # Crear superficie de sonido
    sound_surface = pygame.Surface((n_samples, 1), pygame.SRCALPHA)
    pygame.mixer.init()
    sound = pygame.mixer.Sound(buffer=sound_bytes)
    return sound


def generate_tone(frequency, duration, volume=0.25, frequency_end=None):
    """
    Genera un tono simple con fadeout.
    Si frequency_end es diferente, hace un sweep.
    """
    sample_rate = 22050
    n_samples = int(sample_rate * duration / 1000)

    samples = []

    # Fadeout samples
    fade_samples = max(1, int(sample_rate * 0.05))

    for i in range(n_samples):
        t = i / sample_rate

        # Frecuencia variable si hay sweep
        if frequency_end:
            f = frequency + (frequency_end - frequency) * (i / n_samples)
        else:
            f = frequency

        value = math.sin(2 * math.pi * f * t)

        # Fadeout suave
        if i > n_samples - fade_samples:
            value *= (n_samples - i) / fade_samples

        samples.append(int(value * volume * 32767))

    sound_bytes = struct.pack(f'<{n_samples}h', *samples)
    return pygame.mixer.Sound(buffer=sound_bytes)


def generate_noise_burst(duration, volume=0.2):
    """
    Genera un estallido de ruido blanco.
    """
    sample_rate = 22050
    n_samples = int(sample_rate * duration / 1000)

    samples = []

    # Fadeout
    fade_samples = max(1, int(sample_rate * 0.03))

    for i in range(n_samples):
        value = (import_random() * 2 - 1)

        # Fadeout
        if i > n_samples - fade_samples:
            value *= (n_samples - i) / fade_samples

        samples.append(int(value * volume * 32767))

    sound_bytes = struct.pack(f'<{n_samples}h', *samples)
    return pygame.mixer.Sound(buffer=sound_bytes)


def import_random():
    """Wrapper para random para uso interno."""
    import random
    return random.random()


def generate_sweep(start_freq, end_freq, duration, volume=0.3):
    """
    Genera un sweep de frecuencia (para power-ups).
    """
    return generate_tone(start_freq, duration, volume, end_freq)


def generate_arpeggio(frequencies, note_duration, volume=0.3):
    """
    Genera un arpegio de notas.
    """
    sample_rate = 22050
    note_samples = int(sample_rate * note_duration / 1000)

    all_samples = []

    for freq in frequencies:
        for i in range(note_samples):
            t = i / sample_rate
            value = math.sin(2 * math.pi * freq * t)

            # Envolvente de nota
            attack = int(note_samples * 0.05)
            release = int(note_samples * 0.3)

            if i < attack:
                value *= i / attack
            elif i > note_samples - release:
                value *= (note_samples - i) / release

            all_samples.append(int(value * volume * 32767))

    sound_bytes = struct.pack(f'<{len(all_samples)}h', *all_samples)
    return pygame.mixer.Sound(buffer=sound_bytes)


class SoundManager:
    """
    Gestor centralizado de sonidos del juego.
    Genera y reproduce todos los efectos de sonido sintéticos.
    """

    def __init__(self, enabled=True):
        self.enabled = enabled
        self.volume = 0.7

        # Diccionario de sonidos
        self.sounds = {}

        # Generar todos los sonidos
        self._generate_sounds()

    def _generate_sounds(self):
        """Genera todos los efectos de sonido sintéticos."""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        except pygame.error:
            pass

        # Sonido al rebotar la pelota en la paleta (440 Hz, 80ms)
        self.sounds['paddle_hit'] = generate_tone(440, 80, volume=0.25)

        # Sonido al rebotar en un ladrillo (523 Hz, 60ms)
        self.sounds['brick_hit'] = generate_tone(523, 60, volume=0.2)

        # Sonido al destruir un ladrillo (ruido)
        self.sounds['brick_destroy'] = generate_noise_burst(100, volume=0.25)

        # Sonido de power-up (sweep 200->800 Hz)
        self.sounds['power_up'] = generate_sweep(200, 800, 200, volume=0.3)

        # Sonido al perder una vida (sweep descendente)
        self.sounds['life_lost'] = generate_sweep(300, 80, 400, volume=0.4)

        # Sonido de game over
        self.sounds['game_over'] = generate_sweep(400, 80, 600, volume=0.4)

        # Sonido de victoria (arpegio C-E-G-C)
        victory_notes = [523, 659, 784, 1047]
        self.sounds['victory'] = generate_arpeggio(victory_notes, 150, volume=0.3)

        # Sonido de láser (880 Hz, 50ms)
        self.sounds['laser'] = generate_tone(880, 50, volume=0.15)

        # Sonido de nivel completado
        level_notes = [392, 440, 494, 523, 587, 659, 784]
        self.sounds['level_complete'] = generate_arpeggio(level_notes, 100, volume=0.25)

        # Sonido de bola multibalón
        self.sounds['multi_ball'] = generate_sweep(300, 600, 150, volume=0.25)

    def play(self, sound_name):
        """Reproduce un sonido por nombre."""
        if not self.enabled:
            return

        if sound_name in self.sounds:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(self.volume)
                sound.play()
            except Exception:
                pass

    def set_volume(self, volume):
        """Ajusta el volumen general (0.0 a 1.0)."""
        self.volume = max(0.0, min(1.0, volume))

    def mute(self):
        """Silencia todos los sonidos."""
        self.enabled = False

    def unmute(self):
        """Activa los sonidos."""
        self.enabled = True

    def toggle(self):
        """Alterna entre silencio y sonido."""
        self.enabled = not self.enabled
        return self.enabled


# Instancia global del gestor de sonidos
_sound_manager = None


def get_sound_manager():
    """Obtiene o crea la instancia global del gestor de sonidos."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
