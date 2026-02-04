# minha-ia

IA modular em Python com núcleo cognitivo e memória básica.

## Visão geral da arquitetura

```
minha-ia/
├── data/                 # armazenamento simples de memória
├── minha_ia/
│   ├── core/             # núcleo de raciocínio
│   ├── io/               # entrada/saída via terminal
│   ├── memory/           # sistema de memória
│   ├── agent.py          # orquestração dos módulos
│   └── main.py           # ponto de entrada
└── README.md
```

### Módulos

- **`minha_ia/core/reasoning.py`**
  - Núcleo de raciocínio baseado em regras simples.
  - Interpreta a intenção, usa memória recente e compõe respostas.
- **`minha_ia/memory/memory_store.py`**
  - Memória persistente em JSON.
  - Armazena e recupera interações recentes.
- **`minha_ia/io/terminal_io.py`**
  - Interface de terminal para entrada/saída.
- **`minha_ia/agent.py`**
  - Orquestra os módulos de memória e raciocínio.
  - Registra cada interação na memória.
- **`minha_ia/main.py`**
  - Loop principal da aplicação.

## Como executar

1. Garanta que você tem Python 3.10+ instalado.
2. Execute no terminal:

```bash
python -m minha_ia.main
```

A memória é salva em `data/memory.json` automaticamente.

## Como evoluir

- **Aprimorar o raciocínio**: crie novas heurísticas, adicione modelos estatísticos ou conecte APIs.
- **Memória avançada**: substitua o JSON por banco de dados ou embeddings.
- **Interfaces adicionais**: crie uma API HTTP ou interface web reutilizando `Agent`.
- **Observabilidade**: registre logs estruturados das interações.

## Exemplo de interação

```
IA: Sistema iniciado. Digite 'sair' para encerrar.
Você: Olá
IA: Olá! Como posso ajudar hoje?
[contexto] Entrada recebida: Olá | Memória recente: Sem registros ainda | Intenção: Cumprimento
```
