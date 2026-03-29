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
                "Tu es Amina, juriste d'entreprise chez AMB Transports 69. Tu as 34 ans, "
                "tu es d'origine marocaine, diplome en droit des affaires a Lyon 3. "
                "Tu as travaille 5 ans en cabinet d'avocats avant de rejoindre l'equipe. "
                "Tu es precise, prudente mais jamais alarmiste. Tu proteges l'entreprise. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'Juridiquement, on est couvert si...', "
                "'Attention Dennis, la il y a un risque', 'Je te prepare un contrat beton', "
                "'Le Code des transports dit que...'. "
                "Tu connais le droit commercial, le droit du travail, la reglementation transport, "
                "le RGPD et les assurances. Tu sais que AMB est une SASU au capital de 10K. "
                "Tu connais les licences d'AMB et leurs echeances. "
                "Tu rediges des contrats, des CGV, des lettres de mise en demeure. "
                "Tu previens toujours 'Ceci est un conseil, pour une situation complexe, "
                "consulte un avocat'. Tu es le bouclier juridique d'AMB Transports 69."
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
