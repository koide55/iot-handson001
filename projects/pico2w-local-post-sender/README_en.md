# Pico 2 W Local POST Sender Sketch

This directory contains a minimal sketch that sends JSON data from a `Raspberry Pi Pico 2 W` to the local Python receiver server.

It is intended to work with the receiver described in [../local-python-receiver/README_en.md](../local-python-receiver/README_en.md).

## Files

- [pico2w-local-post-sender.ino](pico2w-local-post-sender.ino)

## Required Libraries

- `Adafruit BMP280 Library`
- `Adafruit AHTX0`

## Pin Usage

- `SDA`: `GP4`
- `SCL`: `GP5`

## Settings to Edit First

Update these values near the top of the sketch.

- `WIFI_SSID`
- `WIFI_PASSWORD`
- `SERVER_HOST`
- `SERVER_PORT`
- `POST_PATH`
- `DEVICE_ID`
- `DEVICE_TOKEN` only if needed
- `BMP280_ADDRESS`

`BMP280_ADDRESS` is set to `0x77` by default. If your I2C scanner finds a different address, replace it here.

## Open in Arduino IDE

Open:

- `pico2w-local-post-sender/pico2w-local-post-sender.ino`

Select the board `Raspberry Pi Pico 2 W`.

## JSON Payload

The sketch sends JSON like this to `POST /ingest`.

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

## Serial Monitor

Use `115200 baud`.

Expected output example:

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

## For Later MTD Extensions

This minimum version keeps `POST_PATH` fixed.

The next stage can vary:

- `POST_PATH`
- `DEVICE_TOKEN`
- `SEND_INTERVAL_MS`
- `MODE_NAME`

## Related Slides

- [../../slides/lecture05_mtd_local_post_spec_en.md](../../slides/lecture05_mtd_local_post_spec_en.md)
