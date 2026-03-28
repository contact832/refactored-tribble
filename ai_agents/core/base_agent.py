"""Classe de base pour tous les agents IA."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from anthropic import Anthropic

from ai_agents.core.messages import Message, MessageType

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Agent de base avec capacité d'appel à Claude API."""

    def __init__(
        self,
        name: str,
        role: str,
        model: str = "claude-sonnet-4-20250514",
        system_prompt: str | None = None,
    ):
        self.name = name
        self.role = role
        self.model = model
        self.system_prompt = system_prompt or f"Tu es {name}, un agent IA spécialisé en {role}."
        self.client = Anthropic()
        self.conversation_history: list[dict[str, str]] = []
        self.sub_agents: dict[str, BaseAgent] = {}
        self._message_log: list[Message] = []

    def add_sub_agent(self, agent: BaseAgent) -> None:
        """Ajoute un sous-agent à cet agent."""
        self.sub_agents[agent.name] = agent
        logger.info("[%s] Sous-agent ajoute : %s (%s)", self.name, agent.name, agent.role)

    def remove_sub_agent(self, name: str) -> None:
        """Retire un sous-agent."""
        self.sub_agents.pop(name, None)

    def delegate(self, agent_name: str, task: str, context: dict[str, Any] | None = None) -> Message:
        """Délègue une tâche à un sous-agent."""
        if agent_name not in self.sub_agents:
            return Message(
                type=MessageType.ERROR,
                content=f"Sous-agent '{agent_name}' introuvable.",
                sender=self.name,
                receiver=agent_name,
            )

        msg = Message(
            type=MessageType.DELEGATION,
            content=task,
            sender=self.name,
            receiver=agent_name,
            data=context or {},
        )
        self._message_log.append(msg)

        sub_agent = self.sub_agents[agent_name]
        logger.info("[%s] Delegation a %s: %s...", self.name, agent_name, task[:80])
        result = sub_agent.handle_message(msg)
        self._message_log.append(result)
        return result

    def call_llm(self, prompt: str, use_history: bool = False) -> str:
        """Appelle Claude API avec le prompt donné."""
        messages = []
        if use_history:
            messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": prompt})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=messages,
        )

        assistant_reply = response.content[0].text

        if use_history:
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    def handle_message(self, message: Message) -> Message:
        """Traite un message entrant et retourne une réponse."""
        logger.info("[%s] Message recu de %s: %s...", self.name, message.sender, message.content[:80])
        try:
            result = self.process(message.content, message.data)
            return message.reply(
                content=result["response"],
                data=result.get("metadata", {}),
                msg_type=MessageType.RESULT,
            )
        except Exception as e:
            logger.error("[%s] Erreur: %s", self.name, e)
            return message.reply(
                content=f"Erreur dans {self.name}: {str(e)}",
                msg_type=MessageType.ERROR,
            )

    @abstractmethod
    def process(self, task: str, context: dict[str, Any]) -> dict[str, Any]:
        """Traite une tâche. Doit retourner {'response': str, 'metadata': dict}."""
        ...

    def get_status(self) -> dict[str, Any]:
        """Retourne le statut de l'agent et de ses sous-agents."""
        return {
            "name": self.name,
            "role": self.role,
            "model": self.model,
            "sub_agents": {
                name: agent.get_status() for name, agent in self.sub_agents.items()
            },
            "messages_processed": len(self._message_log),
        }
