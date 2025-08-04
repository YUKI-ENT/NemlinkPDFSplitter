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

def save_config(output_dir, exam_name):
    config = {
        "output_dir": output_dir,
        "exam_name": exam_name
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# GUI終了時に保存
def on_closing():
    output_dir = entry_output.get().strip()
    exam_name = entry_exam.get().strip() or "SAS検査"
    if output_dir:
        save_config(output_dir, exam_name)
    root.destroy()

def process_pdf(input_path, output_dir, exam_name):
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        today_str = datetime.today().strftime("%Y_%m_%d")
        serial = "0001"

        for i in range(0, total_pages, 4):
            writer = PdfWriter()
            for j in range(4):
                if i + j < total_pages:
                    writer.add_page(reader.pages[i + j])

            temp_pdf_path = output_dir / f"temp_{i//4 + 1}.pdf"
            with open(temp_pdf_path, "wb") as f:
                writer.write(f)

            with pdfplumber.open(str(temp_pdf_path)) as pdf:
                text = pdf.pages[0].extract_text()
                match = re.search(r"ID[:：]\s*(\d+)", text)
                id_number = match.group(1) if match else "unknown"

            new_name = f"{id_number}~{serial}~{today_str}~{exam_name}~RSB.pdf"
            temp_pdf_path.rename(output_dir / new_name)

        # 設定保存
        save_config(str(output_dir), exam_name)

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

def run():
    pdf_path = entry_pdf.get()
    out_dir = entry_output.get()
    exam = entry_exam.get().strip() or "SAS検査"
    if not pdf_path or not out_dir:
        messagebox.showwarning("入力不足", "PDFと出力先フォルダを指定してください。")
        return
    process_pdf(pdf_path, out_dir, exam)

def on_drop(event):
    filepath = event.data.strip("{}")
    if filepath.lower().endswith(".pdf"):
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, filepath)

# --- GUI構築 ---
root = TkinterDnD.Tk()
root.title("PDF分割 & IDリネームツール")
root.geometry("600x270")

tk.Label(root, text="PDFファイル：").pack(anchor="w", padx=10, pady=(10, 0))
entry_pdf = tk.Entry(root, width=70)
entry_pdf.pack(padx=10, fill="x")
entry_pdf.drop_target_register(DND_FILES)
entry_pdf.dnd_bind("<<Drop>>", on_drop)

tk.Button(root, text="ファイル選択", command=select_file).pack(pady=5)

tk.Label(root, text="出力先フォルダ：").pack(anchor="w", padx=10)
entry_output = tk.Entry(root, width=70)
entry_output.pack(padx=10, fill="x")
tk.Button(root, text="出力先を参照", command=select_output_dir).pack(pady=5)

tk.Label(root, text="検査名（例：SAS検査）：").pack(anchor="w", padx=10)
entry_exam = tk.Entry(root, width=40)
entry_exam.pack(padx=10)

# 設定ファイルから復元
config = load_config()
if "output_dir" in config:
    entry_output.insert(0, config["output_dir"])
if "exam_name" in config:
    entry_exam.insert(0, config["exam_name"])
else:
    entry_exam.insert(0, "SAS検査")

tk.Button(root, text="処理実行", command=run, bg="green", fg="white", height=2).pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
