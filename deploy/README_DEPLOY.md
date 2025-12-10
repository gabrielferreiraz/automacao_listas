Deployment checklist for Automação de Listas

This README contains recommended steps to deploy the Streamlit app to a Linux VPS (systemd + nginx). Adjust usernames, paths and domain names as needed.

1) Copy repository to server
   - Place the project at `/opt/automacao_de_listas` (example).

2) Create and activate a Python virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3) Secure secrets
   - Do NOT commit `client_secrets.json` or `credentials.json` to Git.
   - Upload them to the server in a secure directory (same project folder) and protect permissions:
     chmod 600 client_secrets.json credentials.json

4) Create systemd service
   - Copy `deploy/streamlit.service` to `/etc/systemd/system/streamlit_automacao.service`
   - Edit `WorkingDirectory`, `User` and `Environment PATH` to match your install.
   - Reload systemd and enable service:
     sudo systemctl daemon-reload
     sudo systemctl enable --now streamlit_automacao.service

5) Configure nginx reverse-proxy
   - Copy `deploy/nginx_streamlit.conf` into `/etc/nginx/sites-available/automacao` and symlink to `sites-enabled`.
   - Update `server_name` to your domain.
   - Test and reload nginx:
     sudo nginx -t
     sudo systemctl reload nginx

6) HTTPS
   - Use Certbot to obtain TLS cert for your domain and enable HTTPS on nginx.

7) Optional: Supervisor / EasyPanel
   - If using EasyPanel, create an app using the same start command:
     /opt/automacao_de_listas/.venv/bin/streamlit run report_generator.py --server.port=8501 --server.enableCORS=false

8) Logging and monitoring
   - Configure logrotate for any log files you create.
   - Use `journalctl -u streamlit_automacao.service -f` to follow logs.

9) Rollback plan
   - Keep a copy of the previous release directory and a script to restart the service after rollback.

Notes and hints
- Pin your `requirements.txt` before deploying (use `pip freeze > requirements.pinned.txt`).
- Test the app locally with a virtualenv before deploying to reduce surprises.
