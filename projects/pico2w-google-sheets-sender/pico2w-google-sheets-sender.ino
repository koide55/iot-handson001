#include <Wire.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_AHTX0.h>

const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";

// 講師から配られた URL、または Apps Script のデプロイで発行された URL（/exec で終わる）
const char* SHEET_ENDPOINT = "https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec";

// 講師から配られた API キー（自分で受け口を作った場合は Code.gs の API_KEY と一致させる）
const char* API_KEY = "YOUR_API_KEY";

// 自分専用の名前に必ず変更する（例: 学籍番号）。
// 共有シートでは全員の行が混ざるので、この値で自分の行を見分ける。
const char* USER_ID = "user01";

const unsigned long SEND_INTERVAL_MS = 10000;
const uint8_t I2C_SDA_PIN = 4;
const uint8_t I2C_SCL_PIN = 5;
const uint8_t BMP280_ADDRESS = 0x77;

Adafruit_BMP280 bmp;
Adafruit_AHTX0 aht;

unsigned long lastSendAt = 0;

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  Serial.print("Wi-Fi connecting");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  const int maxAttempts = 20;   // 約 10 秒でタイムアウト
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < maxAttempts) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  Serial.println();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi connect timeout; will retry next cycle");
    return;
  }

  Serial.println("Wi-Fi connected");
  Serial.print("Wi-Fi IP: ");
  Serial.println(WiFi.localIP());
}

void initSensors() {
  Wire.setSDA(I2C_SDA_PIN);
  Wire.setSCL(I2C_SCL_PIN);
  Wire.begin();

  if (!bmp.begin(BMP280_ADDRESS)) {
    Serial.print("BMP280 not found at 0x");
    Serial.println(BMP280_ADDRESS, HEX);
    while (1) {
      delay(100);
    }
  }

  if (!aht.begin()) {
    Serial.println("AHT20 not found");
    while (1) {
      delay(100);
    }
  }

  Serial.println("Sensors ready");
}

String buildPayload(float temperatureC, float humidityPct, float pressureHpa) {
  String body = "{";
  body += "\"apiKey\":\"" + String(API_KEY) + "\",";
  body += "\"temperature\":" + String(temperatureC, 2) + ",";
  body += "\"humidity\":" + String(humidityPct, 2) + ",";
  body += "\"pressure\":" + String(pressureHpa, 2) + ",";
  body += "\"userid\":\"" + String(USER_ID) + "\"";
  body += "}";
  return body;
}

bool sendToSheet(const String& body) {
  connectWiFi();

  Serial.print("POST ");
  Serial.println(SHEET_ENDPOINT);
  Serial.print("payload=");
  Serial.println(body);

  WiFiClientSecure client;
  client.setInsecure();   // 演習用。証明書検証を省略する

  HTTPClient http;
  http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);   // Apps Script は 302 で実体 URL に転送される

  if (!http.begin(client, SHEET_ENDPOINT)) {
    Serial.println("http.begin failed");
    return false;
  }

  http.addHeader("Content-Type", "application/json");

  int status = http.POST(body);
  Serial.print("HTTP ");
  Serial.println(status);

  String response = "";
  if (status > 0) {
    response = http.getString();
    Serial.println(response);
  }

  http.end();

  // Apps Script は API キーが間違っていても HTTP 200 を返すので、
  // 成否は応答本文の "ok":true で判定する
  return status == 200 && response.indexOf("\"ok\":true") >= 0;
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  Serial.println("Pico 2 W Google Sheets sender");
  initSensors();
  connectWiFi();
}

void loop() {
  if (millis() - lastSendAt < SEND_INTERVAL_MS) {
    delay(50);
    return;
  }

  lastSendAt = millis();

  connectWiFi();

  sensors_event_t humidityEvent, tempEvent;
  aht.getEvent(&humidityEvent, &tempEvent);

  float temperatureC = tempEvent.temperature;
  float humidityPct = humidityEvent.relative_humidity;
  float pressureHpa = bmp.readPressure() / 100.0;

  Serial.print("AHT temp [C]: ");
  Serial.println(temperatureC);
  Serial.print("AHT humidity [%]: ");
  Serial.println(humidityPct);
  Serial.print("BMP pressure [hPa]: ");
  Serial.println(pressureHpa);

  String payload = buildPayload(temperatureC, humidityPct, pressureHpa);

  if (sendToSheet(payload)) {
    Serial.println("send ok");
  } else {
    Serial.println("send failed");
  }

  Serial.println();
}
