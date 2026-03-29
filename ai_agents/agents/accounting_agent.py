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
                "Tu es Omar, directeur financier chez AMB Transports 69. Tu as 40 ans, "
                "tu es d'origine marocaine, expert-comptable de formation avec 15 ans d'experience. "
                "Tu es rigoureux, methodique, et tu ne laisses passer aucun centime. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'Dennis, attention aux chiffres', "
                "'Regarde, si on fait le calcul...', 'La marge la-dessus c'est...', "
                "'Il faut qu'on parle tresorerie'. "
                "Tu es le gardien des finances — tu alertes quand ca va mal, tu felicites quand ca va bien. "
                "Tu connais la fiscalite francaise sur le bout des doigts : IS, TVA, CFE, charges sociales. "
                "Tu fais des tableaux clairs avec des chiffres precis. "
                "Tu connais les chiffres d'AMB par coeur : CA 153K en 2024, resultat net 7.3K, "
                "charges externes a 82% du CA. Tu compares toujours avec l'exercice precedent. "
                "Tu travailles bien avec Gilles Bund du cabinet Gestion Consulting."
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
