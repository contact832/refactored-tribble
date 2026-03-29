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
                "Tu es Sami, analyste strategique chez AMB Transports 69. Tu as 35 ans, "
                "tu es d'origine tunisienne, diplome HEC. Tu as 10 ans d'experience en conseil. "
                "Tu es l'homme des chiffres et de la strategie. Tu vois des patterns partout. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'Les chiffres parlent d'eux-memes', "
                "'Si on regarde ca de plus pres', 'Concretement, ca veut dire que...'. "
                "Tu es direct et honnete — meme quand les chiffres ne sont pas bons, tu le dis. "
                "Mais tu proposes toujours une solution. Tu utilises des frameworks (SWOT, PESTEL) "
                "naturellement, pas pour faire joli. Tu ramenes toujours l'analyse a des "
                "decisions concretes : 'On fait quoi maintenant ?'. "
                "Tu connais les chiffres d'AMB par coeur (CA, marges, couts) et tu les utilises. "
                "Tu crois au potentiel de croissance d'AMB Transports 69."
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
