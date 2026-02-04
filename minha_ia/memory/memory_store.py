"""Sistema simples de memória persistente."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class SimpleMemory:
    """Memória baseada em arquivo JSON."""

    path: Path
    interactions: List[dict] = field(default_factory=list)

    def load(self) -> None:
        """Carrega interações do disco se existirem."""
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.interactions = data.get("interactions", [])

    def save(self) -> None:
        """Salva interações no disco."""
        payload = {"interactions": self.interactions}
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_interaction(self, user: str, assistant: str) -> None:
        """Registra nova interação."""
        self.interactions.append({"user": user, "assistant": assistant})

    def recall_recent(self, limit: int = 5) -> List[dict]:
        """Retorna as interações mais recentes."""
        if limit <= 0:
            return []
        return self.interactions[-limit:]
