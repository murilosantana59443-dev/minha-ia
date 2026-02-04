"""Ponto de entrada da aplicação."""
from __future__ import annotations

from pathlib import Path

from minha_ia.agent import Agent
from minha_ia.core.reasoning import ReasoningCore
from minha_ia.io.terminal_io import TerminalIO
from minha_ia.memory.memory_store import SimpleMemory


def run() -> None:
    """Executa loop principal."""
    memory = SimpleMemory(path=Path("data/memory.json"))
    memory.load()
    reasoning = ReasoningCore()
    agent = Agent(memory=memory, reasoning=reasoning)
    terminal = TerminalIO()

    terminal.display("Sistema iniciado. Digite 'sair' para encerrar.")
    while True:
        user_input = terminal.prompt()
        if user_input.strip().lower() in {"sair", "exit", "quit"}:
            terminal.display("Até mais! Memória salva.")
            break
        response = agent.handle_input(user_input)
        terminal.display(response.answer)
        terminal.display_context(response.context_summary)


if __name__ == "__main__":
    run()
