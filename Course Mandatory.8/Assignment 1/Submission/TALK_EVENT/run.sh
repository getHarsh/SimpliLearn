#!/opt/homebrew/bin/bash
# run.sh - Project Management MCP Server

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/BUILD_WITH_AI"
LOG_FILE="${SCRIPT_DIR}/server.log"

# Clear log file if it exists
> "$LOG_FILE"

# Redirect all stdout to stderr, preserving original stdout for MCP
exec 3>&1
exec 1>&2

# Cleanup handler
cleanup() {
    echo "🛑 Stopping server..." >> "$LOG_FILE"
    pkill -P $$ 2>/dev/null || true
    exit 0
}

trap cleanup EXIT SIGINT SIGTERM

# Setup environment
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment..." >> "$LOG_FILE"
    python3 -m venv "$VENV_DIR" 2>> "$LOG_FILE"
fi

echo "⚡ Activating virtual environment" >> "$LOG_FILE"
source "$VENV_DIR/bin/activate"

echo "📦 Installing dependencies..." >> "$LOG_FILE"
pip3 install -r "$SCRIPT_DIR/requirements.txt" >> "$LOG_FILE" 2>&1

echo "🚀 Starting MCP Server..." >> "$LOG_FILE"

# Run server with strict I/O separation - using fd 3 for clean JSON output
"$VENV_DIR/bin/python3" -u "$SCRIPT_DIR/mcp_server.py" >&3 2>> "$LOG_FILE"
