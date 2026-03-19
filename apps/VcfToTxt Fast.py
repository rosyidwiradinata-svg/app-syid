import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def vcf_to_txt():
    # Dialog untuk memilih beberapa file VCF
    file_paths = filedialog.askopenfilenames(title="Pilih file VCF", filetypes=[("VCF Files", "*.vcf")])
    
    if not file_paths:
        messagebox.showwarning("Perhatian", "Tidak ada file yang dipilih!")
        return

    # Meminta nama dasar file dan nomor awal
    base_name = simpledialog.askstring("Nama File", "Masukkan nama dasar untuk file TXT:", initialvalue="NamaFile")
    if not base_name:
        messagebox.showwarning("Perhatian", "Nama dasar file tidak boleh kosong!")
        return
    
    try:
        start_number = simpledialog.askinteger("Nomor Awal", "Mulai dari nomor berapa?", initialvalue=1)
        if start_number is None:
            messagebox.showwarning("Perhatian", "Nomor awal harus diisi!")
            return
        
        # Konversi setiap file VCF ke TXT
        current_number = start_number
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
            
            # Menentukan nama file TXT berdasarkan nama dasar dan nomor urut
            directory = os.path.dirname(file_path)
            save_path = os.path.join(directory, f"{base_name}{current_number}.txt")
            
            # Menyimpan nomor telepon ke file TXT
            with open(save_path, "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(phone_numbers))
            
            # Memberi informasi untuk setiap file yang berhasil dikonversi
            messagebox.showinfo("Sukses", f"Nomor telepon berhasil dikonversi dari {os.path.basename(file_path)} ke {save_path}")
            
            current_number += 1  # Menambah nomor untuk file berikutnya
    
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
