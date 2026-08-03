# Pico 2 W Google Sheets Sender Sketch

This directory contains a minimal sketch that sends JSON from `Raspberry Pi Pico 2 W` to your own Google Apps Script web app, which appends the data to a Google Sheet.

Use this as a fallback for when Ambient is unavailable due to an outage or congestion. See "Section 11.5: Fallback When Ambient Is Unavailable" in [../../slides/lecture01_iot_security_pico2w_en.md](../../slides/lecture01_iot_security_pico2w_en.md) for the full write-up.

In class, **the default is a shared sheet prepared by the instructor**, who hands out the endpoint URL. In that case, learners skip the setup section below and only edit the sketch: set `SHEET_ENDPOINT` to the distributed URL and change `USER_ID` to a personal value.

## Files

- [pico2w-google-sheets-sender.ino](pico2w-google-sheets-sender.ino)
- [Code.gs](Code.gs) — the Google Apps Script code

## Libraries Used

- `Adafruit BMP280 Library`
- `Adafruit AHTX0`
- `WiFiClientSecure` (bundled with the `arduino-pico` board package)
- `HTTPClient` (bundled with the `arduino-pico` board package)

## Pins Used

- `SDA`: `GP4`
- `SCL`: `GP5`

## Setting Up the Google Sheets Side

These steps are for whoever hosts the endpoint (the instructor, or a learner hosting their own). If you were given a URL by the instructor, skip this section.

1. Create a new Google Sheet.
2. Open `Extensions -> Apps Script`.
3. Replace the default `myFunction` with the contents of [Code.gs](Code.gs), change `API_KEY` at the top to a long, hard-to-guess string of your own, and save (distribute this key together with the URL).
4. Choose `Deploy -> New deployment`.
5. Click the gear icon and select `Web app` as the type.
6. Use these settings:
   - Execute as: `Me`
   - Who has access: `Anyone`
7. Click `Deploy` and go through the one-time authorization prompt (it's your own script, so it's safe to proceed past the "unverified app" warning).
8. Copy the deployment URL (it ends in `/exec`).

> Note  
> `Who has access: Anyone` means anyone can reach this URL. The `apiKey` check in `Code.gs` prevents writes from someone who only knows the URL, but anyone who also has the key can write. Treat it as a temporary classroom endpoint and revoke the deployment when you're done.
>
> To write directly into an existing sheet, change `getSheetByName('data')` in `Code.gs` to that sheet's name (e.g. `Sheet1`).
>
> Editing the script does not update the live URL until you redeploy — either edit the existing deployment with `New version`, or create a new deployment (which issues a new URL).

## What to Change First

Update these constants at the top of the sketch for your environment:

- `WIFI_SSID`
- `WIFI_PASSWORD`
- `SHEET_ENDPOINT` (the URL distributed by the instructor, or the `.../exec` URL from the steps above)
- `API_KEY` (the key distributed by the instructor; if self-hosted, must match `API_KEY` in `Code.gs`)
- `USER_ID` (**always change this to a personal value**, e.g. your student ID — it is how you find your own rows on a shared sheet)
- `BMP280_ADDRESS`

`BMP280_ADDRESS` defaults to `0x77`. If the I2C scanner shows a different address, use that value instead.

## Opening in Arduino IDE

Open this file in Arduino IDE:

- `pico2w-google-sheets-sender/pico2w-google-sheets-sender.ino`

Select `Raspberry Pi Pico 2 W` as the board.

## JSON Payload

The sketch POSTs JSON like this to `SHEET_ENDPOINT`:

```json
{
  "apiKey": "YOUR_API_KEY",
  "temperature": 24.80,
  "humidity": 51.20,
  "pressure": 1008.40,
  "userid": "user01"
}
```

If the API key does not match, the response is still HTTP 200 but the body is `{"ok":false,"error":"unauthorized"}` and nothing is written. Success is determined by `"ok"` in the response body, not the status code (the sketch already does this).

## Serial Monitor

Open at `115200 baud`.

Expected output:

```text
Pico 2 W Google Sheets sender
Sensors ready
Wi-Fi connecting...
Wi-Fi connected
Wi-Fi IP: 192.168.10.21
AHT temp [C]: 24.80
AHT humidity [%]: 51.20
BMP pressure [hPa]: 1008.40
POST https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
payload={"apiKey":"YOUR_API_KEY","temperature":24.80,"humidity":51.20,"pressure":1008.40,"userid":"user01"}
HTTP 200
{"ok":true}
send ok
```

## Verifying It Works

Open the Google Sheet and confirm that the `data` sheet keeps gaining new rows of `timestamp`, `temperature`, `humidity`, `pressure`, `userid`. On a shared classroom sheet, rows from everyone are interleaved — find yours by your `USER_ID`.

## Common Failures

- forgetting to change `USER_ID`, making it impossible to tell whose rows are whose on a shared sheet
- a mistyped `API_KEY`, returning `{"ok":false,"error":"unauthorized"}` (still HTTP 200 — check the response body)
- `Who has access` left as `Only myself`, causing HTTP 403
- forgetting to redeploy after editing the script, so the old behavior persists
- `SHEET_ENDPOINT` not ending in `/exec`
- using plain `WiFiClient` instead of `WiFiClientSecure`, causing the connection to fail
- forgetting `client.setInsecure()`, causing a certificate error

## Related Docs

- [../../slides/lecture01_iot_security_pico2w_en.md](../../slides/lecture01_iot_security_pico2w_en.md)
