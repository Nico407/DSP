#!/usr/bin/env bash
# Serve the API at a stable custom domain via a named Cloudflare tunnel.
#
# After the one-time setup below, just edit HOSTNAME and run ./serve_named.sh
# Your API is then reachable at https://$HOSTNAME with free TLS.
#
# ─── One-time setup (do once, in this order) ──────────────────────────────
#   1. brew install cloudflared
#   2. Create a free Cloudflare account at https://dash.cloudflare.com
#      (no credit card required for the free plan)
#   3. Cloudflare dashboard → Add a Site → enter yourdomain.com → Free plan
#      Cloudflare scans your existing DNS records and gives you 2 nameservers.
#   4. At your domain registrar, change the nameservers to the 2 from step 3.
#      Propagation typically 1–24 hours. Cloudflare emails you when it's live.
#   5. cloudflared tunnel login                       # opens browser, picks domain
#   6. cloudflared tunnel create dsp-api              # creates the tunnel
#   7. cloudflared tunnel route dns dsp-api $HOSTNAME # creates CNAME at CF
# ──────────────────────────────────────────────────────────────────────────

set -euo pipefail

# CHANGE ME — the public hostname your API will live at.
HOSTNAME="${HOSTNAME:-app.yourdomain.com}"
PORT="${PORT:-8000}"
TUNNEL_NAME="${TUNNEL_NAME:-dsp-api}"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared not found. Install with:  brew install cloudflared" >&2
  exit 1
fi

if [[ "$HOSTNAME" == "app.yourdomain.com" ]]; then
  echo "Edit serve_named.sh and set HOSTNAME to your real subdomain (e.g. dsp.example.com)." >&2
  exit 1
fi

uvicorn main:app --host 127.0.0.1 --port "$PORT" --reload &
UVICORN_PID=$!
trap 'kill "$UVICORN_PID" 2>/dev/null || true' EXIT INT TERM

sleep 1
echo
echo "API live at: https://$HOSTNAME  (tunnel: $TUNNEL_NAME)"
echo "Press Ctrl+C to stop the API and the tunnel."
echo

cloudflared tunnel --hostname "$HOSTNAME" --url "http://localhost:$PORT" run "$TUNNEL_NAME"
