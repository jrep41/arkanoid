"""
Receta local de python-for-android (p4a) para pygame-ce.

python-for-android solo trae una receta "pygame" fijada a la 2.1.0, que no
compila con CPython >= 3.12 (usa cabeceras eliminadas como longintrepr.h).
Esta receta construye pygame-ce —el fork mantenido que usa este proyecto en
escritorio (requirements.txt)— a partir del código fuente de GitHub.

Detalles del build (más información en ANDROID.md):
- Se usa el archivo fuente de GitHub y no el sdist de PyPI para que Cython
  regenere el código C contra las cabeceras de CPython del dispositivo.
- setup.py decide si inyectar "-mavx2" consultando platform.machine(), que en
  una compilación cruzada devuelve la máquina host (x86_64). El compilador del
  NDK rechaza ese flag al targetear ARM, así que aquí se parchea la condición.
- El template Android de pygame-ce 2.5.8 ya incluye los fuentes SIMD de los
  blitters (simd_blitters_sse2.c / simd_blitters_avx2.c), necesarios para que
  surface.so cargue en el dispositivo.
"""

from os import remove, rename
from os.path import exists, join

from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.toolchain import current_directory


class PygameCERecipe(CompiledComponentsPythonRecipe):
    """Compila pygame-ce (SDL2) para Android."""

    version = "2.5.8"
    url = "https://github.com/pygame-community/pygame-ce/archive/{version}.tar.gz"

    # El paquete resultante se importa como "pygame"
    site_packages_name = "pygame"
    name = "pygame-ce"

    depends = [
        "sdl2",
        "sdl2_image",
        "sdl2_mixer",
        "sdl2_ttf",
        "setuptools",
        "jpeg",
        "png",
    ]
    call_hostpython_via_targetpython = False  # Due to setuptools
    install_in_hostpython = False

    # setup.py compila los .pyx con Cython en el host antes de empaquetar
    hostpython_prerequisites = ["setuptools", "cython"]

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            self._patch_avx2_flag()
            self._write_android_setup(arch)
            self._drop_pyproject()

    def _drop_pyproject(self):
        """
        Elimina pyproject.toml para que pip/setuptools usen setup.py.

        pygame-ce declara ``build-backend = 'mesonpy'``. Con pyproject.toml
        presente, ``pip install .`` lanza un build NATIVO con Meson (recompila
        para la máquina host x86_64 y ejecuta un binario de prueba ARM que no
        puede correr), e incluso dejando un ``[project]`` mínimo setuptools
        intenta aplicarlo y falla (``AttributeError: 'NoneType' object has no
        attribute 'get'``). Retirando el archivo, pip recurre al flujo
        setuptools/setup.py y reutiliza el cross-compile ya hecho.

        setup.py obtiene la versión vía ``buildconfig/get_version.py``, que lee
        de pyproject.toml; por eso primero se parchea ese módulo para que use
        la versión fija de la receta cuando el archivo no exista.
        """
        self._patch_get_version()
        pyproject = "pyproject.toml"
        backup = pyproject + ".android-original"
        legacy_backup = pyproject + ".android-disabled"
        # Recupera el original si una ejecución previa ya lo había movido.
        if not exists(backup) and exists(legacy_backup):
            rename(legacy_backup, backup)
        # Deja el directorio sin pyproject.toml, conservando el original aparte.
        if exists(pyproject):
            if exists(backup):
                remove(pyproject)
            else:
                rename(pyproject, backup)

    def _patch_get_version(self):
        """Hace que get_version.py use la versión fija si no hay pyproject.toml."""
        path = join("buildconfig", "get_version.py")
        with open(path, encoding="utf-8") as handle:
            src = handle.read()
        # Idempotente: si ya está parcheado (marcador presente), no repetir.
        marker = "if config_file.exists():"
        needle = "config_text = config_file.read_text()"
        if marker in src or needle not in src:
            return
        replacement = (
            "if config_file.exists():\n"
            "    config_text = config_file.read_text()\n"
            "else:\n"
            f"    config_text = '[project]\\nversion = \"{self.version}\"\\n'"
        )
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(src.replace(needle, replacement, 1))

    def _patch_avx2_flag(self):
        """
        Desactiva la inyección de "-mavx2" al compilar para Android.

        setup.py solo debe usar AVX2 cuando compila para una CPU x86; al cruzar
        a ARM detecta la máquina host y añade el flag, que el clang del NDK
        rechaza ("unsupported option '-mavx2' for target 'aarch64-linux-android'").
        """
        setup_path = "setup.py"
        with open(setup_path, encoding="utf-8") as handle:
            setup_src = handle.read()
        needle = 'machine_name.startswith(("x86", "i686"))'
        patch = (
            '("PYGAME_ANDROID" not in os.environ) '
            'and machine_name.startswith(("x86", "i686"))'
        )
        if needle in setup_src and patch not in setup_src:
            with open(setup_path, "w", encoding="utf-8") as handle:
                handle.write(setup_src.replace(needle, patch, 1))

    def _write_android_setup(self, arch):
        """Genera el archivo Setup de distutils a partir del template de Android."""
        setup_template = open(
            join("buildconfig", "Setup.Android.SDL2.in"), encoding="utf-8"
        ).read()
        env = self.get_recipe_env(arch)
        env["ANDROID_ROOT"] = join(self.ctx.ndk.sysroot, "usr")

        png = self.get_recipe("png", self.ctx)
        png_lib_dir = join(png.get_build_dir(arch.arch), ".libs")
        png_inc_dir = png.get_build_dir(arch)

        jpeg = self.get_recipe("jpeg", self.ctx)
        jpeg_inc_dir = jpeg_lib_dir = jpeg.get_build_dir(arch.arch)

        sdl_mixer_includes = ""
        sdl2_mixer_recipe = self.get_recipe("sdl2_mixer", self.ctx)
        for include_dir in sdl2_mixer_recipe.get_include_dirs(arch):
            sdl_mixer_includes += f"-I{include_dir} "

        setup_file = setup_template.format(
            sdl_includes=(
                " -I"
                + join(self.ctx.bootstrap.build_dir, "jni", "SDL", "include")
                + " -L"
                + join(self.ctx.bootstrap.build_dir, "libs", str(arch))
                + " -L"
                + png_lib_dir
                + " -L"
                + jpeg_lib_dir
                + " -L"
                + arch.ndk_lib_dir_versioned
            ),
            sdl_ttf_includes="-I"
            + join(self.ctx.bootstrap.build_dir, "jni", "SDL2_ttf"),
            sdl_image_includes="-I"
            + join(self.ctx.bootstrap.build_dir, "jni", "SDL2_image", "include"),
            sdl_mixer_includes=sdl_mixer_includes,
            jpeg_includes="-I" + jpeg_inc_dir,
            png_includes="-I" + png_inc_dir,
            freetype_includes="",
        )
        with open("Setup", "w", encoding="utf-8") as handle:
            handle.write(setup_file)

    def build_arch(self, arch):
        # Cython y setuptools deben estar en el hostpython antes de compilar
        self.install_hostpython_prerequisites()
        super().build_arch(arch)

    def install_python_package(self, arch, name=None, env=None, is_dir=True):
        """
        Instala reutilizando el entorno del hostpython (--no-build-isolation).

        Aun sin pyproject.toml, pip 25.x usa el flujo PEP 517 con aislación de
        build: crea un entorno aislado con setuptools pero SIN cython, y
        setup.py aborta con "You need cython". Con --no-build-isolation pip
        usa el entorno del hostpython, donde la receta ya instaló setuptools y
        cython. Se pasa el flag solo aquí (no en setup_extra_args) para no
        romper ``setup.py build_ext``, que no reconoce esa opción.
        """
        self.setup_extra_args = ["--no-build-isolation"]
        super().install_python_package(arch, name=name, env=env, is_dir=is_dir)

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)
        env["USE_SDL2"] = "1"
        env["PYGAME_CROSS_COMPILE"] = "TRUE"
        env["PYGAME_ANDROID"] = "TRUE"
        # El hostpython (CPython 3.14) hereda ~/.local/lib/python3.14/site-packages,
        # donde puede residir un Cython antiguo (p. ej. 0.29.37 instalado a nivel
        # usuario) que eclipsa al Cython 3.x instalado en el propio hostpython.
        # Ese Cython viejo genera C contra API privada eliminada en 3.14
        # (_PyDict_SetItem_KnownHash) y la compilación falla. Excluir el site de
        # usuario garantiza que se use el Cython correcto del hostpython.
        env["PYTHONNOUSERSITE"] = "1"
        return env


recipe = PygameCERecipe()
