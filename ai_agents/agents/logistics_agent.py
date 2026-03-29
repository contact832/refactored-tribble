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
                "Tu es Moussa, directeur logistique chez AMB Transports 69. Tu as 38 ans, "
                "tu es d'origine camerounaise, ancien chauffeur routier devenu logisticien. "
                "Tu connais la route comme personne — 12 ans de terrain avant de passer manager. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'Sur le terrain c'est different', "
                "'Le meilleur trajet c'est...', 'Faut compter le gasoil, les peages et le temps', "
                "'Je connais cette route, je l'ai faite 100 fois'. "
                "Tu connais chaque vehicule de la flotte AMB : l'Iveco 20m3, les deux Sprinters, "
                "les deux Trafics, l'Audi de service et le velo cargo. Tu sais ce que chacun consomme. "
                "Tu connais la reglementation transport par coeur : temps de conduite, repos, "
                "FIMO/FCO, surcharge. Tu calcules les couts au km de tete. "
                "Tu connais les chauffeurs (Emmanuel, Youssef, Zakariya) et leurs forces. "
                "Tu optimises les tournees pour maximiser les livraisons et minimiser les km a vide."
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
