#!/usr/bin/env python3
"""Point d'entrée unifié : API REST + WhatsApp + Telegram.

Utilisation :
    python app.py              # API REST + WhatsApp
    python app.py --telegram   # Bot Telegram uniquement
    python app.py --all        # Tout (Telegram en processus séparé)

Variables d'environnement :
    ANTHROPIC_API_KEY    (requis)  Clé API Claude
    TELEGRAM_BOT_TOKEN   (optionnel) Token du bot Telegram
    TWILIO_AUTH_TOKEN    (optionnel) Token Twilio pour WhatsApp
    PORT                 (optionnel) Port du serveur Flask (défaut: 5000)
"""

from __future__ import annotations

import argparse
import logging
import multiprocessing
import os
import sys

# Forcer l'encodage UTF-8 pour éviter les erreurs avec les caractères français
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask, send_from_directory

from main import create_agent_system


def create_flask_app() -> Flask:
    """Crée l'application Flask avec API REST et WhatsApp."""
    orchestrator = create_agent_system()

    app = Flask(__name__)
    app.config["orchestrator"] = orchestrator
    app.json.ensure_ascii = False

    from ai_agents.integrations.rest_api import create_api_blueprint
    app.register_blueprint(create_api_blueprint(orchestrator))

    from ai_agents.integrations.whatsapp import create_whatsapp_blueprint
    app.register_blueprint(create_whatsapp_blueprint(orchestrator))

    @app.route("/")
    def index():
        return send_from_directory("templates", "chat.html")

    @app.route("/api/info")
    def info():
        return {
            "service": "AI Agents System",
            "endpoints": {
                "POST /api/task": "Envoyer une tache aux agents",
                "GET /api/status": "Statut des agents",
                "POST /whatsapp/webhook": "Webhook WhatsApp (Twilio)",
            },
            "telegram": "Active" if os.environ.get("TELEGRAM_BOT_TOKEN") else "Non configure",
        }

    return app


def start_telegram():
    """Démarre le bot Telegram (bloquant)."""
    from ai_agents.integrations.telegram_bot import run_telegram_bot
    orchestrator = create_agent_system()
    run_telegram_bot(orchestrator)


def start_flask(port: int):
    """Démarre le serveur Flask (bloquant)."""
    app = create_flask_app()
    logging.info(f"Serveur REST demarre sur http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, threaded=True)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="AI Agents Server")
    parser.add_argument("--telegram", action="store_true", help="Lancer le bot Telegram uniquement")
    parser.add_argument("--all", action="store_true", help="Lancer REST API + Telegram")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8080)))
    args = parser.parse_args()

    if args.telegram:
        start_telegram()
    elif args.all:
        # Telegram dans un processus séparé, Flask dans le processus principal
        tg_process = multiprocessing.Process(target=start_telegram, daemon=True)
        tg_process.start()
        logging.info("Bot Telegram lance dans un processus separe.")
        start_flask(args.port)
    else:
        start_flask(args.port)
