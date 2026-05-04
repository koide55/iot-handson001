# Cortex-M33 Assembly Hands-On Notes

## Purpose

This lecture explains the Cortex-M33 instructions that appear in the hands-on project and connects them to visible hardware behavior on `Raspberry Pi Pico 2 W`.

It focuses on:

- `EOR`
- `CBZ` / `CBNZ`
- `UBFX` / `BFI`
- `RBIT` / `REV` / `CLZ`
- `LDREX` / `STREX` as an advanced topic

Pre-reading:

- [Cortex-M33 Assembly Primer](lecture02a_cortex_m33_assembly_primer_en.md)

## Topics

1. understand the role of Cortex-M33 in this class
2. confirm a C-only blink sketch
3. implement LED on/off/toggle with assembly
4. shorten zero-check branches with `CBZ`/`CBNZ`
5. study bit-field operations with `UBFX`/`BFI`
6. study `RBIT`/`REV`/`CLZ`
7. optionally touch on `LDREX`/`STREX`

## Why Use a Separate `.S` File

The class uses a `.S` file instead of inline assembly because:

- the instructions are easier to read
- the boundary between C and assembly is clearer
- the material is easier to distribute

## Basic Wiring

- LED: `GP15` to resistor to LED anode, LED cathode to `GND`
- tact switch: one side to `GP14`, opposite side to `GND`

## Core Idea: Visible Bit Operations

The beauty of Cortex-M33 in this class is not exotic immediate formats. It is that a single instruction often maps directly to something learners can see.

Examples:

- set one bit
- clear one bit
- toggle one bit
- branch when the value is zero
- extract part of a register

## `EOR` for LED Toggle

The class uses `EOR` as the key instruction for LED toggle.

Conceptually:

```cpp
state ^= 1;
```

This lets learners see how a one-bit XOR changes an actual LED state.

## `CBZ` / `CBNZ`

These are useful because embedded code often asks:

- is the flag zero?
- is the counter zero?
- is the input low?

With pull-up input, a pressed tact switch becomes `0`, so `CBZ` is a natural fit.

## `UBFX` / `BFI`

Microcontroller registers often use only part of a word for a specific meaning.

- `UBFX`
  - extract a bit field
- `BFI`
  - insert a bit field

This makes them a clean match for register-style programming.

## `RBIT`, `REV`, `CLZ`

These are excellent examples of instructions that are much cleaner than writing loops by hand.

- `RBIT`
  - reverse bit order
- `REV`
  - reverse byte order
- `CLZ`
  - count leading zeros

## Suggested Exercise Order

1. `led_on_asm()`
2. `led_off_asm()`
3. `led_toggle_asm()`
4. `should_toggle_on_press_asm()`
5. `ubfx_demo_asm()`
6. `bfi_demo_asm()`
7. `rbit_demo_asm()`
8. `rev_demo_asm()`
9. `clz_demo_asm()`

## Assignment and Submission Requirements

### Task 1: Core Functions

Complete:

- `led_on_asm()`
- `led_off_asm()`
- `led_toggle_asm()`
- `should_toggle_on_press_asm()`

Requirements:

- `led_toggle_asm()` must use `EOR`
- `should_toggle_on_press_asm()` must use `CBZ` or `CBNZ`

### Task 2: Bit-Field Functions

Complete:

- `ubfx_demo_asm()`
- `bfi_demo_asm()`

Requirements:

- `ubfx_demo_asm()` extracts 2 bits starting at bit 4
- `bfi_demo_asm()` inserts the low 2 bits into bit position 4

### Task 3: Observation Functions

Complete:

- `rbit_demo_asm()`
- `rev_demo_asm()`
- `clz_demo_asm()`

Confirm the input and output in the serial monitor.

### Submission Items

1. `pico2w-cortexm33-asm-worksheet.ino`
2. `led_asm.S`
3. one serial monitor screenshot
4. one photo or short video showing LED behavior
5. one short explanation document

### The Explanation Document Must Include

1. the instruction used in `led_toggle_asm()`
2. the branch instruction used in `should_toggle_on_press_asm()`
3. the input and result of `UBFX`
4. the input and result of `BFI`
5. which of `RBIT`, `REV`, `CLZ` was the most interesting and why
6. any issue encountered and how it was fixed

### Pass Criteria

- the project compiles
- all 9 functions are implemented
- LED on/off/toggle works on hardware
- the LED toggles only when the tact switch is pressed
- `UBFX`, `BFI`, `RBIT`, `REV`, and `CLZ` results appear in the serial monitor
