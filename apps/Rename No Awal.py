import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)

# Fungsi untuk memvalidasi dan membersihkan nama file
def clean_filename(name):
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        name = name.replace(char, '_')  # Ganti karakter tidak valid dengan '_'
    return name.strip()  # Hapus spasi di awal/akhir nama

def rename_multiple_files():
    # Membuka dialog untuk memilih file dokumen
    file_paths = filedialog.askopenfilenames(
        title="Pilih File Dokumen",
        filetypes=[
            ("Text Files", "*.txt"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Excel Files", "*.xlsx"),
            ("VCF Files", "*.vcf"),
            ("All Document Files", "*.txt;*.pdf;*.docx;*.xlsx;*.vcf")
        ]
    )
    
    if not file_paths:
        messagebox.showerror("Error", "Tidak ada file yang dipilih")
        return

    # Meminta nama pertama (tetap)
    name_part1 = simpledialog.askstring("Nama Pertama", "Masukkan nama pertama (Tetap):")
    if not name_part1:
        messagebox.showerror("Error", "Nama pertama tidak boleh kosong")
        return
    name_part1 = clean_filename(name_part1)

    # Meminta angka awal untuk penomoran
    try:
        start_number = int(simpledialog.askstring("Nomor Awal", "Masukkan nomor awal untuk penomoran:"))
    except (TypeError, ValueError):
        messagebox.showerror("Error", "Nomor awal tidak valid")
        return

    # Meminta nama kedua (tetap)
    name_part2 = simpledialog.askstring("Nama Kedua", "Masukkan nama kedua (Tetap):")
    if not name_part2:
        messagebox.showerror("Error", "Nama kedua tidak boleh kosong")
        return
    name_part2 = clean_filename(name_part2)

    # Mengubah nama file yang dipilih
    counter = start_number
    try:
        for file_path in file_paths:
            # Mengambil ekstensi file
            ext = os.path.splitext(file_path)[1]
            # Membuat nama baru
            new_name = f"{name_part1}{counter}{name_part2}{ext}"
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            logging.info(f"Renaming: {file_path} -> {new_path}")
            os.rename(file_path, new_path)
            counter += 1
        messagebox.showinfo("Sukses", "Nama file berhasil diubah")
    except Exception as e:
        logging.error(f"Error renaming file: {e}")
        messagebox.showerror("Error", f"Gagal mengubah nama file: {e}")

# Membuat antarmuka menggunakan Tkinter
root = tk.Tk()
root.title("Batch Rename Document Files with Custom Name and Numbering")

# Tombol untuk memulai proses rename
button_rename = tk.Button(root, text="Pilih Dokumen dan Ubah Nama", command=rename_multiple_files)
button_rename.pack(padx=10, pady=10)

root.mainloop()
