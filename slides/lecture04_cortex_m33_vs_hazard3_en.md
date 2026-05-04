# Advanced Topic: Comparing Cortex-M33 and Hazard3

## Purpose

This material compares the two CPU families available on `Raspberry Pi Pico 2 W`:

- `ARM Cortex-M33`
- `RISC-V Hazard3`

The goal is not to decide which one is "better." The goal is to see:

- the same task
- written for different ISAs
- and explained in a way learners can compare directly

---

## Shared Starting Point

On `RP2350`, Arduino IDE lets you switch `Tools -> CPU Architecture` between:

- `ARM Cortex-M33`
- `RISC-V Hazard3`

Both are **32-bit** processors, but their instruction sets are different.

---

## Main Takeaway

### Easier to teach first

- `Cortex-M33`

Why:

- it has teaching-friendly instructions such as `CBZ`, `UBFX`, `BFI`, `RBIT`, `REV`, and `CLZ`
- those instructions map nicely to visible hardware behavior

### More interesting for comparison

- `Hazard3 RISC-V`

Why:

- the same logic is often written with a more minimal instruction style
- that makes ISA design differences easier to notice

---

## Comparison Theme

We use the same task on both sides:

- toggling one LED state bit

Comparison points:

1. how to make the constant `1`
2. how to read the current state
3. how to toggle bit 0
4. how to return from the function

---

## Cortex-M33 View

In the current class material, the toggle logic looks like this:

```asm
ldr r1, [r0]
movs r2, #1
eors r1, r1, r2
str r1, [r0]
bx lr
```

Reading it step by step:

- `ldr`
  - read from memory
- `movs`
  - prepare constant `1`
- `eors`
  - toggle bit 0
- `str`
  - write back
- `bx lr`
  - return

---

## Hazard3 RISC-V View

A RISC-V flavored version of the same idea would look like this:

```asm
lw   a1, 0(a0)
li   a2, 1
xor  a1, a1, a2
sw   a1, 0(a0)
ret
```

Reading it step by step:

- `lw`
  - read from memory
- `li`
  - prepare constant `1`
- `xor`
  - toggle bit 0
- `sw`
  - write back
- `ret`
  - return

The overall logic is very similar, but the naming style and ISA culture differ.

---

## Side-by-Side Table

| Role | Cortex-M33 | Hazard3 RISC-V |
|---|---|---|
| Read from memory | `ldr` | `lw` |
| Make constant `1` | `movs` | `li` |
| Toggle bit 0 | `eors` | `xor` |
| Write to memory | `str` | `sw` |
| Return | `bx lr` | `ret` |

This makes one thing clear:

- the task is the same
- the instruction style is different

---

## What Is Interesting Here

### Cortex-M33

- many convenient bit-oriented instructions
- strong fit for microcontroller teaching

### Hazard3 RISC-V

- a simpler, more direct style
- useful for understanding why ARM includes some extra convenience instructions

---

## Advanced Hands-On

### Goal

Use the same LED-toggle idea to describe ISA differences between `Cortex-M33` and `Hazard3`.

### Prerequisite

- learners have already completed the `Cortex-M33` worksheet version
- they know how to switch `Tools -> CPU Architecture`

### Hands-On Task

1. review the `Cortex-M33` version of `led_toggle_asm()`
2. write down what the equivalent `Hazard3` instruction flow would probably be
3. compare the following five items

- read instruction
- constant-making instruction
- toggle instruction
- write instruction
- return instruction

### Important Note

This material does **not** yet provide a full Hazard3 `.S` project. The goal here is comparison and explanation, not a complete second implementation.

---

## Mini Assignment

### Task

Fill in the following table in your own words.

| Item | Cortex-M33 | Hazard3 |
|---|---|---|
| Instruction for constant `1` |  |  |
| Instruction for reading memory |  |  |
| Instruction for toggling bit 0 |  |  |
| Instruction for writing memory |  |  |
| Instruction for returning |  |  |

### Submission Requirements

Submit:

1. the completed comparison table
2. a short note of at least 3 lines explaining the difference between `Cortex-M33` and `Hazard3`

### Pass Criteria

- all 5 table items are filled
- the note explains that the same task can be written differently in different ISAs

---

## Summary

The important points are:

- `Cortex-M33` is easier to use as the main teaching CPU
- `Hazard3 RISC-V` is excellent as a comparison target
- even a simple LED toggle can reveal meaningful ISA differences

For the main class, `Cortex-M33` works best as the primary path. For advanced discussion, `Hazard3` adds a very nice comparison layer.
