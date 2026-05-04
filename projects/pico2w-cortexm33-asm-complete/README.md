# Pico 2 W Cortex-M33 Assembly Project: Complete

This is the instructor-ready complete version of the Cortex-M33 assembly hands-on project.

## Purpose

Use this version when:

- you want a known-good reference
- you want to demo the expected behavior live
- students need an answer key after the exercise

## Files

- `main.ino`
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

## What works here

- LED on
- LED off
- LED toggle by `EOR`
- button decision by `CBZ`
- `UBFX`
- `BFI`
- `RBIT`
- `REV`
- `CLZ`

## Suggested use in class

1. Demo this version first if you need to verify the environment.
2. Hand out the worksheet version.
3. Use this version as the post-exercise walkthrough.
