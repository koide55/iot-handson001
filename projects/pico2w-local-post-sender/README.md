# Pico 2 W ローカル POST 送信スケッチ

このディレクトリには、`Raspberry Pi Pico 2 W` からローカル Python 受信サーバへ JSON を送る最小スケッチを置いている。

送信先は、[../local-python-receiver/README.md](../local-python-receiver/README.md) の受信サーバを想定している。

## ファイル

- [pico2w-local-post-sender.ino](pico2w-local-post-sender.ino)

## 使うライブラリ

- `Adafruit BMP280 Library`
- `Adafruit AHTX0`

## 使うピン

- `SDA`: `GP4`
- `SCL`: `GP5`

## 最初に変更する場所

スケッチ先頭の次の設定を、自分の環境に合わせて書き換える。

- `WIFI_SSID`
- `WIFI_PASSWORD`
- `SERVER_HOST`
- `SERVER_PORT`
- `POST_PATH`
- `DEVICE_ID`
- `DEVICE_TOKEN` 必要な場合のみ
- `BMP280_ADDRESS`

`BMP280_ADDRESS` は既定で `0x77` になっている。I2C スキャナで別のアドレスが見えた場合は、その値に読み替える。

## Arduino IDE で開く

Arduino IDE では、次のファイルを開く。

- `pico2w-local-post-sender/pico2w-local-post-sender.ino`

ボードは `Raspberry Pi Pico 2 W` を選ぶ。

## 送る JSON

次のような JSON を `POST /ingest` へ送る。

```json
{
  "device_id": "pico2w-01",
  "seq": 1,
  "uptime_ms": 12345,
  "temperature_c": 24.8,
  "humidity_pct": 51.2,
  "pressure_hpa": 1008.4,
  "mode": "fixed",
  "bmp280_addr": "0x77",
  "send_interval_ms": 10000
}
```

## シリアルモニタ

`115200 baud` で開く。

期待される出力例:

```text
Pico 2 W local POST sender
Sensors ready
Wi-Fi connecting...
Wi-Fi connected
Wi-Fi IP: 192.168.10.21
AHT temp [C]: 24.80
AHT humidity [%]: 51.20
BMP pressure [hPa]: 1008.40
POST http://192.168.10.10:5000/ingest
payload={"device_id":"pico2w-01","seq":1,"uptime_ms":12345,"temperature_c":24.80,"humidity_pct":51.20,"pressure_hpa":1008.40,"mode":"fixed","bmp280_addr":"0x77","send_interval_ms":10000}
HTTP 200
send ok
```

## MTD へ発展するとき

この最小版では `POST_PATH` は固定である。

次の段階では、以下を変更しやすい。

- `POST_PATH`
- `DEVICE_TOKEN`
- `SEND_INTERVAL_MS`
- `MODE_NAME`

## 関連資料

- [../../slides/lecture05_mtd_local_post_spec.md](../../slides/lecture05_mtd_local_post_spec.md)
- [../../slides/lecture05a_path_rotation_design_discussion.md](../../slides/lecture05a_path_rotation_design_discussion.md)
