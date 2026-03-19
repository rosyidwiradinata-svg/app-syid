import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def vcf_to_txt():
    # Dialog untuk memilih beberapa file VCF
    file_paths = filedialog.askopenfilenames(title="Pilih file VCF", filetypes=[("VCF Files", "*.vcf")])
    
    if not file_paths:
        messagebox.showwarning("Perhatian", "Tidak ada file yang dipilih!")
        return
    
    try:
        for file_path in file_paths:
            # Membaca file VCF dan mengekstrak nomor telepon
            phone_numbers = []
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()  # Hilangkan spasi tambahan
                    if line.startswith("TEL:"):
                        # Mengambil hanya nomor telepon, menghapus segala sesuatu setelah ";"
                        phone = line.replace("TEL:", "").split(";")[0].strip()
                        phone_numbers.append(phone)
            
            # Pastikan ada nomor telepon yang diekstrak
            if not phone_numbers:
                messagebox.showinfo("Info", f"Tidak ada nomor telepon yang ditemukan dalam file {os.path.basename(file_path)}.")
                continue
            
            # Meminta nama baru untuk file TXT
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            new_name = simpledialog.askstring("Nama File", f"Masukkan nama untuk file TXT (default: {base_name}):", initialvalue=base_name)
            if not new_name:
                new_name = base_name
            
            # Simpan file TXT di direktori yang sama dengan file VCF
            directory = os.path.dirname(file_path)
            save_path = os.path.join(directory, f"{new_name}.txt")
            
            # Menyimpan nomor telepon ke file TXT
            with open(save_path, "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(phone_numbers))
            
            # Memberi informasi untuk setiap file yang berhasil dikonversi
            messagebox.showinfo("Sukses", f"Nomor telepon berhasil dikonversi dari {os.path.basename(file_path)} ke {save_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Membuat antarmuka dengan Tkinter
root = tk.Tk()
root.title("Konversi VCF ke TXT")
root.geometry("400x200")

# Tombol untuk mengonversi beberapa file VCF ke TXT
button_convert = tk.Button(root, text="Konversi VCF ke TXT", command=vcf_to_txt)
button_convert.pack(pady=20)

root.mainloop()
