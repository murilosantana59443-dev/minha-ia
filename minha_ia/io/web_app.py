"""Interface web simples para a IA."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html import escape
from urllib.parse import parse_qs

from minha_ia.agent import Agent
from minha_ia.core.language import LanguageCatalog


class WebApp:
    """Servidor web minimalista para interagir com a IA."""

    def __init__(
        self,
        agent: Agent,
        language_catalog: LanguageCatalog,
        host: str = "0.0.0.0",
        port: int = 8000,
    ) -> None:
        self.agent = agent
        self.language_catalog = language_catalog
        self.host = host
        self.port = port
        self.selected_language = "pt"
        self.last_user_message = ""
        self.last_assistant_message = ""

    def run(self) -> None:
        """Inicia o servidor web."""
        app = self

        class Handler(BaseHTTPRequestHandler):
            def _render(self, notice: str = "") -> bytes:
                profiles = app.language_catalog.list_profiles()
                options = "\n".join(
                    (
                        f"<option value=\"{profile.code}\""
                        f"{' selected' if profile.code == app.selected_language else ''}>"
                        f"{profile.name} - {profile.description}"
                        "</option>"
                    )
                    for profile in profiles
                )
                history_items = "\n".join(
                    (
                        f"<li><strong>Você:</strong> {escape(item['user'])}<br>"
                        f"<strong>IA:</strong> {escape(item['assistant'])}</li>"
                    )
                    for item in app.agent.memory.recall_recent(limit=10)
                )
                greeting = app.language_catalog.get(app.selected_language).greeting
                last_user = escape(app.last_user_message) or "..."
                last_reply = escape(app.last_assistant_message) or "Pronto para conversar!"
                html = f"""
                <!doctype html>
                <html lang=\"pt-br\">
                <head>
                  <meta charset=\"utf-8\" />
                  <title>minha-ia</title>
                  <style>
                    * {{ box-sizing: border-box; }}
                    body {{ font-family: "Inter", Arial, sans-serif; margin: 0; background: #0f172a; color: #e2e8f0; }}
                    header {{ padding: 24px 32px; border-bottom: 1px solid #1e293b; background: #0b1120; }}
                    h1 {{ margin: 0; font-size: 20px; letter-spacing: 0.4px; }}
                    .layout {{ display: grid; grid-template-columns: 280px 1fr; min-height: calc(100vh - 72px); }}
                    .sidebar {{ padding: 24px; border-right: 1px solid #1e293b; background: #0b1120; }}
                    .sidebar h2 {{ margin-top: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; }}
                    .content {{ padding: 32px 40px; }}
                    .chat-card {{ background: #111827; border-radius: 16px; padding: 24px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.45); }}
                    .message {{ padding: 14px 16px; border-radius: 12px; margin-bottom: 12px; }}
                    .message.user {{ background: #1e293b; }}
                    .message.assistant {{ background: #0f766e; }}
                    label {{ display: block; margin-top: 16px; font-weight: 600; color: #cbd5f5; }}
                    select, input {{ width: 100%; padding: 10px 12px; margin-top: 8px; border-radius: 10px; border: 1px solid #1e293b; background: #0f172a; color: #e2e8f0; }}
                    textarea {{ width: 100%; padding: 12px; margin-top: 8px; border-radius: 10px; border: 1px solid #1e293b; background: #0f172a; color: #e2e8f0; min-height: 120px; resize: vertical; }}
                    button {{ margin-top: 16px; padding: 12px 18px; background: #22c55e; color: #0b1120; border: none; border-radius: 10px; font-weight: 600; cursor: pointer; }}
                    button:hover {{ background: #16a34a; }}
                    ul {{ padding-left: 18px; color: #cbd5f5; }}
                    .hint {{ color: #94a3b8; font-size: 14px; margin-top: 8px; }}
                    .greeting {{ font-size: 18px; margin-bottom: 16px; }}
                    .composer {{ margin-top: 24px; }}
                    .notice {{ color: #facc15; margin-top: 12px; }}
                  </style>
                </head>
                <body>
                  <header>
                    <h1>minha-ia</h1>
                  </header>
                  <div class=\"layout\">
                    <aside class=\"sidebar\">
                      <h2>Configurações</h2>
                      <form method=\"post\" action=\"/send\">
                        <label for=\"language\">Idioma</label>
                        <select id=\"language\" name=\"language\">
                          {options}
                        </select>
                        <p class=\"hint\">Interface inspirada no ChatGPT para testes rápidos.</p>
                      </form>
                    </aside>
                    <main class=\"content\">
                      <div class=\"chat-card\">
                        <div class=\"greeting\">{escape(greeting)}</div>
                        <div class=\"message user\"><strong>Você:</strong> {last_user}</div>
                        <div class=\"message assistant\"><strong>IA:</strong> {last_reply}</div>
                        <form class=\"composer\" method=\"post\" action=\"/send\">
                          <input type=\"hidden\" name=\"language\" value=\"{app.selected_language}\" />
                          <label for=\"message\">Digite seu comando</label>
                          <textarea id=\"message\" name=\"message\" placeholder=\"Escreva aqui...\"></textarea>
                          <button type=\"submit\">Enviar</button>
                          {f'<div class=\"notice\">{escape(notice)}</div>' if notice else ''}
                        </form>
                        <h2>Histórico recente</h2>
                        <ul>
                          {history_items}
                        </ul>
                      </div>
                    </main>
                  </div>
                </body>
                </html>
                """
                return html.encode("utf-8")

            def _send_response(self, content: bytes) -> None:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            def do_GET(self) -> None:
                content = self._render()
                self._send_response(content)

            def do_POST(self) -> None:
                if self.path != "/send":
                    self.send_error(404)
                    return
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length).decode("utf-8")
                data = parse_qs(body)
                language = data.get("language", [app.selected_language])[0]
                app.selected_language = language or app.selected_language
                message = data.get("message", [""])[0].strip()
                if message:
                    response = app.agent.handle_input(message)
                    app.last_user_message = message
                    app.last_assistant_message = response.answer
                    feedback = ""
                else:
                    feedback = "Digite uma mensagem para continuar."
                content = self._render(notice=feedback)
                self._send_response(content)

            def log_message(self, format: str, *args: object) -> None:
                return

        server = ThreadingHTTPServer((self.host, self.port), Handler)
        server.serve_forever()
