# Cortex-M33 Assembly Primer

## Role of This Material

This is a gentle pre-reading note for the main hands-on:

- [Cortex-M33 Assembly Hands-On](lecture02_assembly_handson_restructured_en.md)

It explains only the instructions that appear in the worksheet version of:

- [led_asm.S](../projects/pico2w-cortexm33-asm-worksheet/led_asm.S)

## Instruction List

- `ldr`
- `str`
- `movs`
- `orrs`
- `bics`
- `eors`
- `cbz`
- `ubfx`
- `bfi`
- `rbit`
- `rev`
- `clz`
- `bx lr`

## Registers

In this class, think of registers such as `r0`, `r1`, and `r2` as very small, very fast work notes inside the CPU.

- `r0`
  - usually holds the first argument
- `r1`
  - often holds a value read from memory
- `r2`
  - often holds a helper constant such as `1`

## Address vs Value

If `r0` contains the address of `state`, that is not the value of `state` itself. It is the location where `state` is stored.

## `ldr` and `str`

```asm
ldr r1, [r0]
```

Read the value stored at the address in `r0` and put it into `r1`.

```asm
str r1, [r0]
```

Write the value in `r1` back to the address in `r0`.

Together, this gives the classic pattern:

1. read
2. modify
3. write back

## `movs`

```asm
movs r2, #1
```

This is close to `r2 = 1`.

In this hands-on, `1` is used as a bit mask for bit 0.

## `orrs`

```asm
orrs r1, r1, r2
```

Close to:

```c
r1 = r1 | r2;
```

Useful for setting bit 0 to 1.

## `bics`

```asm
bics r1, r1, r2
```

Close to:

```c
r1 = r1 & ~r2;
```

Useful for clearing bit 0.

## `eors`

```asm
eors r1, r1, r2
```

Close to:

```c
r1 = r1 ^ r2;
```

Useful for toggling bit 0.

## `cbz`

```asm
cbz r0, label
```

Branch to `label` if `r0` is zero.

In this class, this is useful because with `INPUT_PULLUP`:

- not pressed = `1`
- pressed = `0`

## `ubfx`

```asm
ubfx r0, r0, #4, #2
```

Extract 2 bits starting at bit 4 from `r0`.

Close to:

```c
r0 = (r0 >> 4) & 0x3;
```

## `bfi`

```asm
bfi r0, r1, #4, #2
```

Insert the low 2 bits of `r1` into `r0` starting at bit 4.

## `rbit`

Reverse the bit order of a register value.

## `rev`

Reverse the byte order of a register value.

For example:

```text
0x12345678 -> 0x78563412
```

## `clz`

Count leading zeros.

## `bx lr`

Return from the function.

## TODO to Instruction Map

| TODO | Main Instruction |
|---|---|
| `led_on_asm` | `orrs` |
| `led_off_asm` | `bics` |
| `led_toggle_asm` | `eors` |
| `should_toggle_on_press_asm` | `cbz` |
| `ubfx_demo_asm` | `ubfx` |
| `bfi_demo_asm` | `bfi` |
| `rbit_demo_asm` | `rbit` |
| `rev_demo_asm` | `rev` |
| `clz_demo_asm` | `clz` |

## Next Step

After reading this, continue with:

- [Cortex-M33 Assembly Hands-On](lecture02_assembly_handson_restructured_en.md)
