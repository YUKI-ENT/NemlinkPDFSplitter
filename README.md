# NemLinkPDFSplitter

Teijin社のNemLinkサービスからダウンロードしたCPAP概要レポートPDFを、**患者IDごとに4ページずつ分割し、RS_Baseでの自動ファイリング名にリネームして保存**するWindows用ツールです。

このような1人4ページのレポートです。

![report](https://github.com/user-attachments/assets/f0671e58-9e37-4265-a589-c8ea3af51b8f)

---

## ✅ 主な機能

- PDFを4ページ単位で分割（各患者1レポート）
- PDFからIDを自動抽出
- RSBaseの自動ファイリング名でファイル名をリネーム  
  例：`12345~0001~2025_08_01~SAS検査~RSB.pdf`
- 検査名や出力フォルダをGUI上で入力・保存可能
- PDFファイルのドラッグ＆ドロップ対応（`PDFファイル`のテキストボックスにドラッグドロップできます）
- `.exe` 形式で配布・実行可能（PyInstallerでpythonソースから生成することも可能です）
- レジストリは読み書きしませんので、アンインストールするときはexeファイルの削除でOKです

---

## 🖥️ 動作環境

- Windows 11 / 10

---

## 🚀 起動方法
1. [Release](https://github.com/YUKI-ENT/NemlinkPDFSplitter/releases) から`PDFSplitter.exe`をダウンロード
2. `PDFSplitter.exe`を任意のフォルダに配置し実行するだけです。
![pdfsplitter_gui](https://github.com/user-attachments/assets/d0aed9dc-a732-42cd-be4e-885ad68ffe86)
3. ネムリンクでは、ログイン後全患者を選択 → `レポート印刷` を押すと全患者のデータが連結されたPDFがダウンロードできます。 

