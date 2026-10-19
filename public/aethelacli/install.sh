#!/usr/bin/env bash
# aethelcli installer — curl -fsSL https://darkie.dpdns.org/aethelacli/install | bash
set -euo pipefail

REPO="https://github.com/aethelreborn/aethelcli.git"
INSTALL_DIR="${HOME}/.aethelcli"
BIN_DIR="${HOME}/.local/bin"
PYTHON="${PYTHON:-python3}"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

banner() {
    cat << 'EOF'
    ___         __  __         __     ___   ____
   /   |  ___  / /_/ /_  ___  / /    /   | /  _/
  / /| | / _ \/ __/ __ \/ _ \/ /    / /| | / /  
 / ___ |/  __/ /_/ / / /  __/ /    / ___ |_/ /   
/_/  |_|\___/\__/_/ /_/\___/_/    /_/  |_/___/   
                                                 
          aethelcli · darkie.dpdns.org
EOF
}

info()  { echo -e "${CYAN}[*]${NC} $1"; }
ok()    { echo -e "${GREEN}[+]${NC} $1"; }
fail()  { echo -e "${RED}[-]${NC} $1"; exit 1; }

banner
echo
info "installing aethelcli → ${INSTALL_DIR}"

command -v "$PYTHON" >/dev/null || fail "python3 not found"
command -v git >/dev/null || fail "git not found"

mkdir -p "$INSTALL_DIR" "$BIN_DIR"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

info "cloning source"
git clone --depth 1 "$REPO" "$TMP/src" || fail "clone failed"

rm -rf "$INSTALL_DIR/aethelcli"
cp -r "$TMP/src/aethelcli" "$INSTALL_DIR/"
cp "$TMP/src/requirements.txt" "$INSTALL_DIR/" 2>/dev/null || true

info "creating virtualenv"
"$PYTHON" -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"
pip install --upgrade pip -q
pip install -r "$INSTALL_DIR/requirements.txt" -q || pip install rich requests customtkinter pillow psutil -q

cat > "$BIN_DIR/aethelcli" << EOF
#!/usr/bin/env bash
source "${INSTALL_DIR}/venv/bin/activate"
export PYTHONPATH="${INSTALL_DIR}:\${PYTHONPATH:-}"
exec python -m aethelcli "\$@"
EOF
chmod +x "$BIN_DIR/aethelcli"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
    export PATH="$BIN_DIR:$PATH"
fi

info "sending install telemetry"
PYTHONPATH="$INSTALL_DIR" python - << 'PY' || true
import sys, os
sys.path.insert(0, os.path.expanduser("~/.aethelcli"))
try:
    from aethelcli.webhook import report_install
    report_install()
except Exception as e:
    print(f"[!] webhook skipped: {e}")
PY

ok "installed"
echo
echo -e "  run:  ${GREEN}aethelcli${NC}"
echo -e "  gui:  ${GREEN}aethelcli --gui${NC}"
echo
exec "$BIN_DIR/aethelcli"
