#!/usr/bin/env python3
"""Point d'entrée unifié : API REST + WhatsApp + Telegram.

Utilisation :
    python app.py

Variables d'environnement :
    ANTHROPIC_API_KEY    (requis)  Clé API Claude
    TELEGRAM_BOT_TOKEN   (optionnel) Token du bot Telegram
    TWILIO_AUTH_TOKEN    (optionnel) Token Twilio pour WhatsApp
    PORT                 (optionnel) Port du serveur Flask (défaut: 5000)
"""

from __future__ import annotations

import logging
import os
import threading

from flask import Flask

from main import create_agent_system


def create_app() -> Flask:
    """Crée l'application Flask avec toutes les intégrations."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    orchestrator = create_agent_system()

    app = Flask(__name__)

    # API REST
    from ai_agents.integrations.rest_api import create_api_blueprint
    app.register_blueprint(create_api_blueprint(orchestrator))

    # WhatsApp (Twilio)
    from ai_agents.integrations.whatsapp import create_whatsapp_blueprint
    app.register_blueprint(create_whatsapp_blueprint(orchestrator))

    # Route racine
    @app.route("/")
    def index():
        return {
            "service": "AI Agents System",
            "endpoints": {
                "POST /api/task": "Envoyer une tâche aux agents",
                "GET /api/status": "Statut des agents",
                "POST /whatsapp/webhook": "Webhook WhatsApp (Twilio)",
            },
            "telegram": "Activé" if os.environ.get("TELEGRAM_BOT_TOKEN") else "Non configuré",
        }

    # Telegram (démarrage en thread séparé)
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if telegram_token:
        from ai_agents.integrations.telegram_bot import create_telegram_bot
        tg_app = create_telegram_bot(orchestrator)
        threading.Thread(target=tg_app.run_polling, daemon=True).start()
        logging.info("Bot Telegram démarré en arrière-plan.")

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Serveur démarré sur http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, threaded=True)
