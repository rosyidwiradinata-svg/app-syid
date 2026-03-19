import tkinter as tk
from tkinter import messagebox, filedialog
import re  # Import untuk ekspresi reguler

def clean_phone_number(number):
    # Menghapus karakter non-numerik kecuali '+' dan menambahkan '+' di depan jika tidak ada
    number = re.sub(r'[^\d+]', '', number)  # Menghapus karakter non-numerik
    if not number.startswith('+'):
        number = '+' + number  # Menambahkan '+' jika tidak ada
    return number

def convert_txt_to_vcf_single(txt_file_path, contact_name):
    vcf_file_path = txt_file_path.replace('.txt', '.vcf')
    
    try:
        with open(txt_file_path, 'r') as txt_file, open(vcf_file_path, 'w') as vcf_file:
            lines = txt_file.readlines()
            contact_number = 1
            for line in lines:
                phone = line.strip()
                if phone:
                    cleaned_phone = clean_phone_number(phone)

                    if cleaned_phone and len(cleaned_phone) >= 10:
                        numbered_contact_name = f"{contact_name}{contact_number}"
                        contact_number += 1

                        # Mulai setiap kontak dengan header VCF
                        vcf_file.write("BEGIN:VCARD\n")
                        vcf_file.write("VERSION:3.0\n")
                        vcf_file.write(f"N:{numbered_contact_name}\n")
                        vcf_file.write(f"TEL:{cleaned_phone}\n")
                        vcf_file.write("END:VCARD\n")  # Tutup kontak per VCARD
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengonversi file: {e}")
        return None

    return vcf_file_path

def convert_to_vcf(admin_names, admin_numbers, navy_names, navy_numbers, vcf_file_path):
    # Membuat konten VCF
    vcf_content = ""
    
    for name, number in zip(admin_names, admin_numbers):
        vcf_content += (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{name}\n"
            f"TEL:{number}\n"
            "END:VCARD\n"
        )
        
    for name, number in zip(navy_names, navy_numbers):
        vcf_content += (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{name}\n"
            f"TEL:{number}\n"
            "END:VCARD\n"
        )

    # Menyimpan ke file VCF
    try:
        with open(vcf_file_path, 'w') as vcf_file:
            vcf_file.write(vcf_content)
        messagebox.showinfo("Sukses", f"File VCF berhasil dibuat: {vcf_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file VCF: {e}")

def save_vcf():
    # Mengambil nama dan nomor admin dari Text widget
    admin_text = admin_id_text.get("1.0", tk.END).strip().splitlines()
    admin_numbers = [clean_phone_number(num.strip()) for num in admin_text if num.strip()]
    admin_names = [f"Admin {i + 1}" for i in range(len(admin_numbers))]  # Nama admin berurutan

    # Mengambil nama dan nomor navy dari Text widget
    navy_text = navy_id_text.get("1.0", tk.END).strip().splitlines()
    navy_numbers = [clean_phone_number(num.strip()) for num in navy_text if num.strip()]
    navy_names = [f"Navy {i + 1}" for i in range(len(navy_numbers))]  # Nama navy berurutan
    
    vcf_file_name = file_name_entry.get().strip()
    
    if not vcf_file_name.endswith('.vcf'):
        vcf_file_name += '.vcf'  # Menambahkan ekstensi .vcf jika belum ada

    if not admin_numbers and not navy_numbers:
        messagebox.showwarning("Peringatan", "Masukkan setidaknya satu nomor.")
        return
    
    convert_to_vcf(admin_names, admin_numbers, navy_names, navy_numbers, vcf_file_name)

# Fungsi untuk memilih file dan mengonversi ke satu VCF
def select_files_single():
    contact_name = contact_name_entry_single.get().strip()
    if not contact_name:
        messagebox.showwarning("Warning", "Nama kontak tidak boleh kosong.")
        return
    
    txt_file_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
    if txt_file_paths:
        for txt_file_path in txt_file_paths:
            vcf_file_path = convert_txt_to_vcf_single(txt_file_path, contact_name)
            if vcf_file_path:
                messagebox.showinfo("Sukses", f"File VCF berhasil dibuat: {vcf_file_path}")

# Fungsi untuk memilih file dan mengonversi ke beberapa VCF
def select_files_multiple():
    contact_name = contact_name_entry_multiple.get().strip()
    if not contact_name:
        messagebox.showwarning("Warning", "Nama kontak tidak boleh kosong.")
        return
    
    txt_file_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
    if txt_file_paths:
        for txt_file_path in txt_file_paths:
            vcf_file_path = convert_txt_to_vcf_single(txt_file_path, contact_name)
            if vcf_file_path:
                messagebox.showinfo("Sukses", f"File VCF berhasil dibuat: {vcf_file_path}")

# Fungsi untuk membuat menu pilihan
def show_conversion_options():
    for widget in root.winfo_children():
        widget.destroy()
    
    author_label = tk.Label(root, text="Tools By Bangsyid CV", font=("Helvetica", 14, "italic"), fg='green', bg='lightgrey')
    author_label.pack(pady=5)

    title_label = tk.Label(root, text="Pilih Opsi Konversi", font=("Helvetica", 18, "bold"), fg='green', bg='lightgrey')
    title_label.pack(pady=10)

    multiple_button = tk.Button(root, text="Pecah TXT ke Beberapa VCF", command=setup_multiple_conversion, bg='lightgreen', font=("Helvetica", 12))
    multiple_button.pack(pady=5)

    single_button = tk.Button(root, text="Pecah TXT ke Satu VCF", command=setup_single_conversion, bg='lightgreen', font=("Helvetica", 12))
    single_button.pack(pady=5)

    tools_button = tk.Button(root, text="Tools Admin dan Navy", command=setup_tools, bg='lightgreen', font=("Helvetica", 12))
    tools_button.pack(pady=5)

    exit_button = tk.Button(root, text="Keluar", command=root.quit, bg='lightcoral', font=("Helvetica", 12))
    exit_button.pack(pady=10)

# Fungsi untuk menyiapkan antarmuka konversi ke satu VCF
def setup_single_conversion():
    for widget in root.winfo_children():
        widget.destroy()
    
    author_label = tk.Label(root, text="Tools By Bangsyid CV", font=("Helvetica", 14, "italic"), fg='green', bg='lightgrey')
    author_label.pack(pady=5)

    title_label = tk.Label(root, text="Pecah TXT ke Satu VCF", font=("Helvetica", 18, "bold"), fg='green', bg='lightgrey')
    title_label.pack(pady=10)

    instruction_label = tk.Label(root, text="Konversi file TXT berisi nomor telepon ke satu file VCF", bg='lightgrey', font=("Helvetica", 12))
    instruction_label.pack(pady=5)

    label = tk.Label(root, text="Masukkan Nama Kontak:", bg='lightgrey', font=("Helvetica", 12))
    label.pack(pady=10)

    global contact_name_entry_single
    contact_name_entry_single = tk.Entry(root, width=40, font=("Helvetica", 12))
    contact_name_entry_single.pack(pady=5)

    select_button = tk.Button(root, text="Pilih File untuk Satu VCF", command=select_files_single, bg='lightgreen', font=("Helvetica", 12))
    select_button.pack(pady=5)

    back_button = tk.Button(root, text="Kembali ke Menu Pilihan", command=show_conversion_options, bg='lightyellow', font=("Helvetica", 12))
    back_button.pack(pady=5)

# Fungsi untuk menyiapkan antarmuka konversi ke beberapa VCF
def setup_multiple_conversion():
    for widget in root.winfo_children():
        widget.destroy()
    
    author_label = tk.Label(root, text="Tools By Bangsyid CV", font=("Helvetica", 14, "italic"), fg='green', bg='lightgrey')
    author_label.pack(pady=5)

    title_label = tk.Label(root, text="Pecah TXT ke Beberapa VCF", font=("Helvetica", 18, "bold"), fg='green', bg='lightgrey')
    title_label.pack(pady=10)

    instruction_label = tk.Label(root, text="Konversi beberapa file TXT berisi nomor telepon ke beberapa file VCF", bg='lightgrey', font=("Helvetica", 12))
    instruction_label.pack(pady=5)

    label = tk.Label(root, text="Masukkan Nama Kontak:", bg='lightgrey', font=("Helvetica", 12))
    label.pack(pady=10)

    global contact_name_entry_multiple
    contact_name_entry_multiple = tk.Entry(root, width=40, font=("Helvetica", 12))
    contact_name_entry_multiple.pack(pady=5)

    select_button = tk.Button(root, text="Pilih File untuk Beberapa VCF", command=select_files_multiple, bg='lightgreen', font=("Helvetica", 12))
    select_button.pack(pady=5)

    back_button = tk.Button(root, text="Kembali ke Menu Pilihan", command=show_conversion_options, bg='lightyellow', font=("Helvetica", 12))
    back_button.pack(pady=5)

# Fungsi untuk menyiapkan antarmuka Tools
def setup_tools():
    for widget in root.winfo_children():
        widget.destroy()
    
    author_label = tk.Label(root, text="Tools By Bangsyid CV", font=("Helvetica", 14, "italic"), fg='green', bg='lightgrey')
    author_label.pack(pady=5)

    title_label = tk.Label(root, text="Tools Admin dan Navy", font=("Helvetica", 18, "bold"), fg='green', bg='lightgrey')
    title_label.pack(pady=10)

    instruction_label = tk.Label(root, text="Masukkan Nama dan Nomor untuk Admin dan Navy", bg='lightgrey', font=("Helvetica", 12))
    instruction_label.pack(pady=5)

    global admin_id_text, navy_id_text, file_name_entry
    admin_id_text = tk.Text(root, height=10, width=50, font=("Helvetica", 12))
    admin_id_text.pack(pady=5)
    admin_id_text.insert(tk.END, "Masukkan Nomor Admin (satu per baris)")

    navy_id_text = tk.Text(root, height=10, width=50, font=("Helvetica", 12))
    navy_id_text.pack(pady=5)
    navy_id_text.insert(tk.END, "Masukkan Nomor Navy (satu per baris)")

    file_name_entry = tk.Entry(root, width=40, font=("Helvetica", 12))
    file_name_entry.pack(pady=5)
    file_name_entry.insert(tk.END, "Masukkan Nama File VCF")

    save_button = tk.Button(root, text="Simpan VCF", command=save_vcf, bg='lightgreen', font=("Helvetica", 12))
    save_button.pack(pady=5)

    back_button = tk.Button(root, text="Kembali ke Menu Pilihan", command=show_conversion_options, bg='lightyellow', font=("Helvetica", 12))
    back_button.pack(pady=5)

# Membuat jendela utama
root = tk.Tk()
root.title("Konversi TXT ke VCF")
root.geometry("600x600")
root.configure(bg='lightgrey')  # Mengatur latar belakang jendela utama
show_conversion_options()  # Menampilkan menu pilihan saat pertama kali

# Menjalankan aplikasi
root.mainloop()
