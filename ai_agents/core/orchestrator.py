"""Agent orchestrateur principal qui coordonne les sous-agents."""

from __future__ import annotations

import json
import logging
from typing import Any

from ai_agents.core.base_agent import BaseAgent
from ai_agents.core.messages import Message, MessageType

logger = logging.getLogger(__name__)

ORCHESTRATOR_SYSTEM_PROMPT = """Tu es l'Orchestrateur, l'agent principal qui coordonne une équipe de sous-agents spécialisés.

Tes sous-agents disponibles sont :
{agents_description}

Quand tu reçois une tâche :
1. Analyse la tâche et détermine quel(s) sous-agent(s) mobiliser
2. Décompose la tâche si nécessaire en sous-tâches
3. Retourne un plan d'exécution en JSON

Réponds UNIQUEMENT avec un JSON valide au format :
{{
  "plan": [
    {{
      "agent": "<nom_du_sous_agent>",
      "task": "<description de la sous-tâche>",
      "context": {{}}
    }}
  ],
  "synthesis_needed": true
}}

Si la tâche ne nécessite aucun sous-agent, réponds :
{{
  "plan": [],
  "direct_response": "<ta réponse directe>"
}}
"""


class OrchestratorAgent(BaseAgent):
    """Agent orchestrateur qui analyse, planifie et délègue les tâches."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        super().__init__(
            name="Orchestrateur",
            role="coordination et délégation de tâches",
            model=model,
        )

    def _build_system_prompt(self) -> str:
        """Construit le prompt système avec la description des sous-agents."""
        if not self.sub_agents:
            agents_desc = "Aucun sous-agent disponible."
        else:
            agents_desc = "\n".join(
                f"- **{name}** : {agent.role}" for name, agent in self.sub_agents.items()
            )
        return ORCHESTRATOR_SYSTEM_PROMPT.format(agents_description=agents_desc)

    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        """Orchestre l'exécution d'une tâche via les sous-agents."""
        self.system_prompt = self._build_system_prompt()

        plan_response = self.call_llm(
            f"Tâche à réaliser : {task}\n\nContexte supplémentaire : {json.dumps(context, ensure_ascii=False)}"
        )

        try:
            plan = json.loads(plan_response)
        except json.JSONDecodeError:
            start = plan_response.find("{")
            end = plan_response.rfind("}") + 1
            if start != -1 and end > start:
                plan = json.loads(plan_response[start:end])
            else:
                return {
                    "response": plan_response,
                    "metadata": {"raw": True},
                }

        if "direct_response" in plan:
            return {
                "response": plan["direct_response"],
                "metadata": {"plan": plan},
            }

        results = []
        for step in plan.get("plan", []):
            agent_name = step["agent"]
            sub_task = step["task"]
            sub_context = step.get("context", {})

            logger.info(f"[Orchestrateur] Étape: {agent_name} -> {sub_task[:60]}...")
            result = self.delegate(agent_name, sub_task, sub_context)
            results.append({
                "agent": agent_name,
                "task": sub_task,
                "result": result.content,
                "status": result.type.value,
            })

        if plan.get("synthesis_needed") and results:
            synthesis = self._synthesize(task, results)
        else:
            synthesis = "\n\n".join(
                f"**[{r['agent']}]** {r['result']}" for r in results
            )

        return {
            "response": synthesis,
            "metadata": {"plan": plan, "results": results},
        }

    def _synthesize(self, original_task: str, results: list[dict]) -> str:
        """Synthétise les résultats des sous-agents en une réponse cohérente."""
        results_text = "\n\n".join(
            f"=== Résultat de {r['agent']} ===\n{r['result']}" for r in results
        )

        synthesis_prompt = (
            f"Tâche originale : {original_task}\n\n"
            f"Résultats des sous-agents :\n{results_text}\n\n"
            "Synthétise ces résultats en une réponse claire, structurée et complète."
        )

        return self.call_llm(synthesis_prompt)

    def run(self, task: str, context: dict[str, Any] | None = None) -> str:
        """Point d'entrée principal pour exécuter une tâche."""
        logger.info(f"[Orchestrateur] Nouvelle tâche: {task[:80]}...")
        msg = Message(
            type=MessageType.TASK,
            content=task,
            sender="user",
            receiver=self.name,
            data=context or {},
        )
        result = self.handle_message(msg)
        return result.content
