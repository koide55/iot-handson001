# IoT Hands-On Projects

このディレクトリには、Cortex-M33 アセンブラ演習で使う Arduino IDE プロジェクトをまとめています。

## プロジェクト一覧

| 種類 | 内容 | フォルダ |
|---|---|---|
| 最小版 | 命令確認用の最小サンプル | [pico2w-cortexm33-asm](pico2w-cortexm33-asm/README.md) |
| 完成版 | 講師デモ用、答え合わせ用 | [pico2w-cortexm33-asm-complete](pico2w-cortexm33-asm-complete/README.md) |
| 穴埋め版 | 受講者が `TODO` を埋める演習用 | [pico2w-cortexm33-asm-worksheet](pico2w-cortexm33-asm-worksheet/README.md) |
| 受信サーバ | IoT / MTD 演習で使う最小の Python 受信サーバ | [local-python-receiver](local-python-receiver/README.md) |
| 送信スケッチ | IoT / MTD 演習で使う Pico 2 W 側の最小送信コード | [pico2w-local-post-sender](pico2w-local-post-sender/README.md) |

## どれを使うか

- 授業中に最初から最後まで一緒に進めるなら:
  - 穴埋め版
- 講師が手元で正しい動作を確認したいなら:
  - 完成版
- 命令を少しだけ試したいなら:
  - 最小版

## Arduino IDE で開くときの注意

Arduino IDE では、**フォルダ名と同じ `.ino` ファイル** を開いてください。

たとえば:

- `pico2w-cortexm33-asm/pico2w-cortexm33-asm.ino`
- `pico2w-cortexm33-asm-complete/pico2w-cortexm33-asm-complete.ino`
- `pico2w-cortexm33-asm-worksheet/pico2w-cortexm33-asm-worksheet.ino`

## 関連資料

スライド資料の一覧:

- [../slides/README.md](../slides/README.md)
- [local-python-receiver/README.md](local-python-receiver/README.md)
- [pico2w-local-post-sender/README.md](pico2w-local-post-sender/README.md)

## English

English index:

- [README_en.md](README_en.md)
