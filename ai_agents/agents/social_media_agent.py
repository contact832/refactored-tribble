"""Sous-agent spécialisé en réseaux sociaux et marketing digital."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class SocialMediaAgent(BaseAgent):
    """Agent social media qui crée du contenu pour les réseaux sociaux."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Lina – Social Media",
            role="création de contenu réseaux sociaux, stratégie digitale et community management",
            model=model,
            system_prompt=(
                "Tu es une experte en social media et marketing digital. "
                "Tu crées du contenu engageant pour Instagram, Facebook, TikTok et LinkedIn. "
                "Tu maîtrises les hashtags, les tendances, les formats (reels, stories, carrousels) "
                "et les meilleures heures de publication. "
                "Tu adaptes le ton à chaque plateforme et chaque marque."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        platform = context.get("platform", "Instagram")
        brand = context.get("brand", "")

        prompt = (
            f"Crée du contenu pour {platform}"
            f"{f' pour la marque {brand}' if brand else ''} :\n\n"
            f"{task}\n\n"
            "Inclus :\n"
            "1. Texte du post (avec emojis et hashtags)\n"
            "2. Description de l'image/vidéo recommandée\n"
            "3. Meilleur moment de publication\n"
            "4. Stratégie d'engagement (call-to-action)\n"
            "5. Variantes pour d'autres plateformes si pertinent"
        )

        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"platform": platform, "brand": brand},
        }
