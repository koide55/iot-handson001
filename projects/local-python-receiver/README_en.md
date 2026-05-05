# Local Python Receiver Server

This directory contains a minimal Python server that receives `HTTP POST` messages from a `Raspberry Pi Pico 2 W`.

It is designed for classroom use and depends only on the Python standard library.

## Features

- `POST /ingest`
  - receive JSON messages from the Pico
- `GET /health`
  - basic health check
- `GET /dashboard`
  - read-only dashboard for received logs
- `GET /api/messages`
  - small JSON API for recent messages
- `received.log`
  - stored as JSONL, one JSON object per line

## Files

- [server.py](server.py)

## Run

```bash
cd /Users/koide/Documents/Playground/iot-handson/projects/local-python-receiver
python3 server.py
```

Default URLs:

- ingest endpoint: `http://<server-ip>:5000/ingest`
- health check: `http://127.0.0.1:5000/health`
- dashboard: `http://127.0.0.1:5000/dashboard`

## Common Examples

### Change the port

```bash
python3 server.py --port 5001
```

### Change the log path

```bash
python3 server.py --log-path logs/received.log
```

### Allow multiple paths

```bash
python3 server.py --allowed-paths /ingest/a,/ingest/b,/ingest/c
```

### Require a token

```bash
python3 server.py --expected-token classroom-token-001
```

## Required JSON

At minimum, the following keys are required.

```json
{
  "device_id": "pico2w-01",
  "seq": 1,
  "uptime_ms": 12345,
  "temperature_c": 24.8,
  "humidity_pct": 51.2,
  "pressure_hpa": 1008.4
}
```

## Dashboard

The dashboard is read-only.

It shows recent entries including:

- `device_id`
- source IP
- `seq`
- temperature, humidity, pressure
- `status`
- raw JSON payload

Learners can open `http://<server-ip>:5000/dashboard` in a browser to confirm that their messages arrived.

## API

### `GET /health`

Example response:

```json
{
  "ok": true,
  "message": "receiver is healthy",
  "server_time": "2026-05-05T10:00:00+09:00",
  "allowed_paths": [
    "/ingest"
  ]
}
```

### `GET /api/messages`

Query parameters:

- `limit`
- `device_id`
- `status`

Examples:

```text
/api/messages?limit=5
/api/messages?device_id=pico2w-01
/api/messages?status=accepted
```

## Related Slides

- [../../slides/lecture05_mtd_local_post_spec_en.md](../../slides/lecture05_mtd_local_post_spec_en.md)
