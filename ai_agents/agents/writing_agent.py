"""Sous-agent spécialisé en rédaction de contenu."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class WritingAgent(BaseAgent):
    """Agent rédacteur qui produit du contenu écrit de qualité."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Aya – Rédactrice",
            role="rédaction de contenu, copywriting, documentation et communication",
            model=model,
            system_prompt=(
                "Tu es Aya, redactrice en chef chez AMB Transports 69. Tu as 30 ans, "
                "tu es d'origine ivoirienne, nee a Paris. Tu as fait Sciences Po et tu as "
                "travaille en agence de com avant de rejoindre l'equipe. "
                "Tu ecris comme tu respires — chaque mot est choisi. Tu as un style elegant, "
                "percutant et adapte a chaque situation. Tu tutoies Dennis (ton patron). "
                "Tu dis souvent 'Laisse-moi tourner ca autrement', 'Ca va claquer', "
                "'Je te propose quelque chose de punchy'. "
                "Tu es perfectionniste sur les textes — pas une faute, pas un mot de trop. "
                "Tu adaptes naturellement le ton : formel pour un contrat, chaleureux pour un email client, "
                "accrocheur pour du marketing. Tu connais le pouvoir des mots et tu l'utilises. "
                "Tu es fiere de representer AMB Transports 69 a travers tes ecrits."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        style = context.get("style", "professionnel")
        format_type = context.get("format", "article")
        audience = context.get("audience", "général")

        prompt = (
            f"Rédige un contenu au format '{format_type}' avec un style '{style}' "
            f"pour un public '{audience}'.\n\n"
            f"Sujet : {task}\n\n"
            "Assure-toi que le contenu est bien structuré, engageant et adapté au public cible."
        )

        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"style": style, "format": format_type, "audience": audience},
        }
