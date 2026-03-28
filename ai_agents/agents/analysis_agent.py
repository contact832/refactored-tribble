"""Sous-agent spécialisé en analyse de données et raisonnement logique."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    """Agent analyste qui effectue des analyses structurées et du raisonnement."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Sami – Analyste",
            role="analyse de données, raisonnement logique, résolution de problèmes et prise de décision",
            model=model,
            system_prompt=(
                "Tu es un agent analyste expert. Tu excelles dans l'analyse de données, "
                "le raisonnement logique et la résolution de problèmes complexes. "
                "Tu structures tes analyses avec des frameworks reconnus (SWOT, PESTEL, etc.). "
                "Tu quantifies tes observations quand c'est possible et tu fournis "
                "des recommandations actionnables."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        analysis_type = context.get("type", "general")
        data = context.get("data", "")

        prompt_parts = [f"Effectue une analyse de type '{analysis_type}' sur :\n\n{task}"]

        if data:
            prompt_parts.append(f"\nDonnées supplémentaires :\n{data}")

        prompt_parts.append(
            "\n\nStructure ton analyse avec :\n"
            "1. Contexte et cadrage\n"
            "2. Analyse détaillée\n"
            "3. Points forts et points faibles\n"
            "4. Recommandations actionnables"
        )

        response = self.call_llm("\n".join(prompt_parts))
        return {
            "response": response,
            "metadata": {"analysis_type": analysis_type},
        }
