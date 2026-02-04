"""Ponto de entrada para a interface web."""
from __future__ import annotations

from pathlib import Path

from minha_ia.agent import Agent
from minha_ia.core.language import LanguageCatalog
from minha_ia.core.reasoning import ReasoningCore
from minha_ia.io.web_app import WebApp
from minha_ia.memory.memory_store import SimpleMemory


def run() -> None:
    """Inicializa e executa o servidor web."""
    memory = SimpleMemory(path=Path("data/memory.json"))
    memory.load()
    reasoning = ReasoningCore()
    agent = Agent(memory=memory, reasoning=reasoning)
    language_catalog = LanguageCatalog()

    app = WebApp(agent=agent, language_catalog=language_catalog)
    app.run()


if __name__ == "__main__":
    run()
