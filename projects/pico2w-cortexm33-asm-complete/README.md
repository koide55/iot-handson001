# Pico 2 W Cortex-M33 アセンブラ プロジェクト: 完成版

Cortex-M33 アセンブラのハンズオンプロジェクトの、講師向け完成版です。

## 用途

次のようなときに使います。

- 正しく動く参照実装がほしい
- 期待される動作をその場でデモしたい
- 演習後に答え合わせ用の解答が必要

## ファイル

- `pico2w-cortexm33-asm-complete.ino`
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

## ここで動くもの

- LED 点灯
- LED 消灯
- `EOR` による LED 反転
- `CBZ` によるボタン判定
- `UBFX`
- `BFI`
- `RBIT`
- `REV`
- `CLZ`

## 授業での使い方の例

1. 環境確認が必要なら、まずこの版でデモする。
2. 穴埋め版を配布する。
3. 演習後の答え合わせにこの版を使う。

## English

- [README_en.md](README_en.md)
