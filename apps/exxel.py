import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pandas as pd
import os
import re

def convert_to_vcf(admin_numbers, navy_numbers, custom_numbers, kode, custom_label):
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
    if custom_numbers and custom_label:
        for i, number in enumerate(custom_numbers, start=1):
            vcf += f"""BEGIN:VCARD
VERSION:3.0
FN:{custom_label} {kode}-{i}
TEL;TYPE=CELL:{number}
END:VCARD
"""
    return vcf

def is_phone_number(value):
    """Cek apakah value string adalah nomor telepon minimal 6 digit angka."""
    return isinstance(value, str) and re.fullmatch(r'\d{6,}', value.strip())

def split_by_label(column_data):
    admin = []
    navy = []
    custom = []

    # Status: 0 = belum mulai, 1 = admin, 2 = navy, 3 = custom
    state = 0

    for val in column_data:
        val_str = str(val).strip()
        
        # Cek label admin
        if val_str in ['管理', 'Admin']:
            state = 1
            continue
        # Cek label navy
        elif val_str in ['水军', 'Navy']:
            state = 2
            continue
        
        if is_phone_number(val_str):
            if state == 1:
                admin.append(val_str)
            elif state == 2:
                navy.append(val_str)
            elif state == 3:
                custom.append(val_str)
        else:
            # Jika bukan nomor dan state sudah di Navy, kemungkinan sudah ke custom
            if state == 2 and len(navy) > 0:
                # Setelah label Navy dan ada nomor Navy, pindah ke state custom
                state = 3
            # Abaikan baris bukan nomor saat di custom juga
            # Jadi kita tidak mengubah list jika baris bukan nomor

    return admin, navy, custom

def process_file(file_path):
    df = pd.read_excel(file_path, header=None)
    df = df.dropna(how='all', axis=1)
    saved_files = []

    # Cek dulu apakah ada minimal 1 kolom yang punya kontak custom
    has_custom = False
    for col in df.columns:
        column_data = df[col].dropna().tolist()
        if not column_data:
            continue
        _, _, custom = split_by_label(column_data)
        if custom:
            has_custom = True
            break

    # Jika ada kontak custom di salah satu kolom, minta input custom_label sekali saja
    custom_label = ""
    if has_custom:
        custom_label = simpledialog.askstring(
            "Nama Kontak Custom",
            "Ada kontak tambahan setelah Navy di beberapa kolom. Mau dinamai apa bagian ini?"
        )
        if not custom_label or custom_label.strip() == "":
            messagebox.showerror("Error", "Nama kontak custom tidak boleh kosong.")
            return

    # Proses tiap kolom pakai custom_label yang sama
    for col in df.columns:
        column_data = df[col].dropna().tolist()
        if not column_data:
            continue

        kode = f"{col+1:02d}BX"
        admin, navy, custom = split_by_label(column_data)

        vcf = convert_to_vcf(admin, navy, custom, kode, custom_label)
        file_out = os.path.join(os.path.dirname(file_path), f"{kode}.vcf")

        with open(file_out, "w", encoding="utf-8") as f:
            f.write(vcf)
        saved_files.append(file_out)

    return saved_files

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not file_path:
        return
    try:
        files = process_file(file_path)
        messagebox.showinfo("Selesai", f"VCF berhasil dibuat: {len(files)} file.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("Excel to VCF (Admin / Navy / Custom Label)")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Pilih file Excel:")
label.pack(pady=10)

btn = tk.Button(frame, text="Browse File", command=browse_file)
btn.pack(pady=10)

root.mainloop()
