#!/usr/bin/env bash
# Run the API locally and expose it via a Cloudflare quick tunnel.
# No Cloudflare account required — `cloudflared` prints a random
# https://<words>.trycloudflare.com URL that anyone can hit while this
# script is running. Ctrl+C tears down both processes.
#
# One-time setup:
#   brew install cloudflared   # macOS — see github.com/cloudflare/cloudflared for other OSes

set -euo pipefail

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared not found. Install with:  brew install cloudflared" >&2
  exit 1
fi

PORT="${PORT:-8000}"

# Start uvicorn in the background, kill it on exit.
uvicorn main:app --host 127.0.0.1 --port "$PORT" --reload &
UVICORN_PID=$!
trap 'kill "$UVICORN_PID" 2>/dev/null || true' EXIT INT TERM

# Wait briefly for uvicorn to bind, then start the tunnel in the foreground.
sleep 1
echo
echo "Starting Cloudflare quick tunnel — public URL appears below."
echo "Press Ctrl+C to stop both the API and the tunnel."
echo
cloudflared tunnel --url "http://localhost:$PORT"
