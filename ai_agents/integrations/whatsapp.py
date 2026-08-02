"""Intégration WhatsApp via Twilio webhook."""

from __future__ import annotations

import logging
import os

from flask import Blueprint, request

from ai_agents.core.orchestrator import OrchestratorAgent

logger = logging.getLogger(__name__)

MAX_WHATSAPP_LENGTH = 1600


def create_whatsapp_blueprint(orchestrator: OrchestratorAgent) -> Blueprint:
    """Crée un blueprint Flask pour le webhook WhatsApp Twilio."""
    whatsapp = Blueprint("whatsapp", __name__, url_prefix="/whatsapp")

    @whatsapp.route("/webhook", methods=["POST"])
    def webhook():
        from twilio.twiml.messaging_response import MessagingResponse
        from twilio.request_validator import RequestValidator

        # Validation de la signature Twilio (skip en mode debug)
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
        if auth_token:
            validator = RequestValidator(auth_token)
            url = request.url
            signature = request.headers.get("X-Twilio-Signature", "")
            if not validator.validate(url, request.form, signature):
                logger.warning("Signature Twilio invalide")
                return "Forbidden", 403

        body = request.form.get("Body", "").strip()
        sender = request.form.get("From", "unknown")
        logger.info(f"[WhatsApp] Message de {sender}: {body[:80]}...")

        if not body:
            resp = MessagingResponse()
            resp.message("Envoyez-moi une tâche et mes agents IA s'en occuperont !")
            return str(resp), 200, {"Content-Type": "text/xml"}

        result = orchestrator.run(body)

        # Tronquer si nécessaire (limite WhatsApp)
        if len(result) > MAX_WHATSAPP_LENGTH:
            result = result[:MAX_WHATSAPP_LENGTH - 25] + "\n\n... (réponse tronquée)"

        resp = MessagingResponse()
        resp.message(result)
        return str(resp), 200, {"Content-Type": "text/xml"}

    return whatsapp
