.syntax unified
.thumb

.text

.global led_on_asm
.type led_on_asm, %function
led_on_asm:
    @ TODO 1:
    @ Load *state from [r0] into r1.
    @ Put the value 1 into r2.
    @ Set bit 0 in r1.
    @ Store r1 back to [r0].
    @ Return with bx lr.
    ldr r1, [r0]
    movs r2, #1
    @ TODO: replace the next instruction with the correct one.
    nop
    str r1, [r0]
    bx lr

.global led_off_asm
.type led_off_asm, %function
led_off_asm:
    @ TODO 2:
    @ Clear bit 0 from *state.
    ldr r1, [r0]
    movs r2, #1
    @ TODO: replace the next instruction with the correct one.
    nop
    str r1, [r0]
    bx lr

.global led_toggle_asm
.type led_toggle_asm, %function
led_toggle_asm:
    @ TODO 3:
    @ Toggle bit 0 in *state using EOR.
    ldr r1, [r0]
    movs r2, #1
    @ TODO: replace the next instruction with the correct one.
    nop
    str r1, [r0]
    bx lr

.global should_toggle_on_press_asm
.type should_toggle_on_press_asm, %function
should_toggle_on_press_asm:
    @ TODO 4:
    @ If r0 is zero, branch to .Lpressed.
    @ Otherwise return 0.
    nop
    movs r0, #0
    bx lr
.Lpressed:
    movs r0, #1
    bx lr

.global ubfx_demo_asm
.type ubfx_demo_asm, %function
ubfx_demo_asm:
    @ TODO 5:
    @ Extract 2 bits starting at bit 4 from r0 into r0.
    nop
    bx lr

.global bfi_demo_asm
.type bfi_demo_asm, %function
bfi_demo_asm:
    @ TODO 6:
    @ Insert the low 2 bits of r1 into r0 at bit position 4.
    nop
    bx lr

.global rbit_demo_asm
.type rbit_demo_asm, %function
rbit_demo_asm:
    @ TODO 7:
    @ Reverse the bit order of r0.
    nop
    bx lr

.global rev_demo_asm
.type rev_demo_asm, %function
rev_demo_asm:
    @ TODO 8:
    @ Reverse the byte order of r0.
    nop
    bx lr

.global clz_demo_asm
.type clz_demo_asm, %function
clz_demo_asm:
    @ TODO 9:
    @ Count leading zeros of r0 into r0.
    nop
    bx lr
