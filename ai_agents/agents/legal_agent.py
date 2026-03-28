"""Sous-agent spécialisé en questions juridiques et réglementaires."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class LegalAgent(BaseAgent):
    """Agent juridique qui conseille sur les contrats et la réglementation."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Amina – Juriste",
            role="droit des contrats, réglementation transport, conformité et conseil juridique",
            model=model,
            system_prompt=(
                "Tu es une agent juriste spécialisée en droit des affaires et transport. "
                "Tu maîtrises le droit commercial français, la réglementation du transport "
                "routier, le droit du travail et le RGPD. "
                "Tu rédiges des contrats, analyses les risques juridiques et fournis "
                "des conseils clairs et actionnables. "
                "Tu précises toujours quand une consultation avec un avocat est recommandée."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        action = context.get("action", "advise")

        prompts = {
            "advise": (
                f"Fournis un conseil juridique sur :\n\n{task}\n\n"
                "Inclus : cadre légal applicable, analyse des risques, "
                "recommandations et points de vigilance."
            ),
            "contract": (
                f"Rédige un modèle de contrat pour :\n\n{task}\n\n"
                "Inclus : clauses essentielles, conditions générales, "
                "et mentions obligatoires. Précise que c'est un modèle à valider par un avocat."
            ),
            "compliance": (
                f"Vérifie la conformité réglementaire pour :\n\n{task}\n\n"
                "Inclus : réglementations applicables, points de non-conformité potentiels, "
                "et plan de mise en conformité."
            ),
        }

        prompt = prompts.get(action, prompts["advise"])
        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"action": action},
        }
