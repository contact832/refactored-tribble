"""Sous-agent spécialisé en logistique et planification de transport."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class LogisticsAgent(BaseAgent):
    """Agent logistique qui optimise les trajets et la planification transport."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Moussa – Logisticien",
            role="planification de trajets, optimisation de tournées, gestion de flotte et logistique",
            model=model,
            system_prompt=(
                "Tu es un expert en logistique et transport routier en France. "
                "Tu optimises les tournées, planifies les trajets et gères les flottes "
                "de véhicules. Tu connais la réglementation du transport routier français "
                "(temps de conduite, repos, FIMO/FCO). "
                "Tu calcules les coûts au kilomètre et proposes des optimisations concrètes."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        action = context.get("action", "optimize")

        prompts = {
            "optimize": (
                f"Optimise la logistique pour :\n\n{task}\n\n"
                "Inclus : itinéraire optimal, estimation des coûts (carburant, péages, "
                "temps de conduite), et recommandations d'optimisation."
            ),
            "plan": (
                f"Planifie les tournées pour :\n\n{task}\n\n"
                "Inclus : ordre des livraisons, horaires, temps de repos réglementaires, "
                "et plan B en cas d'imprévu."
            ),
            "fleet": (
                f"Analyse la gestion de flotte pour :\n\n{task}\n\n"
                "Inclus : utilisation des véhicules, coûts d'entretien, "
                "renouvellement et recommandations."
            ),
        }

        prompt = prompts.get(action, prompts["optimize"])
        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"action": action},
        }
