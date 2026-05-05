#!/usr/bin/env python3
"""Minimal local HTTP receiver for the Pico 2 W IoT hands-on."""

from __future__ import annotations

import argparse
import html
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from typing import Any
from urllib.parse import parse_qs, urlparse


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def html_page(title: str, body: str) -> bytes:
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --card: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --line: #d1d5db;
      --ok: #0f766e;
      --bad: #b91c1c;
      --accent: #1d4ed8;
    }}
    body {{
      margin: 0;
      padding: 24px;
      background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{
      max-width: 1100px;
      margin: 0 auto;
    }}
    .hero {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 20px 24px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
      margin-bottom: 20px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
    }}
    p, li {{
      line-height: 1.55;
    }}
    .meta {{
      color: var(--muted);
      font-size: 14px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin: 18px 0 8px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px 16px;
    }}
    .label {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .value {{
      font-size: 22px;
      font-weight: 700;
      margin-top: 4px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid #e5e7eb;
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }}
    th {{
      background: #eff6ff;
      color: #1e3a8a;
      font-weight: 700;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    .ok {{
      color: var(--ok);
      font-weight: 700;
    }}
    .bad {{
      color: var(--bad);
      font-weight: 700;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    a {{
      color: var(--accent);
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
"""
    return page.encode("utf-8")


@dataclass
class ServerConfig:
    host: str
    port: int
    log_path: Path
    allowed_paths: list[str]
    dashboard_limit: int
    expected_token: str | None = None


def parse_args() -> ServerConfig:
    parser = argparse.ArgumentParser(
        description="Minimal local receiver server for the Pico 2 W hands-on."
    )
    parser.add_argument("--host", default=os.getenv("RECEIVER_HOST", "0.0.0.0"))
    parser.add_argument(
        "--port", type=int, default=int(os.getenv("RECEIVER_PORT", "5000"))
    )
    parser.add_argument(
        "--log-path",
        default=os.getenv("RECEIVER_LOG_PATH", "received.log"),
        help="JSONL log file path",
    )
    parser.add_argument(
        "--allowed-paths",
        default=os.getenv("RECEIVER_ALLOWED_PATHS", "/ingest"),
        help="Comma-separated list of accepted POST paths",
    )
    parser.add_argument(
        "--dashboard-limit",
        type=int,
        default=int(os.getenv("RECEIVER_DASHBOARD_LIMIT", "20")),
    )
    parser.add_argument(
        "--expected-token",
        default=os.getenv("RECEIVER_EXPECTED_TOKEN"),
        help="Optional token checked against X-Device-Token",
    )
    args = parser.parse_args()

    paths = [p.strip() for p in args.allowed_paths.split(",") if p.strip()]
    if not paths:
        paths = ["/ingest"]

    return ServerConfig(
        host=args.host,
        port=args.port,
        log_path=Path(args.log_path),
        allowed_paths=paths,
        dashboard_limit=max(1, args.dashboard_limit),
        expected_token=args.expected_token,
    )


def read_log_entries(log_path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []

    entries: list[dict[str, Any]] = []
    with log_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                entries.append(
                    {
                        "time": now_iso(),
                        "status": "invalid-log-line",
                        "raw": line,
                    }
                )
    if limit is None:
        return entries
    return entries[-limit:]


class ReceiverHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], config: ServerConfig):
        self.config = config
        super().__init__(server_address, ReceiverHandler)


class ReceiverHandler(BaseHTTPRequestHandler):
    server: ReceiverHTTPServer
    server_version = "PicoReceiver/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{stamp}] {self.address_string()} {format % args}")

    def _json_response(
        self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html_response(self, title: str, body: str) -> None:
        encoded = html_page(title, body)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _append_log(self, record: dict[str, Any]) -> None:
        log_path = self.server.config.log_path
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _remote_ip(self) -> str:
        return self.client_address[0]

    def _token_ok(self) -> tuple[bool, str | None]:
        expected = self.server.config.expected_token
        provided = self.headers.get("X-Device-Token")
        if not expected:
            return True, provided
        return provided == expected, provided

    def _validate_payload(self, payload: Any) -> tuple[bool, str | None]:
        if not isinstance(payload, dict):
            return False, "body must be a JSON object"

        required = [
            "device_id",
            "seq",
            "uptime_ms",
            "temperature_c",
            "humidity_pct",
            "pressure_hpa",
        ]
        for key in required:
            if key not in payload:
                return False, f"missing required field: {key}"

        if not isinstance(payload["device_id"], str):
            return False, "device_id must be a string"
        if not isinstance(payload["seq"], int):
            return False, "seq must be an integer"
        if not isinstance(payload["uptime_ms"], int):
            return False, "uptime_ms must be an integer"

        numeric_keys = ["temperature_c", "humidity_pct", "pressure_hpa"]
        for key in numeric_keys:
            if not isinstance(payload[key], (int, float)):
                return False, f"{key} must be numeric"

        return True, None

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._json_response(
                {
                    "ok": True,
                    "message": "receiver is healthy",
                    "server_time": now_iso(),
                    "allowed_paths": self.server.config.allowed_paths,
                }
            )
            return

        if parsed.path == "/api/messages":
            params = parse_qs(parsed.query)
            device_id = params.get("device_id", [None])[0]
            status = params.get("status", [None])[0]
            limit = params.get("limit", [str(self.server.config.dashboard_limit)])[0]
            try:
                limit_n = max(1, int(limit))
            except ValueError:
                limit_n = self.server.config.dashboard_limit

            entries = read_log_entries(self.server.config.log_path)
            if device_id:
                entries = [e for e in entries if e.get("device_id") == device_id]
            if status:
                entries = [e for e in entries if e.get("status") == status]
            entries = entries[-limit_n:]
            self._json_response(
                {
                    "ok": True,
                    "count": len(entries),
                    "messages": entries,
                }
            )
            return

        if parsed.path == "/dashboard":
            params = parse_qs(parsed.query)
            device_id = params.get("device_id", [None])[0]
            status_filter = params.get("status", [None])[0]
            entries = read_log_entries(self.server.config.log_path)
            if device_id:
                entries = [e for e in entries if e.get("device_id") == device_id]
            if status_filter:
                entries = [e for e in entries if e.get("status") == status_filter]
            entries = entries[-self.server.config.dashboard_limit :]
            body = self._dashboard_body(entries, device_id, status_filter)
            self._html_response("Pico Receiver Dashboard", body)
            return

        self._json_response(
            {"ok": False, "error": "not found"}, status=HTTPStatus.NOT_FOUND
        )

    def _dashboard_body(
        self,
        entries: list[dict[str, Any]],
        device_id: str | None,
        status_filter: str | None,
    ) -> str:
        accepted = sum(1 for e in entries if e.get("status") == "accepted")
        rejected = sum(1 for e in entries if e.get("status") != "accepted")
        last_seen = entries[-1].get("time", "-") if entries else "-"

        filter_parts = []
        if device_id:
            filter_parts.append(f"device_id={html.escape(device_id)}")
        if status_filter:
            filter_parts.append(f"status={html.escape(status_filter)}")
        filter_text = ", ".join(filter_parts) if filter_parts else "none"

        rows = []
        for entry in reversed(entries):
            payload = entry.get("payload", {})
            status = str(entry.get("status", "-"))
            status_class = "ok" if status == "accepted" else "bad"
            rows.append(
                "<tr>"
                f"<td>{html.escape(str(entry.get('time', '-')))}</td>"
                f"<td><code>{html.escape(str(entry.get('device_id', '-')))}</code></td>"
                f"<td>{html.escape(str(entry.get('remote_addr', '-')))}</td>"
                f"<td>{html.escape(str(payload.get('seq', '-')))}</td>"
                f"<td>{html.escape(str(payload.get('temperature_c', '-')))}</td>"
                f"<td>{html.escape(str(payload.get('humidity_pct', '-')))}</td>"
                f"<td>{html.escape(str(payload.get('pressure_hpa', '-')))}</td>"
                f"<td class=\"{status_class}\">{html.escape(status)}</td>"
                f"<td><code>{html.escape(json.dumps(payload, ensure_ascii=False))}</code></td>"
                "</tr>"
            )

        if not rows:
            rows.append(
                "<tr><td colspan=\"9\">No messages yet. Send a POST from the Pico and refresh this page.</td></tr>"
            )

        allowed_paths = ", ".join(self.server.config.allowed_paths)
        api_example = "/api/messages?limit=5"
        return f"""
<section class="hero">
  <h1>Pico Receiver Dashboard</h1>
  <p>Read-only view of the latest received messages for the IoT hands-on.</p>
  <div class="meta">Allowed POST paths: <code>{html.escape(allowed_paths)}</code></div>
  <div class="meta">Filters: {filter_text}</div>
  <div class="grid">
    <div class="card"><div class="label">Recent entries</div><div class="value">{len(entries)}</div></div>
    <div class="card"><div class="label">Accepted</div><div class="value">{accepted}</div></div>
    <div class="card"><div class="label">Rejected</div><div class="value">{rejected}</div></div>
    <div class="card"><div class="label">Last seen</div><div class="value" style="font-size:16px;">{html.escape(str(last_seen))}</div></div>
  </div>
  <p class="meta">JSON API: <a href="{api_example}"><code>{api_example}</code></a></p>
</section>
<table>
  <thead>
    <tr>
      <th>Time</th>
      <th>Device</th>
      <th>Source IP</th>
      <th>Seq</th>
      <th>Temp C</th>
      <th>Humidity %</th>
      <th>Pressure hPa</th>
      <th>Status</th>
      <th>Payload</th>
    </tr>
  </thead>
  <tbody>
    {''.join(rows)}
  </tbody>
</table>
"""

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path not in self.server.config.allowed_paths:
            self._json_response(
                {"ok": False, "error": "path not allowed"},
                status=HTTPStatus.NOT_FOUND,
            )
            return

        token_ok, provided_token = self._token_ok()
        if not token_ok:
            self._json_response(
                {"ok": False, "error": "invalid device token"},
                status=HTTPStatus.FORBIDDEN,
            )
            return

        content_length = self.headers.get("Content-Length")
        if not content_length:
            self._json_response(
                {"ok": False, "error": "missing Content-Length"},
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        try:
            raw = self.rfile.read(int(content_length))
        except ValueError:
            self._json_response(
                {"ok": False, "error": "invalid Content-Length"},
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json_response(
                {"ok": False, "error": "body must be valid JSON"},
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        valid, error = self._validate_payload(payload)
        record = {
            "time": now_iso(),
            "remote_addr": self._remote_ip(),
            "device_id": payload.get("device_id", "-")
            if isinstance(payload, dict)
            else "-",
            "status": "accepted" if valid else "rejected",
            "path": parsed.path,
            "token": provided_token,
            "payload": payload,
        }
        self._append_log(record)

        if not valid:
            self._json_response(
                {"ok": False, "error": error},
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        self._json_response(
            {
                "ok": True,
                "message": "accepted",
                "server_time": now_iso(),
                "received_path": parsed.path,
            }
        )


def main() -> None:
    config = parse_args()
    config.log_path.parent.mkdir(parents=True, exist_ok=True)
    server = ReceiverHTTPServer((config.host, config.port), config)
    print("Minimal Pico receiver server starting")
    print(f"listen:   http://{config.host}:{config.port}")
    print(f"health:   http://127.0.0.1:{config.port}/health")
    print(f"dashboard:http://127.0.0.1:{config.port}/dashboard")
    print(f"log path: {config.log_path}")
    print(f"paths:    {', '.join(config.allowed_paths)}")
    if config.expected_token:
        print("token:    enabled")
    else:
        print("token:    disabled")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
