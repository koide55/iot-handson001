# Pico 2 W Cortex-M33 Assembly Minimal Project

This project is a minimal Arduino IDE project for the `Raspberry Pi Pico 2 W` that pairs with the Cortex-M33 assembly hands-on slides.

## Goal

Keep the project small and reliable while still demonstrating useful Cortex-M33 instructions:

- `EOR` for LED toggle
- `CBZ` / `CBNZ` for zero/non-zero branching
- `UBFX` / `BFI` for bit-field extraction and insertion
- `RBIT` / `REV` / `CLZ` for bit and byte operations

## Design choice

To keep the sample easy to build in Arduino IDE, this version does **not** directly poke RP2350 GPIO registers from assembly.

Instead:

- Arduino API handles pin setup and `digitalWrite`
- Assembly functions manipulate a 1-bit LED state and return results to C++

This keeps the project focused on the instruction behavior itself and avoids depending on RP2350-specific register headers.

## Files

- `pico2w-cortexm33-asm.ino`
  - Arduino sketch
- `led_asm.S`
  - ARM Thumb assembly functions
- `asm_api.h`
  - function declarations shared with C++

## Board settings

In Arduino IDE:

- Board: `Raspberry Pi Pico 2 W`
- CPU Architecture: `ARM Cortex-M33`

This project is not for the `RISC-V Hazard3` setting.

## Wiring

- `GP15` -> resistor -> LED anode
- LED cathode -> `GND`
- optional button:
  - one side -> `GP14`
  - other side -> `GND`

The sketch uses `INPUT_PULLUP` for the button.

## What the sketch does

1. Turns LED on by calling assembly
2. Turns LED off by calling assembly
3. Toggles LED by calling assembly
4. Uses a button check with `CBZ`
5. Prints `UBFX`, `BFI`, `RBIT`, `REV`, and `CLZ` demo results to Serial

## Notes

- The `.S` file uses unified ARM syntax and Thumb functions.
- If you switch the board to `RISC-V Hazard3`, this file will not assemble.
- This project is the minimal working starting point. A later version can replace the Arduino API output path with direct GPIO register writes if desired.
