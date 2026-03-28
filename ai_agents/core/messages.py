"""Système de messages pour la communication entre agents."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MessageType(Enum):
    """Types de messages échangés entre agents."""
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    STATUS = "status"
    DELEGATION = "delegation"


@dataclass
class Message:
    """Message échangé entre un agent et ses sous-agents."""
    type: MessageType
    content: str
    sender: str
    receiver: str
    data: dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)

    def reply(self, content: str, data: dict[str, Any] | None = None, msg_type: MessageType = MessageType.RESULT) -> Message:
        """Crée un message de réponse."""
        return Message(
            type=msg_type,
            content=content,
            sender=self.receiver,
            receiver=self.sender,
            data=data or {},
            parent_id=self.message_id,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "parent_id": self.parent_id,
            "type": self.type.value,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }
