# Pico 2 W Cortex-M33 アセンブラ プロジェクト: 穴埋め版

Cortex-M33 アセンブラのハンズオンプロジェクトの、受講者向け穴埋め版です。

## 用途

次のようなときに使います。

- 受講者にアセンブラを自分で書かせたい
- 白紙のファイルではなくガイド付きの穴埋めにしたい
- いくつかの中心的な命令に絞りたい

## ファイル

- `pico2w-cortexm33-asm-worksheet.ino`
- `asm_api.h`
- `led_asm.S`

## ボード設定

- ボード: `Raspberry Pi Pico 2 W`
- CPU Architecture: `ARM Cortex-M33`

## 配線

- `GP15` -> 抵抗 -> LED アノード
- LED カソード -> `GND`
- ボタン（任意）:
  - 片側 -> `GP14`
  - 反対側 -> `GND`

## 演習の流れ

1. まず一度ビルドして実行する。
2. `led_asm.S` を開く。
3. 各 `TODO` を埋める。
4. 小さなステップごとに再ビルドする。

## おすすめの順番

1. `led_on_asm`
2. `led_off_asm`
3. `led_toggle_asm`
4. `should_toggle_on_press_asm`
5. `ubfx_demo_asm`
6. `bfi_demo_asm`
7. `rbit_demo_asm`
8. `rev_demo_asm`
9. `clz_demo_asm`

## 講師向けメモ

完成版（解答）は次の場所にあります。

- `../pico2w-cortexm33-asm-complete/`

## English

- [README_en.md](README_en.md)
