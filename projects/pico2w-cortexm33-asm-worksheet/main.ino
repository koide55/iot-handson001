#include "asm_api.h"

const int LED_PIN = 15;
const int BUTTON_PIN = 14;

volatile uint32_t g_led_state = 0;

void apply_led_state() {
  digitalWrite(LED_PIN, g_led_state ? HIGH : LOW);
}

void print_demo_results() {
  const uint32_t sample = 0x12345678u;
  const uint32_t field_source = 0x000000b0u;
  const uint32_t field_insert = 0x00000002u;

  Serial.println("=== Cortex-M33 asm worksheet ===");

  Serial.print("UBFX source      : 0x");
  Serial.println(field_source, HEX);
  Serial.print("UBFX bits[5:4]   : 0x");
  Serial.println(ubfx_demo_asm(field_source), HEX);

  Serial.print("BFI original     : 0x");
  Serial.println(field_source, HEX);
  Serial.print("BFI insert value : 0x");
  Serial.println(field_insert, HEX);
  Serial.print("BFI result       : 0x");
  Serial.println(bfi_demo_asm(field_source, field_insert), HEX);

  Serial.print("RBIT source      : 0x");
  Serial.println(sample, HEX);
  Serial.print("RBIT result      : 0x");
  Serial.println(rbit_demo_asm(sample), HEX);

  Serial.print("REV source       : 0x");
  Serial.println(sample, HEX);
  Serial.print("REV result       : 0x");
  Serial.println(rev_demo_asm(sample), HEX);

  Serial.print("CLZ source       : 0x");
  Serial.println(sample, HEX);
  Serial.print("CLZ result       : ");
  Serial.println(clz_demo_asm(sample));

  Serial.println();
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  Serial.begin(115200);
  delay(2000);

  Serial.println("Pico 2 W Cortex-M33 assembly worksheet");
  print_demo_results();

  led_on_asm((uint32_t*)&g_led_state);
  apply_led_state();
  delay(300);

  led_off_asm((uint32_t*)&g_led_state);
  apply_led_state();
  delay(300);

  led_toggle_asm((uint32_t*)&g_led_state);
  apply_led_state();
  delay(300);
}

void loop() {
  uint32_t button_level = (uint32_t)digitalRead(BUTTON_PIN);

  if (should_toggle_on_press_asm(button_level)) {
    led_toggle_asm((uint32_t*)&g_led_state);
    apply_led_state();
    delay(200);
  }

  delay(20);
}
