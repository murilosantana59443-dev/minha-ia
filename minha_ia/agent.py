"""Orquestra os módulos da IA."""
from __future__ import annotations

from dataclasses import dataclass

from minha_ia.core.reasoning import ReasoningCore
from minha_ia.memory.memory_store import SimpleMemory


@dataclass
class AgentResponse:
    """Resposta completa produzida pelo agente."""

    answer: str
    context_summary: str


class Agent:
    """Agente modular que integra raciocínio e memória."""

    def __init__(self, memory: SimpleMemory, reasoning: ReasoningCore) -> None:
        self.memory = memory
        self.reasoning = reasoning

    def handle_input(self, user_input: str) -> AgentResponse:
        """Processa a entrada do usuário e gera uma resposta."""
        recent_context = self.memory.recall_recent(limit=5)
        response = self.reasoning.respond(user_input, recent_context)
        self.memory.add_interaction(user_input, response.answer)
        self.memory.save()
        return response
