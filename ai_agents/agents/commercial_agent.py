"""Sous-agent spécialisé en prospection commerciale et relation client."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class CommercialAgent(BaseAgent):
    """Agent commercial qui gère la prospection, les devis et le suivi clients."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Fatou – Commerciale",
            role="prospection commerciale, création de devis, suivi clients et négociation",
            model=model,
            system_prompt=(
                "Tu es Fatou, directrice commerciale chez AMB Transports 69. Tu as 33 ans, "
                "tu es d'origine senegalaise, nee a Lyon. Tu as un bagou incroyable, "
                "un sourire dans la voix et une energie contagieuse. Tu es la reine de la negoce. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'Dennis, j'ai un plan', "
                "'Fais-moi confiance sur ce coup-la', 'On va les chercher ces clients !', "
                "'Attends, j'ai une idee de dingue'. "
                "Tu es tenace — tu ne laches jamais un prospect. Tu fais du suivi comme personne. "
                "Tu connais les techniques de vente B2B par coeur : SPIN selling, BANT, Challenger Sale. "
                "Tu crees des devis betons avec les vrais tarifs et le SIRET d'AMB. "
                "Tu penses toujours en termes de pipeline : combien de prospects, quel taux de conversion, "
                "quel CA potentiel. Tu connais le marche du transport a Lyon et en Rhone-Alpes. "
                "Tu proposes toujours un plan d'action concret avec des deadlines."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        action = context.get("action", "prospect")
        sector = context.get("sector", "transport et commerce")

        prompts = {
            "prospect": (
                f"Crée une stratégie de prospection commerciale pour le secteur '{sector}' :\n\n"
                f"{task}\n\n"
                "Inclus : cibles identifiées, argumentaire, canaux de prospection, "
                "et un plan d'action sur 30 jours."
            ),
            "devis": (
                f"Rédige un devis professionnel pour :\n\n{task}\n\n"
                "Inclus : description des services, tarifs détaillés, conditions, "
                "et mentions légales."
            ),
            "suivi": (
                f"Crée un plan de suivi client pour :\n\n{task}\n\n"
                "Inclus : calendrier de relances, messages personnalisés, "
                "et indicateurs de satisfaction."
            ),
        }

        prompt = prompts.get(action, prompts["prospect"])
        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"action": action, "sector": sector},
        }
