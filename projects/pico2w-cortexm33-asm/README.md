# Pico 2 W Cortex-M33 アセンブラ 最小プロジェクト

このプロジェクトは、Cortex-M33 アセンブラのハンズオン用スライドと対になる、`Raspberry Pi Pico 2 W` 向けの最小 Arduino IDE プロジェクトです。

## ねらい

プロジェクトを小さく確実に保ちつつ、Cortex-M33 の便利な命令を体験します。

- `EOR`: LED の反転
- `CBZ` / `CBNZ`: 0 / 非 0 での分岐
- `UBFX` / `BFI`: ビットフィールドの取り出しと埋め込み
- `RBIT` / `REV` / `CLZ`: ビット・バイト操作

## 設計方針

Arduino IDE でビルドしやすくするため、この版ではアセンブラから RP2350 の GPIO レジスタを直接叩くことは **しません**。

代わりに:

- ピン設定と `digitalWrite` は Arduino API が担当する
- アセンブラ関数は 1 ビットの LED 状態を操作し、結果を C++ へ返す

これにより、命令そのものの挙動に集中でき、RP2350 固有のレジスタヘッダへの依存を避けられます。

## ファイル

- `pico2w-cortexm33-asm.ino`
  - Arduino スケッチ
- `led_asm.S`
  - ARM Thumb アセンブラ関数
- `asm_api.h`
  - C++ と共有する関数宣言

## ボード設定

Arduino IDE で:

- ボード: `Raspberry Pi Pico 2 W`
- CPU Architecture: `ARM Cortex-M33`

このプロジェクトは `RISC-V Hazard3` 設定用ではありません。

## 配線

- `GP15` -> 抵抗 -> LED アノード
- LED カソード -> `GND`
- ボタン（任意）:
  - 片側 -> `GP14`
  - 反対側 -> `GND`

スケッチではボタンに `INPUT_PULLUP` を使います。

## スケッチの動作

1. アセンブラを呼んで LED を点灯する
2. アセンブラを呼んで LED を消灯する
3. アセンブラを呼んで LED を反転する
4. `CBZ` を使ってボタンを判定する
5. `UBFX`、`BFI`、`RBIT`、`REV`、`CLZ` のデモ結果をシリアルに表示する

## 補足

- `.S` ファイルは unified ARM 構文と Thumb 関数を使います。
- ボードを `RISC-V Hazard3` に切り替えると、このファイルはアセンブルできません。
- このプロジェクトは、最小で動く出発点です。必要であれば、後の版で Arduino API による出力経路を GPIO レジスタ直接書き込みに置き換えられます。

## English

- [README_en.md](README_en.md)
