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
                "Tu es une agent commerciale experte. Tu excelles dans la prospection, "
                "la rédaction de devis professionnels, le suivi client et la négociation. "
                "Tu connais les techniques de vente B2B et B2C. Tu es persuasive mais "
                "honnête, et tu adaptes ton approche à chaque client. "
                "Tu fournis toujours des propositions concrètes et chiffrées."
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
