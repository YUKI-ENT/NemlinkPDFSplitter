import os
import re
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfReader, PdfWriter
import pdfplumber

CONFIG_FILE = "config.json"

def load_config():
    if Path(CONFIG_FILE).exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(output_dir, exam_name, pages_per_split):
    config = {
        "output_dir": output_dir,
        "exam_name": exam_name,
        "pages_per_split": pages_per_split,  # ▼追加
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# GUI終了時に保存
def on_closing():
    output_dir = entry_output.get().strip()
    exam_name = entry_exam.get().strip() or "SAS検査"
    pages = entry_pages.get().strip() or "4"
    try:
        pages_int = max(1, int(pages))
    except ValueError:
        pages_int = 4
    if output_dir:
        save_config(output_dir, exam_name, pages_int)
    root.destroy()

def process_pdf(input_path, output_dir, exam_name, pages_per_split):
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        today_str = datetime.today().strftime("%Y_%m_%d")

        for idx, i in enumerate(range(0, total_pages, pages_per_split), start=1):
            writer = PdfWriter()
            for j in range(pages_per_split):
                if i + j < total_pages:
                    writer.add_page(reader.pages[i + j])

            temp_pdf_path = output_dir / f"temp_{idx}.pdf"
            with open(temp_pdf_path, "wb") as f:
                writer.write(f)

            with pdfplumber.open(str(temp_pdf_path)) as pdf:
                text = pdf.pages[0].extract_text() or ""
                match = re.search(r"ID[:：]\s*(\d+)", text)
                id_number = match.group(1) if match else "unknown"

            # 連番を動的に（4桁ゼロ埋め）
            serial = f"{idx:04d}"

            # 同じIDでも衝突しないように
            new_name = f"{id_number}~{serial}~{today_str}~{exam_name}~RSB.pdf"
            temp_pdf_path.rename(output_dir / new_name)

        # 設定保存
        save_config(str(output_dir), exam_name, pages_per_split)

        messagebox.showinfo("完了", f"保存先：{output_dir}\n出力が完了しました！")

    except Exception as e:
        messagebox.showerror("エラー", str(e))

def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, filepath)

def select_output_dir():
    folder = filedialog.askdirectory()
    if folder:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, folder)
        # ここで保存
        pages = entry_pages.get().strip() or "4"
        try:
            pages_int = max(1, int(pages))
        except ValueError:
            pages_int = 4
        exam = entry_exam.get().strip() or "SAS検査"
        save_config(folder, exam, pages_int)
        

def run():
    pdf_path = entry_pdf.get()
    out_dir = entry_output.get()
    exam = entry_exam.get().strip() or "SAS検査"
    pages_str = entry_pages.get().strip() or "4"
    if not pdf_path or not out_dir:
        messagebox.showwarning("入力不足", "PDFと出力先フォルダを指定してください。")
        return
    try:
        pages = int(pages_str)
        if pages <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("入力エラー", "分割ページ数は1以上の整数を入力してください。")
        return
    process_pdf(pdf_path, out_dir, exam, pages)

def on_drop(event):
    filepath = event.data.strip("{}")
    if filepath.lower().endswith(".pdf"):
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, filepath)

# --- GUI構築 ---
root = TkinterDnD.Tk()
root.title("PDF分割 & IDリネームツール")
root.geometry("680x240")          # 少し横広に
root.minsize(640, 220)

main = tk.Frame(root)
main.pack(fill="both", expand=True, padx=10, pady=10)

# Entry列は横に伸びる
main.grid_columnconfigure(0, weight=0)
main.grid_columnconfigure(1, weight=1)   # ← ここが伸びる列
main.grid_columnconfigure(2, weight=0)

# 1行目: PDFファイル
tk.Label(main, text="PDFファイル：").grid(row=0, column=0, sticky="w", padx=(0,10), pady=(0,6))
entry_pdf = tk.Entry(main)
entry_pdf.grid(row=0, column=1, sticky="ew", pady=(0,6))
entry_pdf.drop_target_register(DND_FILES)
entry_pdf.dnd_bind("<<Drop>>", on_drop)
tk.Button(main, text="ファイル選択", command=select_file, width=14).grid(row=0, column=2, sticky="w", padx=(10,0), pady=(0,6))

# 2行目: 出力先フォルダ
tk.Label(main, text="出力先フォルダ：").grid(row=1, column=0, sticky="w", padx=(0,10), pady=6)
entry_output = tk.Entry(main)
entry_output.grid(row=1, column=1, sticky="ew", pady=6)
tk.Button(main, text="出力先を参照", command=select_output_dir, width=14).grid(row=1, column=2, sticky="w", padx=(10,0), pady=6)

# 3行目: 検査名（1行で完結）
tk.Label(main, text="検査名（例：SAS検査）：").grid(row=2, column=0, sticky="w", padx=(0,10), pady=6)
entry_exam = tk.Entry(main)
entry_exam.grid(row=2, column=1, columnspan=2, sticky="ew", pady=6)  # ← 右まで広げて改行させない

# 4行目: 分割ページ数（ラベルとボックスを横並び）
tk.Label(main, text="分割ページ数：").grid(row=3, column=0, sticky="w", padx=(0,10), pady=6)
entry_pages = tk.Entry(main, width=8)
entry_pages.grid(row=3, column=1, sticky="w", pady=6)
entry_pages.insert(0, "4")  # デフォルト4

# 5行目: 実行ボタン（常に見える位置に）
run_btn = tk.Button(main, text="処理実行", command=run, bg="green", fg="white", font=("Meiryo", 11, "bold"),width=15)
run_btn.grid(row=4, column=0, columnspan=3, pady=(15,0))

# 設定ファイルから復元
config = load_config()
if "output_dir" in config:
    entry_output.insert(0, config["output_dir"])
if "exam_name" in config:
    entry_exam.insert(0, config["exam_name"])
else:
    entry_exam.insert(0, "SAS検査")
if "pages_per_split" in config:
    entry_pages.delete(0, tk.END)
    entry_pages.insert(0, str(config["pages_per_split"]))

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()