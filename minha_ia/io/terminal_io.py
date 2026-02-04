"""Interface de terminal para a IA."""
from __future__ import annotations


class TerminalIO:
    """Gerencia interação com o usuário via terminal."""

    def display_languages(self, languages: list[dict[str, str]]) -> None:
        print("Idiomas disponíveis:")
        for language in languages:
            print(
                f"- {language['code']}: {language['name']} "
                f"({language['description']})"
            )

    def prompt(self) -> str:
        return input("Você: ")

    def prompt_language(self) -> str:
        return input("Escolha o idioma (código): ").strip().lower()

    def display(self, message: str) -> None:
        print(f"IA: {message}")

    def display_context(self, context: str) -> None:
        print(f"[contexto] {context}")
