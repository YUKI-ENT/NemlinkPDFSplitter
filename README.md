# NemLinkPDFSplitter

Teijin社のNemLinkサービスからダウンロードしたCPAP概要レポートPDFを、**患者IDごとに4ページずつ分割し、RS_Base（レセプトソフト）での自動ファイリングに適したファイル名にリネームして保存**するWindows用ツールです。

---

## ✅ 主な機能

- PDFを4ページ単位で分割（各患者1レポート）
- PDFからIDを自動抽出
- RSBaseの自動ファイリング名でファイル名をリネーム  
  例：`12345~0001~2025_08_01~SAS検査~RSB.pdf`
- 検査名や出力フォルダをGUI上で入力・保存可能
- PDFファイルのドラッグ＆ドロップ対応
- `.exe` 形式で配布・実行可能（PyInstallerでpythonソースから生成することも可能です）

---

## 🖥️ 動作環境

- Windows 11 / 10

---

## 🚀 起動方法

### 1. `PDFSplitter.exe`を任意のフォルダに配置します。
![pdfsplitter_gui](https://github.com/user-attachments/assets/d0aed9dc-a732-42cd-be4e-885ad68ffe86)



#### 必要パッケージをインストール

```bash
pip install -r requirements.txt
