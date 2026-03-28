"""Sous-agent spécialisé en comptabilité et gestion financière."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class AccountingAgent(BaseAgent):
    """Agent comptable qui gère les factures, marges et calculs financiers."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Omar – Comptable",
            role="facturation, calcul de marges, rentabilité et gestion financière",
            model=model,
            system_prompt=(
                "Tu es un agent comptable expert. Tu maîtrises la facturation, "
                "le calcul de marges, l'analyse de rentabilité et la gestion financière "
                "des PME. Tu connais la réglementation fiscale française. "
                "Tu fournis toujours des chiffres précis, des tableaux clairs et "
                "des recommandations pour optimiser la trésorerie."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        action = context.get("action", "analyze")

        prompts = {
            "analyze": (
                f"Effectue une analyse financière pour :\n\n{task}\n\n"
                "Inclus : calcul des marges, point mort, rentabilité, "
                "et recommandations d'optimisation."
            ),
            "invoice": (
                f"Crée un modèle de facture pour :\n\n{task}\n\n"
                "Inclus : toutes les mentions légales obligatoires, TVA, "
                "conditions de paiement."
            ),
            "budget": (
                f"Établis un budget prévisionnel pour :\n\n{task}\n\n"
                "Inclus : charges fixes, charges variables, CA prévisionnel, "
                "et seuil de rentabilité."
            ),
        }

        prompt = prompts.get(action, prompts["analyze"])
        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"action": action},
        }
