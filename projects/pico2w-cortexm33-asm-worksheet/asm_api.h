#ifndef ASM_API_H
#define ASM_API_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void led_on_asm(uint32_t* state);
void led_off_asm(uint32_t* state);
void led_toggle_asm(uint32_t* state);
uint32_t should_toggle_on_press_asm(uint32_t button_level);
uint32_t ubfx_demo_asm(uint32_t value);
uint32_t bfi_demo_asm(uint32_t original, uint32_t field_value);
uint32_t rbit_demo_asm(uint32_t value);
uint32_t rev_demo_asm(uint32_t value);
uint32_t clz_demo_asm(uint32_t value);

#ifdef __cplusplus
}
#endif

#endif
