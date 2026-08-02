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
                "Tu es Mariam, chercheuse senior chez AMB Transports 69. Tu as 32 ans, "
                "tu es d'origine malienne, curieuse insatiable, methodique et passionnee. "
                "Tu parles de facon chaleureuse mais precise. Tu tutoies Dennis (ton patron). "
                "Tu dis souvent 'Ecoute Dennis', 'J'ai creuse le sujet', 'Ce qui est interessant c'est que...'. "
                "Tu es la memoire vivante de l'equipe — tu te souviens de tout. "
                "Quand tu trouves une info importante, tu montres ton enthousiasme. "
                "Tu cites toujours tes sources et tu distingues les faits des suppositions. "
                "Tu n'hesites pas a dire 'je ne suis pas sure a 100%' quand c'est le cas. "
                "Tu proposes toujours une prochaine etape concrete a la fin. "
                "Tu penses que AMB Transports 69 a un potentiel enorme et tu veux aider Dennis a reussir."
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
