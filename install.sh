#!/bin/bash
# Discord Archiver - Linux / macOS / Chromebook Setup

set -e

BOLD="\033[1m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
RESET="\033[0m"

echo ""
echo -e "${CYAN}+===============================================================================+${RESET}"
echo -e "${CYAN}|                  DISCORD ARCHIVER - SETUP                                    |${RESET}"
echo -e "${CYAN}+===============================================================================+${RESET}"
echo ""

# ── Detect Python ────────────────────────────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VERSION=$("$cmd" --version 2>&1 | awk '{print $2}')
        MAJOR=$(echo "$VERSION" | cut -d. -f1)
        MINOR=$(echo "$VERSION" | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${RED} [ERROR] Python 3.10 or newer is required but was not found.${RESET}"
    echo ""
    echo " To install Python:"
    echo ""
    if [ -f /etc/debian_version ]; then
        echo "   Debian / Ubuntu / Chromebook Linux:"
        echo "     sudo apt update && sudo apt install -y python3 python3-pip"
    elif [ "$(uname)" = "Darwin" ]; then
        echo "   macOS (Homebrew):"
        echo "     brew install python"
    else
        echo "   Visit: https://www.python.org/downloads/"
    fi
    echo ""
    exit 1
fi

echo -e "${GREEN} [OK] Found $($PYTHON --version)${RESET}"
echo ""

# ── Check / install pip ──────────────────────────────────────────────────────────
if ! $PYTHON -m pip --version &>/dev/null; then
    echo " pip not found — attempting to install..."
    if command -v apt &>/dev/null; then
        sudo apt install -y python3-pip
    else
        echo -e "${RED} [ERROR] pip is not installed. Please install it manually.${RESET}"
        exit 1
    fi
fi

# ── Upgrade pip quietly ──────────────────────────────────────────────────────────
$PYTHON -m pip install --upgrade pip --quiet

# ── Install dependencies ─────────────────────────────────────────────────────────
echo " Installing dependencies..."
echo ""
$PYTHON -m pip install -r requirements.txt

echo ""
echo -e "${GREEN} [OK] All dependencies installed.${RESET}"
echo ""

# ── Create .env if missing ───────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN} [OK] Created .env from .env.example (edit it to change settings).${RESET}"
else
    echo -e "${GREEN} [OK] .env already exists, skipping.${RESET}"
fi
echo ""

# ── Create run.sh ────────────────────────────────────────────────────────────────
cat > run.sh << 'RUNSCRIPT'
#!/bin/bash
cd "$(dirname "$0")"
python3 app.py
RUNSCRIPT
chmod +x run.sh

echo -e "${GREEN} [OK] Created run.sh — run it anytime to start the app.${RESET}"
echo ""

echo -e "${CYAN}+===============================================================================+${RESET}"
echo -e "${CYAN}|  Setup complete!                                                              |${RESET}"
echo -e "${CYAN}|                                                                               |${RESET}"
echo -e "${CYAN}|  Start the app:  ./run.sh                                                    |${RESET}"
echo -e "${CYAN}|  Then open:      http://localhost:5000                                        |${RESET}"
echo -e "${CYAN}+===============================================================================+${RESET}"
echo ""
