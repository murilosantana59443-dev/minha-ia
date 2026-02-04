"""Núcleo de raciocínio simples para a IA."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from minha_ia.agent import AgentResponse


@dataclass
class Thought:
    """Representa uma ideia intermediária do raciocínio."""

    title: str
    details: str


class ReasoningCore:
    """Implementa um raciocínio simples baseado em regras."""

    def __init__(self) -> None:
        self.principles = [
            "Ser claro e objetivo",
            "Usar memória recente quando útil",
            "Sugerir próximos passos",
        ]

    def respond(self, user_input: str, memory: Iterable[dict]) -> AgentResponse:
        """Gera uma resposta usando memória recente e heurísticas."""
        normalized = user_input.strip().lower()
        thoughts: List[Thought] = [
            Thought("Entrada recebida", user_input.strip()),
            Thought("Memória recente", self._summarize_memory(memory)),
            Thought("Intenção", self._infer_intent(normalized)),
        ]
        answer = self._compose_answer(normalized, thoughts)
        context_summary = " | ".join(f"{thought.title}: {thought.details}" for thought in thoughts)
        return AgentResponse(answer=answer, context_summary=context_summary)

    def _infer_intent(self, normalized: str) -> str:
        if any(keyword in normalized for keyword in ("oi", "olá", "hello", "hey")):
            return "Cumprimento"
        if "memória" in normalized:
            return "Consulta sobre memória"
        if "ajuda" in normalized or "help" in normalized:
            return "Pedido de ajuda"
        return "Diálogo geral"

    def _summarize_memory(self, memory: Iterable[dict]) -> str:
        entries = list(memory)
        if not entries:
            return "Sem registros ainda"
        last = entries[-1]
        return f"Última interação: '{last.get('user')}' -> '{last.get('assistant')}'"

    def _compose_answer(self, normalized: str, thoughts: List[Thought]) -> str:
        if "memória" in normalized:
            return (
                "Aqui está o que lembro das últimas interações. "
                "Se quiser, posso limpar ou expandir a memória."
            )
        if any(keyword in normalized for keyword in ("oi", "olá", "hello", "hey")):
            return "Olá! Como posso ajudar hoje?"
        if "ajuda" in normalized or "help" in normalized:
            return (
                "Posso responder perguntas, registrar suas interações e sugerir próximos passos. "
                "Pergunte o que quiser!"
            )
        summary = next((t.details for t in thoughts if t.title == "Memória recente"), "")
        return (
            "Entendi. Posso ajudar a explorar essa ideia. "
            f"{summary} "
            "Quer aprofundar em algum ponto específico?"
        )
