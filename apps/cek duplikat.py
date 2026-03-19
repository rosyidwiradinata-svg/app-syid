import tkinter as tk
from tkinter import filedialog, messagebox

def cek_duplikat():
    # Ambil teks dari input
    data = text_input.get("1.0", tk.END).strip().split("\n")

    # Filter hanya nomor unik dan cek duplikat
    seen = set()
    duplicates = set()
    
    for nomor in data:
        nomor = nomor.strip()
        if nomor in seen:
            duplicates.add(nomor)
        else:
            seen.add(nomor)

    # Tampilkan hasil
    if duplicates:
        hasil_var.set("Nomor Duplikat Ditemukan:\n" + "\n".join(duplicates))
    else:
        hasil_var.set("Semua nomor unik, tidak ada duplikat.")

def hapus_duplikat():
    # Ambil teks dari input
    data = text_input.get("1.0", tk.END).strip().split("\n")

    # Hapus duplikat, urutan tetap sama
    unique_numbers = list(dict.fromkeys([nomor.strip() for nomor in data]))

    # Tampilkan hasil ke input kembali
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, "\n".join(unique_numbers))

    hasil_var.set("Duplikat telah dihapus! Hanya nomor unik yang tersisa.")

def load_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, file.read())

# GUI Tkinter
root = tk.Tk()
root.title("Pengecek & Penghapus Nomor Duplikat")

# Text input
text_input = tk.Text(root, height=10, width=50)
text_input.pack(pady=10)

# Tombol cek duplikat
btn_cek = tk.Button(root, text="Cek Duplikat", command=cek_duplikat)
btn_cek.pack()

# Tombol hapus duplikat
btn_hapus = tk.Button(root, text="Hapus Duplikat", command=hapus_duplikat)
btn_hapus.pack()

# Tombol Load File
btn_load = tk.Button(root, text="Muat dari File", command=load_from_file)
btn_load.pack()

# Label hasil
hasil_var = tk.StringVar()
hasil_label = tk.Label(root, textvariable=hasil_var, fg="red", justify="left")
hasil_label.pack(pady=10)

# Jalankan aplikasi
root.mainloop()
