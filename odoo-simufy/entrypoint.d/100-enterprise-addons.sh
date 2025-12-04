#!/bin/bash

set -e

# ===== Configuración =====
REPO_URL="git@github.com:odoo/enterprise.git"
BRANCH="17.0"          # <-- pon aquí la rama donde está el commit
COMMIT="0a6bc37"       # commit deseado (abreviado o completo)
DEST_DIR="/opt/odoo/enterprise_addons"
CONFIG_FILE="/etc/ssh/ssh_config.d/github.conf"
PRIVATE_KEY="/opt/odoo/certificates/github_rsa"
SSH_ODDO="/opt/odoo/.ssh"

sudo chmod 600 $PRIVATE_KEY
sudo chown odoo:odoo $PRIVATE_KEY

# ===== Función: clonar, hacer checkout y dejar solo working tree + .revision =====
clone_and_checkout() {
    echo "Descargando repo y dejando solo el working tree en $DEST_DIR..."

    # Aseguramos que exista el directorio destino (puede ser un volumen montado)
    sudo mkdir -p "$DEST_DIR"

    # Vaciar el contenido del directorio, pero sin borrar el propio mount point
    # Incluye archivos ocultos (menos . y ..)
    sudo rm -rf "$DEST_DIR"/* "$DEST_DIR"/.[!.]* "$DEST_DIR"/..?* 2>/dev/null || true

    sudo chown -R odoo:odoo "$DEST_DIR"

    # Partial clone (historial pero sin blobs antiguos)
    echo "Clonando con partial clone (--filter=blob:none, rama $BRANCH)..."
    sudo -u odoo git clone --filter=blob:none --branch "$BRANCH" "$REPO_URL" "$DEST_DIR"

    cd "$DEST_DIR"

    echo "Haciendo checkout al commit $COMMIT..."
    sudo -u odoo git checkout "$COMMIT"

    FULL_COMMIT=$(git rev-parse HEAD)
    echo "Commit real tras checkout: $FULL_COMMIT"

    # Verificar que FULL_COMMIT coincide con COMMIT (soportando abreviado)
    if [ ${#COMMIT} -lt 40 ]; then
        case "$FULL_COMMIT" in
            "$COMMIT"*)
                echo "OK: el commit actual ($FULL_COMMIT) coincide con el prefijo esperado ($COMMIT)."
                ;;
            *)
                echo "ERROR: el commit actual ($FULL_COMMIT) no coincide con el esperado ($COMMIT)." >&2
                exit 1
                ;;
        esac
    else
        if [ "$FULL_COMMIT" != "$COMMIT" ]; then
            echo "ERROR: el commit actual ($FULL_COMMIT) no coincide con el esperado ($COMMIT)." >&2
            exit 1
        fi
    fi

    # Guardar el commit completo en .revision
    echo "$FULL_COMMIT" | sudo tee "$DEST_DIR/.revision" >/dev/null
    sudo chown odoo:odoo "$DEST_DIR/.revision"

    # Eliminar .git para ahorrar espacio
    echo "Eliminando .git para reducir espacio..."
    sudo rm -rf "$DEST_DIR/.git"

    echo "Repositorio preparado en $DEST_DIR con commit $FULL_COMMIT y sin .git"
    cd - > /dev/null
}

# ===== Configuración SSH =====

sudo mkdir -p "$(dirname "$CONFIG_FILE")"
sudo tee "$CONFIG_FILE" > /dev/null <<EOF
Host github.com
    IdentityFile $PRIVATE_KEY
    StrictHostKeyChecking yes
EOF

mkdir -p "$SSH_ODDO"
sudo mkdir -p /root/.ssh
sudo chown -R odoo:odoo "$SSH_ODDO"

ssh-keyscan -t rsa github.com >> "$SSH_ODDO/known_hosts" 2>/dev/null || true
sudo sh -c 'ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts' 2>/dev/null || true

sudo mkdir -p "$DEST_DIR"
sudo chown -R odoo:odoo "$DEST_DIR"
sudo git config --global --add safe.directory "$DEST_DIR" || true

# ===== Lógica principal =====

# Si existe .revision, comprobamos si el commit guardado es el que queremos
if [ -f "$DEST_DIR/.revision" ]; then
    SAVED_COMMIT=$(cat "$DEST_DIR/.revision")
    echo "Encontrado .revision con commit $SAVED_COMMIT. Comparando con el deseado ($COMMIT)..."

    MATCH=0
    if [ ${#COMMIT} -lt 40 ]; then
        case "$SAVED_COMMIT" in
            "$COMMIT"*)
                MATCH=1
                ;;
        esac
    else
        if [ "$SAVED_COMMIT" = "$COMMIT" ]; then
            MATCH=1
        fi
    fi

    if [ "$MATCH" -eq 1 ]; then
        echo "El commit guardado ($SAVED_COMMIT) coincide con el deseado ($COMMIT). No es necesario descargar nada."
    else
        echo "El commit guardado ($SAVED_COMMIT) NO coincide con el deseado ($COMMIT). Re-descargando el repositorio..."
        clone_and_checkout
    fi
else 

    # Si no hay .revision, es la primera vez o el directorio está vacío → descargar
    echo "No hay commit previo guardado (.revision). Descargando repositorio por primera vez..."
    clone_and_checkout

fi 
