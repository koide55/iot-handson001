# ローカル Python 受信サーバ

このディレクトリには、`Raspberry Pi Pico 2 W` からの `HTTP POST` を受け取る最小の Python サーバを置いている。

授業用途を意識して、**標準ライブラリだけで動く** ようにしている。

## 含まれる機能

- `POST /ingest`
  - Pico からの JSON を受信する
- `GET /health`
  - 動作確認用
- `GET /dashboard`
  - 受信ログの閲覧専用ダッシュボード
- `GET /api/messages`
  - 最新ログを JSON で返す簡易 API
- `received.log`
  - 1 行 1 JSON の JSONL 形式で保存

## ファイル

- [server.py](server.py)

## 起動方法

```bash
cd /Users/koide/Documents/Playground/iot-handson/projects/local-python-receiver
python3 server.py
```

起動すると、既定では次の URL を使う。

- 受信先: `http://<server-ip>:5000/ingest`
- ヘルスチェック: `http://127.0.0.1:5000/health`
- ダッシュボード: `http://127.0.0.1:5000/dashboard`

## よく使う起動例

### ポートを変える

```bash
python3 server.py --port 5001
```

### ログ保存先を変える

```bash
python3 server.py --log-path logs/received.log
```

### 複数パスを許可する

```bash
python3 server.py --allowed-paths /ingest/a,/ingest/b,/ingest/c
```

### トークンを必須にする

```bash
python3 server.py --expected-token classroom-token-001
```

## 受信する JSON

最低限、次のキーが必要である。

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

## ダッシュボード

ダッシュボードは **閲覧専用** である。

- 最新 20 件程度のログを表示する
- `device_id`
- 送信元 IP
- `seq`
- 温度、湿度、気圧
- `status`
- JSON ペイロード

受講生は、ブラウザで `http://<server-ip>:5000/dashboard` を開くことで、自分の送信が届いたか確認できる。

## API

### `GET /health`

返り値の例:

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

クエリ:

- `limit`
- `device_id`
- `status`

例:

```text
/api/messages?limit=5
/api/messages?device_id=pico2w-01
/api/messages?status=accepted
```

## 関連資料

- [../../slides/lecture05_mtd_local_post_spec.md](../../slides/lecture05_mtd_local_post_spec.md)
- [../../slides/lecture05a_path_rotation_design_discussion.md](../../slides/lecture05a_path_rotation_design_discussion.md)
