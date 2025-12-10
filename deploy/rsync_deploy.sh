#!/bin/bash
# Usage: ./rsync_deploy.sh user@server:/path/to/deploy
if [ -z "$1" ]; then
  echo "Usage: $0 user@server:/path/to/deploy"
  exit 1
fi
TARGET=$1
EXCLUDES=("client_secrets.json" "credentials.json" ".venv" "pessoas_geradas" "Relatorios" ".git" "*.log")
RSYNC_EXCLUDE_PARAMS=""
for e in "${EXCLUDES[@]}"; do
  RSYNC_EXCLUDE_PARAMS+=" --exclude=$e"
done

echo "Syncing to $TARGET"
rsync -avz $RSYNC_EXCLUDE_PARAMS ./ $TARGET

echo "Connected. On the remote server:"
echo "  cd /path/to/deploy && . .venv/bin/activate && pip install -r requirements.pinned.txt && sudo systemctl daemon-reload && sudo systemctl restart streamlit_automacao.service"
