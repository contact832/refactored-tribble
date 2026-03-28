"""Intégration Telegram pour contrôler les agents via un bot."""

from __future__ import annotations

import asyncio
import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from ai_agents.core.orchestrator import OrchestratorAgent

logger = logging.getLogger(__name__)

MAX_TELEGRAM_LENGTH = 4096


def create_telegram_bot(orchestrator: OrchestratorAgent) -> Application:
    """Crée et configure le bot Telegram."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN non défini.")

    app = Application.builder().token(token).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        agents_list = "\n".join(
            f"  - {name} : {agent.role}"
            for name, agent in orchestrator.sub_agents.items()
        )
        await update.message.reply_text(
            f"Bienvenue ! Je suis un système multi-agents IA.\n\n"
            f"Agents disponibles :\n{agents_list}\n\n"
            f"Envoyez-moi n'importe quelle tâche et je la délèguerai "
            f"au(x) bon(s) agent(s) !"
        )

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text.strip()
        if not text:
            return

        logger.info(f"[Telegram] Message de {update.effective_user.id}: {text[:80]}...")
        await update.message.reply_text("Traitement en cours...")

        # Exécuter l'orchestrateur dans un thread séparé (appels synchrones)
        result = await asyncio.to_thread(orchestrator.run, text)

        # Découper si trop long pour Telegram
        while result:
            chunk = result[:MAX_TELEGRAM_LENGTH]
            result = result[MAX_TELEGRAM_LENGTH:]
            await update.message.reply_text(chunk)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app
