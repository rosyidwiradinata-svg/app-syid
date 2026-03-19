import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

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

    # Meminta pengguna memasukkan nama dasar file
    base_name = simpledialog.askstring("Nama Dasar File", "Masukkan nama dasar untuk file:")
    if not base_name:
        messagebox.showerror("Error", "Nama dasar tidak boleh kosong")
        return

    # Meminta angka awal untuk penomoran
    try:
        start_number = int(simpledialog.askstring("Nomor Awal", "Masukkan nomor awal untuk penomoran:"))
    except (TypeError, ValueError):
        messagebox.showerror("Error", "Nomor awal tidak valid")
        return

    # Mengubah nama file yang dipilih dengan penomoran otomatis
    counter = start_number
    try:
        for file_path in file_paths:
            # Mengambil ekstensi file
            ext = os.path.splitext(file_path)[1]
            # Membuat nama baru dengan penomoran di belakang
            new_name = f"{base_name}{counter}{ext}"
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)
            counter += 1
        messagebox.showinfo("Sukses", "Nama file berhasil diubah")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengubah nama file: {e}")

# Membuat antarmuka menggunakan Tkinter
root = tk.Tk()
root.title("Batch Rename Document Files with Numbering")

# Tombol untuk memulai proses rename
button_rename = tk.Button(root, text="Pilih Dokumen dan Ubah Nama", command=rename_multiple_files)
button_rename.pack(padx=10, pady=10)

root.mainloop()
