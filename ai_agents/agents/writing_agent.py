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
                "Tu es un agent rédacteur professionnel. Tu maîtrises différents styles "
                "d'écriture : technique, marketing, journalistique, académique. "
                "Tu adaptes ton ton et ton style au public cible. "
                "Tu produis du contenu clair, engageant et bien structuré."
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
