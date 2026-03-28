#!/usr/bin/env python3
"""Point d'entrée principal du système d'agents IA.

Exemple d'utilisation :
    python main.py "Crée une API REST en Python pour gérer des utilisateurs"
    python main.py --interactive
"""

from __future__ import annotations

import argparse
import logging
import sys

from ai_agents.core.orchestrator import OrchestratorAgent
from ai_agents.agents.research_agent import ResearchAgent
from ai_agents.agents.code_agent import CodeAgent
from ai_agents.agents.writing_agent import WritingAgent
from ai_agents.agents.analysis_agent import AnalysisAgent
from ai_agents.agents.commercial_agent import CommercialAgent
from ai_agents.agents.accounting_agent import AccountingAgent
from ai_agents.agents.social_media_agent import SocialMediaAgent
from ai_agents.agents.translator_agent import TranslatorAgent
from ai_agents.agents.logistics_agent import LogisticsAgent
from ai_agents.agents.legal_agent import LegalAgent
from ai_agents.company_profile import get_agent_company_prompt


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def create_agent_system(model: str = "claude-sonnet-4-20250514") -> OrchestratorAgent:
    """Crée et configure le système d'agents avec tous les sous-agents."""
    orchestrator = OrchestratorAgent(model=model)

    # Ajout des sous-agents spécialisés
    orchestrator.add_sub_agent(ResearchAgent(model=model))
    orchestrator.add_sub_agent(CodeAgent(model=model))
    orchestrator.add_sub_agent(WritingAgent(model=model))
    orchestrator.add_sub_agent(AnalysisAgent(model=model))
    orchestrator.add_sub_agent(CommercialAgent(model=model))
    orchestrator.add_sub_agent(AccountingAgent(model=model))
    orchestrator.add_sub_agent(SocialMediaAgent(model=model))
    orchestrator.add_sub_agent(TranslatorAgent(model=model))
    orchestrator.add_sub_agent(LogisticsAgent(model=model))
    orchestrator.add_sub_agent(LegalAgent(model=model))

    # Charger les infos AMB Transports 69 dans chaque agent
    _load_company_knowledge(orchestrator)

    return orchestrator


def _load_company_knowledge(orchestrator: OrchestratorAgent) -> None:
    """Charge la base de connaissances AMB Transports 69 dans tous les agents."""
    company_prompt = get_agent_company_prompt("")

    # Injecter dans le system prompt de chaque sous-agent
    for name, agent in orchestrator.sub_agents.items():
        agent.system_prompt = agent.system_prompt + "\n\n" + company_prompt
        logging.info("[Memoire] %s connait AMB Transports 69", name)

    # L'orchestrateur aussi
    orchestrator._company_context = company_prompt
    logging.info("[Memoire] Base de connaissances AMB Transports 69 chargee pour %d agents", len(orchestrator.sub_agents))


def interactive_mode(orchestrator: OrchestratorAgent) -> None:
    """Mode interactif : boucle de conversation avec l'utilisateur."""
    print("\n🤖 Système d'Agents IA")
    print("=" * 50)
    print("Agents disponibles :")
    for name, agent in orchestrator.sub_agents.items():
        print(f"  • {name} — {agent.role}")
    print(f"\nTapez 'quit' pour quitter, 'status' pour voir l'état.\n")

    while True:
        try:
            user_input = input("📝 Votre tâche > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAu revoir !")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Au revoir !")
            break
        if user_input.lower() == "status":
            import json
            print(json.dumps(orchestrator.get_status(), indent=2, ensure_ascii=False))
            continue

        print(f"\n⏳ Traitement en cours...\n")
        result = orchestrator.run(user_input)
        print(f"\n{'=' * 50}")
        print(f"📋 Résultat :\n")
        print(result)
        print(f"\n{'=' * 50}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Système d'Agents IA avec sous-agents")
    parser.add_argument("task", nargs="?", help="Tâche à exécuter (mode direct)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Mode interactif")
    parser.add_argument("--model", "-m", default="claude-sonnet-4-20250514", help="Modèle Claude à utiliser")
    parser.add_argument("--verbose", "-v", action="store_true", help="Logs détaillés")
    args = parser.parse_args()

    setup_logging(args.verbose)
    orchestrator = create_agent_system(model=args.model)

    if args.interactive or not args.task:
        interactive_mode(orchestrator)
    else:
        result = orchestrator.run(args.task)
        print(result)


if __name__ == "__main__":
    main()
