import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def replace_in_file(file_path, search_texts):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Pecah input teks yang dicari menjadi list
        search_list = search_texts.splitlines()

        # Lakukan replace dengan string kosong untuk menghapus teks yang dicari
        for search_text in search_list:
            file_content = re.sub(search_text, '', file_content)  # Ganti dengan string kosong (hapus teks)

        # Menulis ulang konten yang sudah diganti
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_content)

        print(f"Updated: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def replace_in_folder(folder_path, search_texts, file_extension=".txt"):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(file_extension):  # Pilih file berdasarkan ekstensi
                file_path = os.path.join(root, file_name)
                replace_in_file(file_path, search_texts)

def select_folder():
    folder_path = filedialog.askdirectory()
    entry_folder.delete(0, tk.END)
    entry_folder.insert(0, folder_path)

def start_replacement():
    folder_path = entry_folder.get()
    search_texts = text_search.get("1.0", tk.END).strip()
    extension = entry_extension.get()

    if not folder_path or not search_texts or not extension:
        messagebox.showwarning("Peringatan", "Mohon lengkapi semua input!")
        return

    try:
        replace_in_folder(folder_path, search_texts, file_extension=extension)
        messagebox.showinfo("Sukses", "Penggantian teks selesai!")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Membuat jendela Tkinter
root = tk.Tk()
root.title("Hapus Teks di Banyak Dokumen")
root.geometry("500x350")

# Label dan input folder
label_folder = tk.Label(root, text="Pilih Folder:")
label_folder.pack(pady=5)
entry_folder = tk.Entry(root, width=50)
entry_folder.pack(pady=5)
button_browse = tk.Button(root, text="Browse", command=select_folder)
button_browse.pack(pady=5)

# Label dan input teks yang dicari (multiline Text widget)
label_search = tk.Label(root, text="Teks yang Dicari (satu baris per kata yang akan dihapus):")
label_search.pack(pady=5)
text_search = tk.Text(root, width=50, height=5)
text_search.pack(pady=5)

# Label dan input ekstensi file
label_extension = tk.Label(root, text="Ekstensi File (misal: .txt):")
label_extension.pack(pady=5)
entry_extension = tk.Entry(root, width=50)
entry_extension.pack(pady=5)
entry_extension.insert(0, ".txt")  # Default .txt

# Tombol untuk memulai proses replace
button_start = tk.Button(root, text="Mulai Penghapusan", command=start_replacement)
button_start.pack(pady=20)

# Menjalankan GUI
root.mainloop()
