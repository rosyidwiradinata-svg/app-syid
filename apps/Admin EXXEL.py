import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import re

def convert_to_vcf(admin_numbers, navy_numbers, kode):
    vcf = ""
    for i, number in enumerate(admin_numbers, start=1):
        vcf += f"""BEGIN:VCARD
VERSION:3.0
FN:Admin {kode}-{i}
TEL;TYPE=CELL:{number}
END:VCARD
"""
    for i, number in enumerate(navy_numbers, start=1):
        vcf += f"""BEGIN:VCARD
VERSION:3.0
FN:Navy {kode}-{i}
TEL;TYPE=CELL:{number}
END:VCARD
"""
    return vcf

def is_phone_number(value):
    return isinstance(value, str) and re.fullmatch(r'\d{6,}', value)

def split_by_label(column_data):
    admin = []
    navy = []
    current_list = None

    for val in column_data:
        val_str = str(val).strip()
        if val_str in ['管理', 'Admin']:
            current_list = admin
            continue
        elif val_str in ['水军', 'Navy']:
            current_list = navy
            continue

        if is_phone_number(val_str) and current_list is not None:
            current_list.append(val_str)

    return admin, navy

def process_file(file_path):
    df = pd.read_excel(file_path, header=None)
    df = df.dropna(how='all', axis=1)

    saved_files = []

    for col in df.columns:
        column_data = df[col].dropna().tolist()
        if not column_data:
            continue

        kode = f"{col+1:02d}BX"
        admin_numbers, navy_numbers = split_by_label(column_data)

        combined_vcf = convert_to_vcf(admin_numbers, navy_numbers, kode)

        base_dir = os.path.dirname(file_path)
        combined_file = os.path.join(base_dir, f"{kode}.vcf")
        with open(combined_file, "w") as f:
            f.write(combined_vcf)

        saved_files.append(combined_file)

    return saved_files

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not file_path:
        return
    try:
        saved_files = process_file(file_path)
        messagebox.showinfo("Selesai", f"VCF berhasil dibuat: {len(saved_files)} file.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("Excel to VCF Converter (Fix Admin/Navy Label)")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Pilih file Excel:")
label.pack(pady=10)

btn = tk.Button(frame, text="Browse File", command=browse_file)
btn.pack(pady=10)

root.mainloop()
