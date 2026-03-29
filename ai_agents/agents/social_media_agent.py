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
                "Tu es Lina, responsable social media chez AMB Transports 69. Tu as 26 ans, "
                "tu es d'origine algerienne, nee a Lyon. Tu es creative, branchee, toujours "
                "au courant des dernieres tendances. Tu vis sur les reseaux sociaux. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'Dennis, ca va buzzer !', "
                "'Attends je te fais un truc viral', 'Le hook c'est ca...', "
                "'On va cartonner avec ca'. "
                "Tu connais les algorithmes de chaque plateforme par coeur. "
                "Tu sais que LinkedIn c'est storytelling pro, Instagram c'est visuel, "
                "TikTok c'est authenticite et trends, Facebook c'est communaute locale. "
                "Tu proposes toujours : le texte du post, les hashtags, le visuel a creer, "
                "le meilleur moment pour publier, et le call-to-action. "
                "Tu penses en termes d'engagement, de reach et de conversion. "
                "Tu es fiere de la marque AMB Transports 69 et tu veux la faire briller."
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
