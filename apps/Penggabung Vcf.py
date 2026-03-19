import tkinter as tk
from tkinter import filedialog, messagebox
import os

def gabungkan_vcf(file1, file2, nama_output):
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            isi1 = f1.read()
            isi2 = f2.read()
        
        hasil = isi1.strip() + "\n" + isi2.strip()
        lokasi_simpan = filedialog.asksaveasfilename(defaultextension=".vcf", initialfile=nama_output, filetypes=[("VCF Files", "*.vcf")])
        
        if lokasi_simpan:
            with open(lokasi_simpan, 'w', encoding='utf-8') as f_out:
                f_out.write(hasil)
            messagebox.showinfo("Sukses", f"File berhasil disimpan sebagai:\n{lokasi_simpan}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menggabungkan file:\n{e}")

def pilih_file1():
    file = filedialog.askopenfilename(filetypes=[("VCF Files", "*.vcf")])
    if file:
        entry_file1.delete(0, tk.END)
        entry_file1.insert(0, file)

def pilih_file2():
    file = filedialog.askopenfilename(filetypes=[("VCF Files", "*.vcf")])
    if file:
        entry_file2.delete(0, tk.END)
        entry_file2.insert(0, file)

def mulai_penggabungan():
    file1 = entry_file1.get()
    file2 = entry_file2.get()
    nama_output = entry_output.get().strip()

    if not file1 or not file2 or not nama_output:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
        return
    
    gabungkan_vcf(file1, file2, nama_output)

# GUI
root = tk.Tk()
root.title("Penggabung File VCF")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="File VCF Pertama:").pack(pady=(10, 0))
entry_file1 = tk.Entry(root, width=40)
entry_file1.pack()
tk.Button(root, text="Pilih File", command=pilih_file1).pack(pady=5)

tk.Label(root, text="File VCF Kedua:").pack(pady=(10, 0))
entry_file2 = tk.Entry(root, width=40)
entry_file2.pack()
tk.Button(root, text="Pilih File", command=pilih_file2).pack(pady=5)

tk.Label(root, text="Nama File Output (tanpa ekstensi):").pack(pady=(10, 0))
entry_output = tk.Entry(root, width=30)
entry_output.pack()

tk.Button(root, text="Gabungkan dan Simpan", command=mulai_penggabungan, bg="green", fg="white").pack(pady=15)

root.mainloop()
