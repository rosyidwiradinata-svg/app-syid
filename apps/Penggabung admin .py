import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def buat_vcf_admin(nama, nomor):
    return f"""BEGIN:VCARD
VERSION:3.0
FN:{nama}
TEL;TYPE=CELL:{nomor}
END:VCARD
"""

def tampilkan_form_nomor(nama_dasar, callback):
    # Jendela input multiline
    input_window = tk.Toplevel()
    input_window.title("Masukkan Nomor Admin")
    input_window.geometry("400x300")

    label = tk.Label(input_window, text="Masukkan beberapa nomor admin, satu per baris:")
    label.pack(pady=5)

    text_area = tk.Text(input_window, height=12, width=50)
    text_area.pack(padx=10, pady=10)

    def proses():
        isi = text_area.get("1.0", tk.END).strip()
        input_window.destroy()
        callback(nama_dasar, isi)

    btn_kirim = tk.Button(input_window, text="Lanjutkan", command=proses)
    btn_kirim.pack(pady=5)

def proses_data_admin(nama_dasar, input_nomor):
    nomor_list = [nomor.strip() for nomor in input_nomor.strip().splitlines() if nomor.strip()]
    if not nomor_list:
        messagebox.showwarning("Perhatian", "Tidak ada nomor yang valid!")
        return

    vcf_entries = []
    for i, nomor in enumerate(nomor_list, start=1):
        nama_lengkap = f"{nama_dasar} {i}"
        vcf_entries.append(buat_vcf_admin(nama_lengkap, nomor))

    target_file_paths = filedialog.askopenfilenames(
        title="Pilih file VCF untuk ditambahkan Admin",
        filetypes=[("VCF Files", "*.vcf")]
    )

    if not target_file_paths:
        messagebox.showwarning("Perhatian", "Tidak ada file target yang dipilih!")
        return

    try:
        for target_path in target_file_paths:
            with open(target_path, "r", encoding="utf-8") as target_file:
                isi_lama = target_file.read().strip()

            isi_baru = isi_lama + "\n" + "\n".join(vcf_entries)

            with open(target_path, "w", encoding="utf-8") as output_file:
                output_file.write(isi_baru.strip())

        messagebox.showinfo("Sukses", "Semua admin berhasil ditambahkan ke file VCF!")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

def tambahkan_admin_ke_vcf():
    nama_dasar = simpledialog.askstring("Nama Dasar", "Masukkan nama dasar untuk admin (misal: Contoh):")
    if not nama_dasar:
        messagebox.showwarning("Perhatian", "Nama dasar tidak dimasukkan!")
        return

    tampilkan_form_nomor(nama_dasar, proses_data_admin)

# GUI
root = tk.Tk()
root.title("Tambahkan Admin ke File VCF")
root.geometry("400x200")

btn = tk.Button(root, text="Tambah Admin Otomatis ke File VCF", command=tambahkan_admin_ke_vcf)
btn.pack(pady=30)

root.mainloop()
