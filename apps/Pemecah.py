import tkinter as tk
from tkinter import filedialog, messagebox
import re  # Import modul regular expression
import os  # Untuk operasi file dan path

# Fungsi untuk mengonversi file TXT ke VCF dengan pemecahan kontak per file sesuai input
def convert_txt_to_vcf(txt_file_path, contact_name, contacts_per_file, start_number, file_base_name):
    output_folder = os.path.join(os.path.dirname(txt_file_path), "VCF_Files")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    try:
        with open(txt_file_path, 'r') as txt_file:
            lines = txt_file.readlines()
            contact_number = 1
            file_number = start_number
            vcf_file = None

            for index, line in enumerate(lines):
                phone = line.strip()
                if phone:
                    cleaned_phone = re.sub(r'\D', '', phone)

                    if cleaned_phone:
                        formatted_phone = f"+{cleaned_phone}" if not cleaned_phone.startswith('+') else cleaned_phone
                        numbered_contact_name = f"{contact_name}{contact_number}"
                        
                        if contact_number % contacts_per_file == 1:
                            if vcf_file:
                                vcf_file.close()
                            vcf_file_path = os.path.join(output_folder, f"{file_base_name}{file_number}.vcf")
                            vcf_file = open(vcf_file_path, 'w')
                            file_number += 1

                        vcf_file.write("BEGIN:VCARD\n")
                        vcf_file.write(f"N:{numbered_contact_name}\n")
                        vcf_file.write(f"TEL:{formatted_phone}\n")
                        vcf_file.write("END:VCARD\n")

                        contact_number += 1
            
            if vcf_file:
                vcf_file.close()

        messagebox.showinfo("Sukses", f"File VCF berhasil dibuat dalam folder: {output_folder}")
        return output_folder
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengonversi file: {e}")
        return None

def select_files():
    contact_name = contact_name_entry.get().strip()
    contacts_per_file = contacts_per_file_entry.get().strip()
    file_base_name = file_name_entry.get().strip()
    start_number = start_number_entry.get().strip()

    if not contact_name:
        messagebox.showwarning("Warning", "Nama kontak tidak boleh kosong.")
        return
    
    if not contacts_per_file.isdigit() or int(contacts_per_file) <= 0:
        messagebox.showwarning("Warning", "Jumlah kontak per file harus berupa angka positif.")
        return

    if not start_number.isdigit() or int(start_number) < 1:
        messagebox.showwarning("Warning", "Angka mulai harus berupa angka positif dan lebih besar dari nol.")
        return
    
    if not file_base_name:
        messagebox.showwarning("Warning", "Nama file tidak boleh kosong.")
        return

    contacts_per_file = int(contacts_per_file)
    start_number = int(start_number)
    
    txt_file_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
    if txt_file_paths:
        for txt_file_path in txt_file_paths:
            output_folder = convert_txt_to_vcf(txt_file_path, contact_name, contacts_per_file, start_number, file_base_name)
            if output_folder:
                messagebox.showinfo("Sukses", f"File VCF berhasil dibuat dalam folder: {output_folder}")

# Membuat antarmuka grafis
def create_gui():
    root = tk.Tk()
    root.title("Konverter Kontak ke VCF")
    root.geometry("400x500")

    # Menambahkan padding ke semua elemen menggunakan grid manager
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Frame utama
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.grid(sticky="nsew")

    # Menambahkan label untuk menyebutkan pembuat alat
    author_label = tk.Label(main_frame, text="Tools By Bangsyid CV", font=("Arial", 12, "italic"))
    author_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Menambahkan label instruksi di awal menu
    title_label = tk.Label(main_frame, text="Pecah TXT ke VCF", font=("Arial", 16, "bold"))
    title_label.grid(row=1, column=0, columnspan=2, pady=10)

    instruction_label = tk.Label(main_frame, text="Konversi file TXT berisi nomor telepon ke VCF")
    instruction_label.grid(row=2, column=0, columnspan=2, pady=5)

    # Input untuk nama kontak
    label = tk.Label(main_frame, text="Masukkan Nama Kontak:")
    label.grid(row=3, column=0, sticky="w", pady=5)

    global contact_name_entry
    contact_name_entry = tk.Entry(main_frame, width=40)
    contact_name_entry.grid(row=3, column=1, pady=5)

    # Input untuk jumlah kontak per file
    contacts_per_file_label = tk.Label(main_frame, text="Jumlah Kontak per File:")
    contacts_per_file_label.grid(row=4, column=0, sticky="w", pady=5)

    global contacts_per_file_entry
    contacts_per_file_entry = tk.Entry(main_frame, width=40)
    contacts_per_file_entry.grid(row=4, column=1, pady=5)

    # Input untuk nama file dasar
    file_name_label = tk.Label(main_frame, text="Nama File Dasar:")
    file_name_label.grid(row=5, column=0, sticky="w", pady=5)

    global file_name_entry
    file_name_entry = tk.Entry(main_frame, width=40)
    file_name_entry.grid(row=5, column=1, pady=5)

    # Input untuk angka mulai
    start_number_label = tk.Label(main_frame, text="Angka Mulai untuk Penamaan:")
    start_number_label.grid(row=6, column=0, sticky="w", pady=5)

    global start_number_entry
    start_number_entry = tk.Entry(main_frame, width=40)
    start_number_entry.grid(row=6, column=1, pady=5)

    # Tombol untuk memilih file
    select_button = tk.Button(main_frame, text="Pilih File", command=select_files)
    select_button.grid(row=7, column=0, columnspan=2, pady=10)

    # Tombol keluar
    exit_button = tk.Button(main_frame, text="Keluar", command=root.quit)
    exit_button.grid(row=8, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
