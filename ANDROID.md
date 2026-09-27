# Arkanoid en Android (APK)

Este documento explica cómo generar el APK de `main.py` y cómo está resuelta la
entrada táctil. La versión de escritorio sigue funcionando igual que siempre.

## Resumen técnico

| Aspecto | Decisión |
|---|---|
| Empaquetado | [Buildozer](https://buildozer.readthedocs.io/) + [python-for-android](https://python-for-android.readthedocs.io/) (bootstrap `sdl2`) |
| Motor gráfico | `pygame-ce` 2.5.8 (receta local en `p4a-recipes/pygame-ce/`) |
| Entrada táctil | Eventos `pygame.FINGERDOWN` / `FINGERMOTION` / `FINGERUP` |
| Ratón emulado | Los `MOUSE*` generados por toques se descartan (`event.touch == True`) |
| Orientación | Horizontal (`orientation = landscape`) |

## Controles táctiles

| Gesto | Acción | Equivalente en escritorio |
|---|---|---|
| Arrastrar el dedo por el área de juego | Mover la paleta | Ratón / flechas |
| Mantener el dedo pulsado | Disparo continuo de láser | Mantener el clic |
| Toque rápido (tap) | Empezar, lanzar la pelota, disparar o continuar | Clic / Espacio |
| Botón `♪ SONIDO` | Activar / silenciar | Tecla `N` |
| Botón `+ BOLA EXTRA` | Añadir pelota (máx. 5) | Tecla `B` |
| Botón `II PAUSA` | Pausar / seguir | Tecla `P` |

Multitáctil: un dedo mueve la paleta mientras otro mantiene el fuego.

## Cómo funciona la entrada táctil en SDL2

En SDL2 para Android los toques directos llegan como eventos
`pygame.FINGERDOWN`, `pygame.FINGERMOTION` y `pygame.FINGERUP`. Sus atributos
`x` e `y` vienen **normalizados en el rango 0.0..1.0 sobre la superficie
lógica** (la que crea `pygame.display.set_mode(..., pygame.SCALED)` con
`SCREEN_WIDTH x SCREEN_HEIGHT`), de modo que se convierten a píxeles lógicos
multiplicando por esas dimensiones (ver `Game.finger_to_screen`).

Además, SDL2 **emula automáticamente** eventos de ratón (`MOUSEBUTTONDOWN`,
`MOUSEMOTION`, `MOUSEBUTTONUP`) a partir de los toques simples. Esos eventos
llevan el atributo `touch = True` y se descartan en `Game.handle_events` para
que cada acción no se ejecute dos veces. El ratón real (`touch = False`)
sigue funcionando en escritorio.

> Nota: con `pygame.SCALED`, los eventos de ratón ya llegan convertidos a
> coordenadas lógicas por el propio SDL2; los `FINGER*` se escalan a mano.

## Generar el APK

### Requisitos (una sola vez)

- Linux con JDK 17+ (`java -version`), `git`, `ccache`, `autoconf`, `automake`,
  `libtool`, `pkg-config`, `zlib1g-dev`, `libssl-dev`, `libffi-dev`.
- Buildozer: `pip install buildozer` (o `pipx install buildozer`).
- En Fedora: `sudo dnf install java-17-openjdk-devel git ccache autoconf automake libtool pkgconf-pkg-config zlib-devel openssl-devel libffi-devel`.
- **CMake** (lo necesita la receta `jpeg`): `pip install cmake` dentro del venv.
- **Módulos Perl de Fedora** (los necesita `perl Configure` de la receta
  `openssl`): Fedora instala `perl-interpreter` sin el meta `perl`, así que los
  módulos del núcleo van en paquetes sueltos. Sin root se instalan en
  `~/.local/{share,lib64}/perl5` extrayendo los RPM con
  `dnf download <pkg>` + `rpm2cpio <pkg>.rpm | cpio -idmu`. Paquetes
  necesarios: `perl-FindBin`, `perl-IPC-Cmd`, `perl-Params-Check`,
  `perl-Module-Load-Conditional`, `perl-ExtUtils-MakeMaker`,
  `perl-ExtUtils-MM-Utils`, `perl-Test-Harness`, `perl-Benchmark`,
  `perl-version`, `perl-Digest-SHA`, `perl-Locale-Maketext`.
- El primer build descarga Android SDK/NDK (~2-4 GB) y compila CPython, SDL2 y
  pygame-ce: puede tardar 20-60 minutos. Los siguientes son incrementales.

### Compilar

```bash
cd /home/jose/Documentos/arkapp1

# Activar el entorno virtual (buildozer lo detecta por VIRTUAL_ENV).
# Debe contener buildozer y cmake: pip install cmake
source .venv/bin/activate

# PERL5LIB apunta a los módulos Perl instalados a nivel de usuario (Fedora)
export PERL5LIB="$HOME/.local/share/perl5:$HOME/.local/lib64/perl5"

# Generar el APK de depuración
buildozer android debug
```

El APK queda en `bin/`, por ejemplo `bin/arkanoid-1.0.0-arm64-v8a-debug.apk`
(~17 MB, solo `arm64-v8a`). Contiene las librerías nativas
(`libpython3.14.so`, `libSDL2*.so`) y el código del juego empaquetado en
`assets/private.tar` (`main.pyc`, `sounds.pyc`, `high_score.txt`).

### Instalar en un dispositivo (USB con depuración activada)

```bash
buildozer android debug deploy run logcat
# o manualmente:
adb install -r bin/arkanoid-*-arm64-v8a-debug.apk
adb shell am start -n org.arkanoid.arkanoid/org.kivy.android.PythonActivity
adb logcat -s python:*        # ver los prints/errores del juego
```

### APK de publicación (firmado)

`buildozer android release` genera por defecto un **AAB** (App Bundle), que
**no se instala en un móvil** (solo sirve para subir a Google Play). Para que
genere un APK instalable, en `buildozer.spec` está puesto:

```ini
android.release_artifact = apk
```

La vía recomendada es el script incluido, que crea el keystore (si no existe),
compila, alinea (`zipalign`) y firma (`apksigner`) el APK:

```bash
./sign_apk.sh
```

Te pedirá la **contraseña del keystore** de forma interactiva; no la escribas en
ningún archivo ni la subas al repositorio. El resultado queda en
`bin/arkanoid-1.0.0-arm64-v8a-release-signed.apk`.

> ⚠️ Guarda el keystore (`keystore/arkanoid-release.jks`) y su contraseña en un
> lugar seguro: si los pierdes, no podrás publicar actualizaciones de la app con
> la misma identidad. Ya están protegidos por `.gitignore`.

#### Alternativa manual (equivalente a lo que hace el script)

```bash
buildozer android release
SDK=$HOME/.buildozer/android/platform/android-sdk
BT=$(ls -d $SDK/build-tools/* | sort -V | tail -1)
"$BT/zipalign" -f -p 4 bin/arkanoid-*-release-unsigned.apk bin/aligned.apk
"$BT/apksigner" sign --ks keystore/arkanoid-release.jks --ks-key-alias arkanoid \
    --out bin/arkanoid-1.0.0-arm64-v8a-release-signed.apk bin/aligned.apk
"$BT/apksigner" verify --verbose bin/arkanoid-1.0.0-arm64-v8a-release-signed.apk
```

#### Firma automática dentro de buildozer (opcional)

Si prefieres que buildozer firme durante el build, define las cuatro variables
`P4A_RELEASE_*` (Gradle las lee del entorno) **en tu sesión de terminal**, nunca
en el repositorio:

```bash
export P4A_RELEASE_KEYSTORE="$PWD/keystore/arkanoid-release.jks"
export P4A_RELEASE_KEYALIAS="arkanoid"
export P4A_RELEASE_KEYSTORE_PASSWD='<tu contraseña>'    # escríbela tú
export P4A_RELEASE_KEYALIAS_PASSWD='<tu contraseña>'
buildozer android release        # genera el APK ya firmado
```

## Por qué una receta local de pygame-ce

python-for-android solo incluye la receta `pygame` fijada a la **2.1.0**, que
no compila con CPython >= 3.12 (usa `longintrepr.h`, eliminada de las cabeceras
públicas). La receta local `p4a-recipes/pygame-ce/__init__.py` construye
**pygame-ce 2.5.8** (el mismo que `requirements.txt` en escritorio) e incluye
los ajustes de compilación cruzada necesarios:

1. **`-mavx2`**: el `setup.py` de pygame-ce decide si inyecta esa flag consultando
   `platform.machine()`, que en compilación cruzada devuelve la máquina host
   (x86_64). El clang del NDK la rechaza al targetear ARM, así que la receta
   parchea esa condición.
2. **Cython**: los `.pyx` de pygame-ce se generan en el host
   (`hostpython_prerequisites = ["setuptools", "cython"]`).
3. **`PYTHONNOUSERSITE=1`**: el hostpython (CPython 3.14) hereda
   `~/.local/lib/python3.14/site-packages`; un Cython antiguo instalado a nivel
   de usuario eclipsa al Cython 3.x del hostpython y genera C contra API privada
   eliminada en 3.14 (`_PyDict_SetItem_KnownHash`). Excluir el site de usuario
   garantiza que se use el Cython correcto.
4. **`pyproject.toml` desactivado**: pygame-ce declara
   `build-backend = 'mesonpy'`. Con ese archivo presente, `pip install .` lanza
   un build **nativo** con Meson (recompila para x86_64 y ejecuta un binario de
   prueba ARM que no puede correr). La receta lo elimina en `prebuild_arch`
   (parcheando antes `buildconfig/get_version.py`, que lo usa para la versión)
   para que pip use `setup.py`.
5. **`--no-build-isolation`**: pip 25.x aplica aislación de build (PEP 517) con
   un entorno vacío, sin Cython, y `setup.py` aborta. La receta pasa ese flag
   **solo** a la instalación final.

El template Android de pygame-ce 2.5.8 (`buildconfig/Setup.Android.SDL2.in`) ya
incluye los fuentes SIMD de los blitters (`simd_blitters_sse2.c`,
`simd_blitters_avx2.c`), necesarios para que `surface.so` cargue en el
dispositivo (un build correcto no garantiza que el `.so` resuelva sus símbolos:
compruébalo siempre con `adb logcat`).

## Solución de problemas

| Síntoma | Causa / arreglo |
|---|---|
| `Can not perform a '--user' install` | Buildozer no detecta el venv: ejecuta `source .venv/bin/activate` antes. |
| `sh.CommandNotFound: cmake` | Falta CMake para la receta `jpeg`: `pip install cmake` en el venv activo. |
| `Can't locate FindBin.pm` (u otro módulo Perl) | Faltan módulos Perl del núcleo (receta `openssl`): instálalos en `~/.local/...` y exporta `PERL5LIB` (ver requisitos). |
| `longintrepr.h: No such file` | Estás usando la receta `pygame` de p4a en vez de la local `pygame-ce`. |
| `unsupported option '-mavx2'` | Falta el parche de `_patch_avx2_flag` en la receta. |
| `call to undeclared function '_PyDict_SetItem_KnownHash'` | Cython antiguo de `~/.local` eclipsa al del hostpython: asegura `PYTHONNOUSERSITE=1` y borra los `.c` con cabecera `Generated by Cython 0.29.37`. |
| `sanity check executable ... binary or interpreter not executable` | pip usó el backend meson por el `pyproject.toml`: la receta debe eliminarlo en `prebuild_arch`. |
| `You need cython` | pip usó aislación de build: la receta debe pasar `--no-build-isolation` a la instalación. |
| `option --no-build-isolation not recognized` | El flag se puso en `setup_extra_args` a nivel de clase y rompe `setup.py build_ext`; debe aplicarse solo a la instalación pip. |
| `dlopen failed ... surface.so` | Faltan los SIMD blitters en el template; usa pygame-ce >= 2.5. |
| El juego se ve en vertical | `orientation = landscape` en `buildozer.spec`; SDL puede reorientar tras `set_mode`. |
| Sin sonido | El juego degrada a modo silencio sin romperse (ver `sounds.py`). |
| Los toques hacen doble acción | No se están filtrando los `MOUSE*` emulados (`event.touch`). |

## Rendimiento en gama baja

El renderizado es software (CPU) y los blits con alfa son caros en ARM. Si el
juego va lento en un dispositivo modesto:

- Reduce el número de partículas (`add_particles`) y el tamaño de los halos.
- Evita velos translúcidos a pantalla completa por frame (el menú de pausa ya
  cachea su fondo).
- Mide en el dispositivo, no en el escritorio: los costes de blending son
  ~100x superiores en ARM sin SIMD.

## Pruebas

```bash
# Pruebas headless de la entrada táctil (sin pantalla ni audio)
SDL_VIDEODRIVER=offscreen SDL_AUDIODRIVER=dummy ARKANOID_TOUCH=1 \
    .venv/bin/python tests/test_touch_input.py
```

`ARKANOID_TOUCH=1` fuerza el modo táctil en escritorio para poder probar la
misma lógica que en Android.
