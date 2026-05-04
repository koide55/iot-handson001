# Pico 2 W Cortex-M33 Assembly Project: Worksheet

This is the student worksheet version of the Cortex-M33 assembly hands-on project.

## Purpose

Use this version when:

- students should fill in the assembly themselves
- you want a guided worksheet instead of a blank file
- you want to focus on a few core instructions

## Files

- `pico2w-cortexm33-asm-worksheet.ino`
- `asm_api.h`
- `led_asm.S`

## Board settings

- Board: `Raspberry Pi Pico 2 W`
- CPU Architecture: `ARM Cortex-M33`

## Wiring

- `GP15` -> resistor -> LED anode
- LED cathode -> `GND`
- optional button:
  - one side -> `GP14`
  - other side -> `GND`

## Exercise flow

1. Build and run once.
2. Open `led_asm.S`.
3. Fill each `TODO`.
4. Rebuild after each small step.

## Suggested order

1. `led_on_asm`
2. `led_off_asm`
3. `led_toggle_asm`
4. `should_toggle_on_press_asm`
5. `ubfx_demo_asm`
6. `bfi_demo_asm`
7. `rbit_demo_asm`
8. `rev_demo_asm`
9. `clz_demo_asm`

## Instructor note

The complete answer-key version lives in:

- `../pico2w-cortexm33-asm-complete/`
