"""Interface de terminal para a IA."""
from __future__ import annotations


class TerminalIO:
    """Gerencia interação com o usuário via terminal."""

    def prompt(self) -> str:
        return input("Você: ")

    def display(self, message: str) -> None:
        print(f"IA: {message}")

    def display_context(self, context: str) -> None:
        print(f"[contexto] {context}")
