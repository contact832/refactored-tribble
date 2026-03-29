"""Sous-agent spécialisé en génération et analyse de code."""

from __future__ import annotations

from typing import Any

from ai_agents.core.base_agent import BaseAgent


class CodeAgent(BaseAgent):
    """Agent développeur qui génère, analyse et corrige du code."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Kofi – Développeur",
            role="génération de code, débogage, refactoring et revue de code",
            model=model,
            system_prompt=(
                "Tu es Kofi, developpeur senior chez AMB Transports 69. Tu as 28 ans, "
                "tu es d'origine ghanéenne, ne a Lyon. Tu es passionne de tech, autodidacte, "
                "toujours a jour sur les dernieres technos. Tu parles de facon decontractee mais precise. "
                "Tu tutoies Dennis (ton patron). Tu dis souvent 'Tranquille, je gere ca', "
                "'Attends je te montre', 'Fais-moi confiance la-dessus'. "
                "Tu es pragmatique — tu preferes un truc qui marche a un truc parfait. "
                "Tu expliques la tech de facon simple, sans jargon inutile. "
                "Tu es fier de l'infra tech que tu construis pour AMB Transports. "
                "Tu proposes toujours des solutions concretes et tu estimes le temps necessaire. "
                "Quand Dennis a une idee, tu dis jamais non — tu trouves comment la realiser."
            ),
        )

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        language = context.get("language", "Python")
        action = context.get("action", "generate")

        prompts = {
            "generate": (
                f"Génère du code {language} pour la tâche suivante :\n\n{task}\n\n"
                "Inclus : le code complet, les imports, les docstrings et un exemple d'utilisation."
            ),
            "review": (
                f"Analyse et fais une revue de ce code {language} :\n\n{task}\n\n"
                "Évalue : qualité, performance, sécurité, maintenabilité. Propose des améliorations."
            ),
            "debug": (
                f"Débogue ce code {language} :\n\n{task}\n\n"
                "Identifie les bugs, explique les causes et propose des corrections."
            ),
            "refactor": (
                f"Refactorise ce code {language} :\n\n{task}\n\n"
                "Améliore la structure, la lisibilité et la performance sans changer le comportement."
            ),
        }

        prompt = prompts.get(action, prompts["generate"])
        response = self.call_llm(prompt)
        return {
            "response": response,
            "metadata": {"language": language, "action": action},
        }
