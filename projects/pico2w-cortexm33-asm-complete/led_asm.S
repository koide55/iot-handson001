.syntax unified
.thumb

.text

.global led_on_asm
.type led_on_asm, %function
led_on_asm:
    ldr r1, [r0]
    movs r2, #1
    orrs r1, r1, r2
    str r1, [r0]
    bx lr

.global led_off_asm
.type led_off_asm, %function
led_off_asm:
    ldr r1, [r0]
    movs r2, #1
    bics r1, r1, r2
    str r1, [r0]
    bx lr

.global led_toggle_asm
.type led_toggle_asm, %function
led_toggle_asm:
    ldr r1, [r0]
    movs r2, #1
    eors r1, r1, r2
    str r1, [r0]
    bx lr

.global should_toggle_on_press_asm
.type should_toggle_on_press_asm, %function
should_toggle_on_press_asm:
    cbz r0, .Lpressed
    movs r0, #0
    bx lr
.Lpressed:
    movs r0, #1
    bx lr

.global ubfx_demo_asm
.type ubfx_demo_asm, %function
ubfx_demo_asm:
    ubfx r0, r0, #4, #2
    bx lr

.global bfi_demo_asm
.type bfi_demo_asm, %function
bfi_demo_asm:
    bfi r0, r1, #4, #2
    bx lr

.global rbit_demo_asm
.type rbit_demo_asm, %function
rbit_demo_asm:
    rbit r0, r0
    bx lr

.global rev_demo_asm
.type rev_demo_asm, %function
rev_demo_asm:
    rev r0, r0
    bx lr

.global clz_demo_asm
.type clz_demo_asm, %function
clz_demo_asm:
    clz r0, r0
    bx lr
