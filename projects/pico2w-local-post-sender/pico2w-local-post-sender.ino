#include <Wire.h>
#include <WiFi.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_AHTX0.h>

const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";

const char* SERVER_HOST = "192.168.10.10";
const int SERVER_PORT = 5000;
const char* POST_PATH = "/ingest";

const char* DEVICE_ID = "pico2w-01";
const char* DEVICE_TOKEN = "";
const char* MODE_NAME = "fixed";

const unsigned long SEND_INTERVAL_MS = 10000;
const uint8_t I2C_SDA_PIN = 4;
const uint8_t I2C_SCL_PIN = 5;
const uint8_t BMP280_ADDRESS = 0x77;

Adafruit_BMP280 bmp;
Adafruit_AHTX0 aht;
WiFiClient client;

unsigned long lastSendAt = 0;
unsigned long seqNo = 0;

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  Serial.print("Wi-Fi connecting");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
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

String buildPayload(
  unsigned long seq,
  unsigned long uptimeMs,
  float temperatureC,
  float humidityPct,
  float pressureHpa
) {
  String body = "{";
  body += "\"device_id\":\"" + String(DEVICE_ID) + "\",";
  body += "\"seq\":" + String(seq) + ",";
  body += "\"uptime_ms\":" + String(uptimeMs) + ",";
  body += "\"temperature_c\":" + String(temperatureC, 2) + ",";
  body += "\"humidity_pct\":" + String(humidityPct, 2) + ",";
  body += "\"pressure_hpa\":" + String(pressureHpa, 2) + ",";
  body += "\"mode\":\"" + String(MODE_NAME) + "\",";
  body += "\"bmp280_addr\":\"0x" + String(BMP280_ADDRESS, HEX) + "\",";
  body += "\"send_interval_ms\":" + String(SEND_INTERVAL_MS);
  body += "}";
  return body;
}

int readHttpStatus() {
  unsigned long start = millis();
  while (!client.available() && millis() - start < 5000) {
    delay(10);
  }

  if (!client.available()) {
    return -1;
  }

  String statusLine = client.readStringUntil('\n');
  statusLine.trim();
  Serial.print("HTTP status line: ");
  Serial.println(statusLine);

  int firstSpace = statusLine.indexOf(' ');
  if (firstSpace < 0) {
    return -1;
  }

  int secondSpace = statusLine.indexOf(' ', firstSpace + 1);
  if (secondSpace < 0) {
    secondSpace = statusLine.length();
  }

  String codeText = statusLine.substring(firstSpace + 1, secondSpace);
  return codeText.toInt();
}

bool sendJson(const String& body) {
  connectWiFi();

  Serial.print("POST http://");
  Serial.print(SERVER_HOST);
  Serial.print(":");
  Serial.print(SERVER_PORT);
  Serial.println(POST_PATH);
  Serial.print("payload=");
  Serial.println(body);

  if (!client.connect(SERVER_HOST, SERVER_PORT)) {
    Serial.println("server connection failed");
    return false;
  }

  client.print("POST " + String(POST_PATH) + " HTTP/1.1\r\n");
  client.print("Host: " + String(SERVER_HOST) + "\r\n");
  client.print("Content-Type: application/json\r\n");
  client.print("Connection: close\r\n");
  if (String(DEVICE_TOKEN).length() > 0) {
    client.print("X-Device-Token: " + String(DEVICE_TOKEN) + "\r\n");
  }
  client.print("Content-Length: " + String(body.length()) + "\r\n");
  client.print("\r\n");
  client.print(body);

  int statusCode = readHttpStatus();
  Serial.print("HTTP ");
  Serial.println(statusCode);

  while (client.available()) {
    String line = client.readStringUntil('\n');
    line.trim();
    if (line.length() > 0) {
      Serial.println(line);
    }
  }

  client.stop();
  return statusCode == 200;
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  Serial.println("Pico 2 W local POST sender");
  initSensors();
  connectWiFi();
}

void loop() {
  if (millis() - lastSendAt < SEND_INTERVAL_MS) {
    delay(50);
    return;
  }

  lastSendAt = millis();
  seqNo++;

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

  String payload = buildPayload(
    seqNo,
    millis(),
    temperatureC,
    humidityPct,
    pressureHpa
  );

  if (sendJson(payload)) {
    Serial.println("send ok");
  } else {
    Serial.println("send failed");
  }

  Serial.println();
}
