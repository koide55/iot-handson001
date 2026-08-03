# Pico 2 W Google スプレッドシート送信スケッチ

このディレクトリには、`Raspberry Pi Pico 2 W` から自前の Google Apps Script ウェブアプリへ JSON を POST し、Google スプレッドシートにデータを蓄積する最小スケッチを置いている。

Ambient が障害や混雑でつながらないときの代替手段として使う。詳しい解説は [../../slides/lecture01_iot_security_pico2w.md](../../slides/lecture01_iot_security_pico2w.md) の「11.9 Ambient が使えないときの代替」を参照。

授業では、**講師が用意した共有シートの URL を配る運用が基本**。その場合、受講者は「Google スプレッドシート側の準備」を飛ばし、スケッチの `SHEET_ENDPOINT` を配られた URL に、`USER_ID` を自分専用の値に書き換えるだけでよい。

## ファイル

- [pico2w-google-sheets-sender.ino](pico2w-google-sheets-sender.ino)
- [Code.gs](Code.gs) — Google Apps Script 側のコード

## 使うライブラリ

- `Adafruit BMP280 Library`
- `Adafruit AHTX0`
- `WiFiClientSecure`（`arduino-pico` ボードパッケージに同梱）
- `HTTPClient`（`arduino-pico` ボードパッケージに同梱）

## 使うピン

- `SDA`: `GP4`
- `SCL`: `GP5`

## Google スプレッドシート側の準備

受け口を用意する人（講師、または自習で自分の受け口を作る人）の手順。講師が配った URL を使う受講者は飛ばしてよい。

1. Google スプレッドシートを新規作成する
2. `拡張機能 -> Apps Script` を開く
3. デフォルトの `myFunction` を消し、[Code.gs](Code.gs) の内容を貼り付け、先頭の `API_KEY` を自分で決めた推測されにくい長い文字列に書き換えて保存する（この値は URL と一緒に受講者へ配る）
4. `デプロイ -> 新しいデプロイ` を選ぶ
5. 種類の選択で歯車アイコンから `ウェブアプリ` を選ぶ
6. 次の設定にする
   - 次のユーザーとして実行: `自分`
   - アクセスできるユーザー: `全員`
7. `デプロイ` をクリックし、初回の承認画面を進める（自分のスクリプトなので `詳細 -> (プロジェクト名)に移動（安全ではないページ）` を選んでよい）
8. 発行された URL（`.../exec` で終わる）をコピーする

> 注記  
> `アクセスできるユーザー: 全員` は、この URL へ誰でもアクセスできる状態を意味する。`Code.gs` の `apiKey` 認証により URL だけでは書き込めないが、キーが漏れれば書き込めるため、演習用の一時的な受け口として扱い、演習後はデプロイを取り消すこと。
>
> 既存のシートへ直接書き込みたい場合は、`Code.gs` の `getSheetByName('data')` をそのシート名（例: `シート1`）に合わせて変更する。
>
> コードを変更した場合、保存しただけでは公開済みの URL には反映されない。`デプロイを管理` から `新バージョン` でデプロイし直すか、`新しいデプロイ` で URL を発行し直すこと。

## 最初に変更する場所

スケッチ先頭の次の設定を、自分の環境に合わせて書き換える。

- `WIFI_SSID`
- `WIFI_PASSWORD`
- `SHEET_ENDPOINT`（講師から配られた URL、または上記手順で発行した `.../exec` の URL）
- `API_KEY`（講師から配られた API キー。自分で受け口を作った場合は `Code.gs` の `API_KEY` と一致させる）
- `USER_ID`（**自分専用の値に必ず変更する**。例: 学籍番号。共有シートで自分の行を見分けるために使う）
- `BMP280_ADDRESS`

`BMP280_ADDRESS` は既定で `0x77` になっている。I2C スキャナで別のアドレスが見えた場合は、その値に読み替える。

## Arduino IDE で開く

Arduino IDE では、次のファイルを開く。

- `pico2w-google-sheets-sender/pico2w-google-sheets-sender.ino`

ボードは `Raspberry Pi Pico 2 W` を選ぶ。

## 送る JSON

次のような JSON を `SHEET_ENDPOINT` へ POST する。

```json
{
  "apiKey": "YOUR_API_KEY",
  "temperature": 24.80,
  "humidity": 51.20,
  "pressure": 1008.40,
  "userid": "user01"
}
```

API キーが一致しない場合、応答は HTTP 200 のまま `{"ok":false,"error":"unauthorized"}` が返り、シートには書き込まれない。成否はステータスコードではなく応答本文の `"ok"` で判定する（スケッチは対応済み）。

## シリアルモニタ

`115200 baud` で開く。

期待される出力例:

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

## 動作確認

Google スプレッドシートを開き、`data` シートに `timestamp`, `temperature`, `humidity`, `pressure`, `userid` の行が追加され続けていれば成功。共有シートの場合は他の受講者の行と混ざるので、自分の `USER_ID` の行を探す。

## よくある失敗

- `USER_ID` を書き換え忘れて、共有シート上で誰の行か区別できなくなる
- `API_KEY` の貼り間違いで `{"ok":false,"error":"unauthorized"}` が返る（HTTP 200 のままなので応答本文まで確認する）
- `アクセスできるユーザー` を `自分のみ` のままにしてしまい、HTTP 403 になる
- コード変更後に再デプロイをせず、古い動作のままになる
- `SHEET_ENDPOINT` が `.../exec` で終わっていない
- `WiFiClientSecure` ではなく `WiFiClient`（HTTP用）を使って接続に失敗する
- `client.setInsecure()` を忘れて証明書エラーになる

## 関連資料

- [../../slides/lecture01_iot_security_pico2w.md](../../slides/lecture01_iot_security_pico2w.md)
