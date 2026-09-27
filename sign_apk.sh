#!/usr/bin/env bash
#
# sign_apk.sh — Genera un APK de release FIRMADO listo para instalar o compartir.
#
# Uso:
#   ./sign_apk.sh
#
# El script:
#   1) Crea un keystore si no existe (te pide una contraseña).
#   2) Compila el APK de release con buildozer (sin firmar).
#   3) Alinea y firma el APK con apksigner usando el keystore.
#   4) Deja el resultado en bin/ y te indica el comando para instalarlo.
#
# IMPORTANTE: ejecútalo en TU terminal (no en una terminal gestionada por una
# herramienta), para que puedas teclear la contraseña. Guarda el keystore y su
# contraseña en lugar seguro: si los pierdes, no podrás publicar actualizaciones
# de la app con la misma identidad. Nunca subas el keystore ni las contraseñas
# al repositorio (ya están en .gitignore).
#
# Contraseñas:
#   Por defecto se piden por teclado (sin mostrarlas). También puedes definirlas
#   antes de ejecutar, para uso no interactivo:
#       export ARK_KEYSTORE_PASS='...'      # contraseña del keystore
#       export ARK_KEY_PASS='...'           # contraseña de la clave (si es distinta)
#   El script NUNCA escribe las contraseñas en disco ni en el historial.

set -euo pipefail

# --- Rutas ---------------------------------------------------------------
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEYSTORE_DIR="${PROJECT_DIR}/keystore"
KEYSTORE="${KEYSTORE_DIR}/arkanoid-release.jks"
KEY_ALIAS="arkanoid"
APK_UNSIGNED="${PROJECT_DIR}/bin/arkanoid-1.0.0-arm64-v8a-release-unsigned.apk"
APK_SIGNED="${PROJECT_DIR}/bin/arkanoid-1.0.0-arm64-v8a-release-signed.apk"

# Android SDK de buildozer (apunta al que ya usa el proyecto)
SDK_HOME="${ANDROID_HOME:-$HOME/.buildozer/android/platform/android-sdk}"
BUILD_TOOLS="$(ls -d "${SDK_HOME}"/build-tools/* 2>/dev/null | sort -V | tail -1 || true)"
APKSIGNER="${BUILD_TOOLS}/apksigner"
ZIPALIGN="${BUILD_TOOLS}/zipalign"
KEYTOOL="$(command -v keytool || echo /usr/bin/keytool)"
APK_ALIGNED="${PROJECT_DIR}/bin/arkanoid-1.0.0-arm64-v8a-release-aligned.apk"

die() { echo "ERROR: $*" >&2; exit 1; }

[ -x "${APKSIGNER}" ] || die "No encuentro apksigner en ${BUILD_TOOLS}. ¿Está instalado el Android SDK?"
[ -x "${ZIPALIGN}" ] || die "No encuentro zipalign en ${BUILD_TOOLS}."
[ -x "${KEYTOOL}" ]  || die "No encuentro keytool."

# --- Contraseñas ---------------------------------------------------------
# Se leen por stdin (read -s), NO con Console.readPassword() de Java, que en
# algunas terminales se cuelga porque intenta leer de /dev/tty.
_ask_pass() {
    # $1 = variable destino, $2 = texto del prompt
    local __var="$1" __prompt="$2" __val=""
    read -r -s -p "${__prompt}" __val
    echo "" >&2
    printf -v "${__var}" '%s' "${__val}"
}

# Contraseña del keystore
if [ -n "${ARK_KEYSTORE_PASS:-}" ]; then
    STORE_PASS="${ARK_KEYSTORE_PASS}"
else
    _ask_pass STORE_PASS "Contraseña del keystore: "
fi
[ -n "${STORE_PASS}" ] || die "La contraseña del keystore no puede estar vacía."

# Contraseña de la clave (por defecto, la misma que la del keystore)
if [ -n "${ARK_KEY_PASS:-}" ]; then
    KEY_PASS="${ARK_KEY_PASS}"
else
    KEY_PASS="${STORE_PASS}"
fi

# Exporta las contraseñas como variables de entorno con nombres internos para
# pasarlas a keytool/apksigner mediante ':env' (nunca por la línea de comandos,
# que quedaría visible en el listado de procesos).
export ARK_KS_PASS_ENV="${STORE_PASS}"
export ARK_KEY_PASS_ENV="${KEY_PASS}"

# --- 1) Keystore ---------------------------------------------------------
mkdir -p "${KEYSTORE_DIR}"

if [ ! -f "${KEYSTORE}" ]; then
    echo "==> No existe keystore; se creará en: ${KEYSTORE}"
    "${KEYTOOL}" -genkeypair \
        -v \
        -keystore "${KEYSTORE}" \
        -alias "${KEY_ALIAS}" \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000 \
        -dname "CN=Arkanoid Neon Breakout, OU=Games, O=Arkanoid, L=, S=, C=ES" \
        -storepass:env ARK_KS_PASS_ENV \
        -keypass:env ARK_KEY_PASS_ENV
    echo "==> Keystore creado. ¡Haz una copia de seguridad de ${KEYSTORE}!"
else
    echo "==> Usando keystore existente: ${KEYSTORE}"
fi

# --- 2) Compilar el APK de release (sin firmar) --------------------------
echo "==> Compilando el APK de release con buildozer..."
cd "${PROJECT_DIR}"
# Activar el venv de buildozer si no lo está ya
if [ -z "${VIRTUAL_ENV:-}" ] && [ -x "${PROJECT_DIR}/.venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "${PROJECT_DIR}/.venv/bin/activate"
fi
# PERL5LIB para los módulos Perl instalados a nivel de usuario (Fedora)
export PERL5LIB="${PERL5LIB:-$HOME/.local/share/perl5:$HOME/.local/lib64/perl5}"

buildozer android release

[ -f "${APK_UNSIGNED}" ] || die "No se generó ${APK_UNSIGNED}. Revisa la salida de buildozer."

# --- 3) Alinear y firmar -------------------------------------------------
echo "==> Alineando el APK (zipalign)..."
rm -f "${APK_ALIGNED}" "${APK_SIGNED}"
"${ZIPALIGN}" -f -p 4 "${APK_UNSIGNED}" "${APK_ALIGNED}"

echo "==> Firmando el APK..."
"${APKSIGNER}" sign \
    --ks "${KEYSTORE}" \
    --ks-key-alias "${KEY_ALIAS}" \
    --ks-pass env:ARK_KS_PASS_ENV \
    --key-pass env:ARK_KEY_PASS_ENV \
    --out "${APK_SIGNED}" \
    "${APK_ALIGNED}"

echo "==> Verificando la firma..."
"${APKSIGNER}" verify --verbose "${APK_SIGNED}" | head -5

# --- 4) Resultado --------------------------------------------------------
echo ""
echo "==> APK firmado listo: ${APK_SIGNED}"
echo ""
echo "Para instalarlo en el móvil conectado:"
echo "  ${SDK_HOME}/platform-tools/adb install -r \"${APK_SIGNED}\""
