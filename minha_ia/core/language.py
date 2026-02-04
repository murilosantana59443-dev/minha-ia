"""Perfis de linguagem suportados pela IA."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class LanguageProfile:
    """Representa um idioma disponível e sua descrição."""

    code: str
    name: str
    description: str
    greeting: str


class LanguageCatalog:
    """Catálogo de idiomas e mensagens relacionadas."""

    def __init__(self) -> None:
        self._languages: Dict[str, LanguageProfile] = {
            "pt": LanguageProfile(
                code="pt",
                name="Português",
                description="Ideal para interações naturais em português brasileiro.",
                greeting="Olá! Posso ajudar em português.",
            ),
            "en": LanguageProfile(
                code="en",
                name="English",
                description="Useful for technical discussions and global communication.",
                greeting="Hello! I can help in English.",
            ),
            "es": LanguageProfile(
                code="es",
                name="Español",
                description="Adecuado para conversaciones rápidas en español.",
                greeting="¡Hola! Puedo ayudar en español.",
            ),
        }

    def list_profiles(self) -> List[LanguageProfile]:
        """Retorna a lista de idiomas disponíveis."""
        return list(self._languages.values())

    def get(self, code: str) -> LanguageProfile:
        """Retorna o idioma escolhido ou o padrão."""
        return self._languages.get(code, self._languages["pt"])
