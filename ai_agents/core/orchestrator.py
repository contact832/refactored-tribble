"""Agent orchestrateur principal qui coordonne les sous-agents."""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from ai_agents.core.base_agent import BaseAgent
from ai_agents.core.messages import Message, MessageType

logger = logging.getLogger(__name__)

ORCHESTRATOR_SYSTEM_PROMPT = """Tu es le Chef d'orchestre de l'equipe IA d'AMB Transports 69.
Tu coordonnes une equipe de 10 collaborateurs specialises. Tu es AUTONOME et PROACTIF.

TON EQUIPE :
{agents_description}

TON PATRON : Dennis BOATENG, president d'AMB Transports 69.

REGLES D'AUTONOMIE :
1. INTERPRETE les demandes vagues — si Dennis dit "trouve-moi des clients", ne demande PAS de precisions. Lance Fatou en prospection, Mariam en recherche de marche, et Aya pour les emails.
2. MOBILISE PLUSIEURS AGENTS quand c'est pertinent. Une seule demande = souvent 2-3 agents.
3. SOIS CONCRET — chaque tache donnee a un agent doit etre precise et actionnable.
4. PENSE BUSINESS — chaque reponse doit aider AMB Transports 69 a grandir.
5. ANTICIPE — propose des actions supplementaires que Dennis n'a pas demandees mais qui seraient utiles.
6. Ne demande JAMAIS de precisions sauf si c'est vraiment impossible de deviner ce que Dennis veut.

COMMENT DECOMPOSER UNE TACHE :
- "Trouve des clients" → Fatou (strategie prospection) + Mariam (recherche marche) + Aya (emails/pitchs)
- "Occupe-toi de LinkedIn" → Lina (strategie social) + Aya (textes profil) + Sami (analyse positionnement)
- "Fais un devis" → Fatou (devis) + Omar (verification tarifs) + Amina (mentions legales)
- "Optimise mes tournees" → Moussa (logistique) + Omar (couts) + Sami (analyse rentabilite)
- "J'ai un probleme juridique" → Amina (conseil) + Mariam (recherche reglementation)

Reponds UNIQUEMENT avec un JSON valide :
{{
  "plan": [
    {{
      "agent": "<prenom de l'agent>",
      "task": "<tache DETAILLEE et PRECISE pour cet agent, avec tout le contexte necessaire>",
      "context": {{}}
    }}
  ],
  "synthesis_needed": true
}}

Pour un simple bonjour ou question basique :
{{
  "plan": [],
  "direct_response": "<reponse chaleureuse et proactive, en proposant ce que l'equipe peut faire>"
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
            f"Tâche à réaliser : {task}\n\nContexte supplémentaire : {json.dumps(context, ensure_ascii=False)}",
            use_history=False,
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

        steps = plan.get("plan", [])
        results = [None] * len(steps)

        def _run_step(index, step):
            agent_name = self._resolve_agent_name(step["agent"])
            sub_task = step["task"]
            sub_context = step.get("context", {})
            logger.info("[Orchestrateur] Etape parallele %d: %s -> %s...", index + 1, agent_name, sub_task[:60])
            result = self.delegate(agent_name, sub_task, sub_context)
            return index, {
                "agent": agent_name,
                "task": sub_task,
                "result": result.content,
                "status": result.type.value,
            }

        # Lancer tous les agents en parallele
        with ThreadPoolExecutor(max_workers=len(steps) or 1) as executor:
            futures = [executor.submit(_run_step, i, step) for i, step in enumerate(steps)]
            for future in as_completed(futures):
                idx, res = future.result()
                results[idx] = res

        results = [r for r in results if r is not None]

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

    def _resolve_agent_name(self, name: str) -> str:
        """Résout le nom d'un agent même si le LLM retourne un nom approximatif."""
        # Correspondance exacte
        if name in self.sub_agents:
            return name

        # Correspondance insensible à la casse
        name_lower = name.lower().strip()
        for registered_name in self.sub_agents:
            if registered_name.lower() == name_lower:
                return registered_name

        # Correspondance partielle (ex: "Fatou" trouve "Fatou – Commerciale")
        for registered_name in self.sub_agents:
            if name_lower in registered_name.lower() or registered_name.lower() in name_lower:
                return registered_name

        # Correspondance par prénom ou rôle
        for registered_name in self.sub_agents:
            parts = registered_name.replace("–", " ").replace("-", " ").split()
            for part in parts:
                if part.lower() == name_lower:
                    return registered_name

        return name  # Retourne tel quel, delegate() gérera l'erreur

    def _synthesize(self, original_task: str, results: list[dict]) -> str:
        """Synthétise les résultats des sous-agents en une réponse cohérente."""
        results_text = "\n\n".join(
            f"=== Résultat de {r['agent']} ===\n{r['result']}" for r in results
        )

        synthesis_prompt = (
            f"Tache originale de Dennis : {original_task}\n\n"
            f"Resultats de ton equipe :\n{results_text}\n\n"
            "Synthetise ces resultats en UNE reponse claire et structuree pour Dennis.\n"
            "IMPORTANT :\n"
            "- Parle a Dennis directement, tutoie-le\n"
            "- Mentionne quel agent a fait quoi (ex: 'Fatou a prepare...')\n"
            "- Finis TOUJOURS par 'Prochaines etapes recommandees :' avec 2-3 actions concretes\n"
            "- Sois proactif : propose des choses que Dennis n'a pas demandees mais qui seraient utiles\n"
            "- Sois concis mais complet"
        )

        return self.call_llm(synthesis_prompt)

    def run(self, task: str, context: dict[str, Any] | None = None) -> str:
        """Point d'entrée principal pour exécuter une tâche."""
        logger.info("[Orchestrateur] Nouvelle tache: %s...", task[:80])
        msg = Message(
            type=MessageType.TASK,
            content=task,
            sender="user",
            receiver=self.name,
            data=context or {},
        )
        result = self.handle_message(msg)
        return result.content
