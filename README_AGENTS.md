# Système d'Agents IA avec Sous-Agents

Architecture multi-agents utilisant Claude API, avec un orchestrateur principal et des sous-agents spécialisés.

## Architecture

```
┌─────────────────────────────────────────┐
│            Orchestrateur                │
│   (analyse, planifie, délègue, synthèse)│
├────────┬────────┬──────────┬────────────┤
│        │        │          │            │
▼        ▼        ▼          ▼            │
Chercheur Développeur Rédacteur Analyste  │
│        │        │          │            │
└────────┴────────┴──────────┴────────────┘
```

## Agents disponibles

| Agent | Rôle |
|-------|------|
| **Orchestrateur** | Coordonne les sous-agents, décompose les tâches, synthétise les résultats |
| **Chercheur** | Recherche et synthèse d'informations |
| **Développeur** | Génération, revue, débogage et refactoring de code |
| **Rédacteur** | Rédaction de contenu (articles, docs, marketing) |
| **Analyste** | Analyse de données, raisonnement logique, recommandations |

## Installation

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="votre-clé-api"
```

## Utilisation

```bash
# Mode interactif
python main.py --interactive

# Mode direct
python main.py "Crée une API REST en Python pour gérer des utilisateurs"

# Avec logs détaillés
python main.py -v "Analyse les avantages de microservices vs monolithe"
```

## Utilisation en tant que bibliothèque

```python
from ai_agents.core.orchestrator import OrchestratorAgent
from ai_agents.agents.research_agent import ResearchAgent
from ai_agents.agents.code_agent import CodeAgent

# Créer l'orchestrateur
orchestrator = OrchestratorAgent()

# Ajouter des sous-agents
orchestrator.add_sub_agent(ResearchAgent())
orchestrator.add_sub_agent(CodeAgent())

# Exécuter une tâche
result = orchestrator.run("Crée un script de web scraping en Python")
print(result)
```

## Créer un sous-agent personnalisé

```python
from ai_agents.core.base_agent import BaseAgent

class MonAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MonAgent",
            role="description du rôle",
            system_prompt="Instructions pour l'agent...",
        )

    def process(self, task, context):
        response = self.call_llm(f"Ma tâche : {task}")
        return {"response": response, "metadata": {}}

# L'ajouter à l'orchestrateur
orchestrator.add_sub_agent(MonAgent())
```
