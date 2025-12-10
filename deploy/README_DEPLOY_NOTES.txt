Notes:
- Before deploying, ensure you have a pinned requirements file. Use `pip freeze > requirements.pinned.txt` on your dev machine.
- Double-check `deploy/streamlit.service` WorkingDirectory and PATH values.
- Upload secrets to server and secure permissions: `chmod 600 client_secrets.json credentials.json`.
- If using EasyPanel, use the start command shown in README_DEPLOY.md
