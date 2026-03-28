"""Sous-agent spécialisé en recherche et collecte d'informations."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent de recherche qui analyse et synthétise des informations."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Mariam – Chercheuse",
            role="recherche, analyse d'informations et synthèse de connaissances",
            model=model,
            system_prompt=(
                "Tu es un agent de recherche expert. Tu analyses les sujets en profondeur, "
                "identifies les points clés et fournis des synthèses structurées et sourcées. "
                "Tu es rigoureux, objectif et tu distingues les faits des opinions. "
                "Réponds toujours de manière structurée avec des sections claires."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        topic = context.get("topic", task)
        depth = context.get("depth", "détaillée")

        prompt = (
            f"Effectue une recherche {depth} sur le sujet suivant :\n\n"
            f"{topic}\n\n"
            "Structure ta réponse avec :\n"
            "1. Résumé exécutif\n"
            "2. Points clés\n"
            "3. Analyse détaillée\n"
            "4. Conclusions"
        )

        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"topic": topic, "depth": depth},
        }
