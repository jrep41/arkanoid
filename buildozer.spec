[app]

# (str) Title of your application
title = Arkanoid Neon Breakout

# (str) Package name
package.name = arkanoid

# (str) Package domain (needed for android/ios packaging)
package.domain = org.arkanoid

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,txt

# (list) List of directory to exclude (let empty to not exclude anything)
# Se excluye todo lo que no debe entrar en el APK: versiones alternativas del
# juego, entorno virtual, cachés y documentación.
source.exclude_dirs = .venv, .git, .idea, .vscode, .ruff_cache, __pycache__, tests, p4a-recipes, bin, .buildozer

# (list) List of exclusions using pattern matching
source.exclude_patterns = arkanoid.py, arkanoid_enhanced.py, opencode.json, *.md, *.log, *.png

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# pygame-ce se construye con la receta local de p4a-recipes/pygame-ce
# (la receta oficial de p4a es pygame 2.1.0 y no compila con CPython >= 3.12).
requirements = python3,pygame-ce

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/assets/icon.png

# (list) Supported orientations
# El juego está diseñado en horizontal (mueble arcade)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
# El juego es 100% local: no necesita ningún permiso
android.permissions =

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 27c

# (int) Android NDK API to use. This is the minimum API your app will support,
# it should usually match android.minapi.
android.ndk_api = 21

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_license = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# arm64-v8a cubre la inmensa mayoría de dispositivos actuales. Para publicar en
# Google Play añade también armeabi-v7a (APK más grande).
android.archs = arm64-v8a

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

# (str) The format used to package the app for release mode (apk or aar).
# aab (App Bundle) solo sirve para subir a Google Play y NO se puede instalar
# directamente en un móvil. Con apk, `buildozer android release` genera un APK
# instalable con adb (sin firmar; para publicar hay que firmarlo).
android.release_artifact = apk

#
# Python for android (p4a) specific
#

# (str) The directory in which python-for-android should look for your own
# build recipes (if any). Aquí vive la receta de pygame-ce.
p4a.local_recipes = ./p4a-recipes

# (str) Bootstrap to use for android builds (sdl2 es el correcto para pygame)
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
