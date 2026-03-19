import tkinter as tk
from tkinter import filedialog, messagebox
import chardet
import os

def detect_encoding(filepath):
    """Deteksi encoding file untuk pembacaan aman."""
    with open(filepath, 'rb') as f:
        rawdata = f.read(100000)
    result = chardet.detect(rawdata)
    return result['encoding'] if result['encoding'] else 'utf-8'

def gabungkan_file():
    filepaths = filedialog.askopenfilenames(
        title="Pilih File",
        filetypes=[("Semua File Teks", "*.txt *.vcf")]
    )
    
    if not filepaths:
        return

    ext = os.path.splitext(filepaths[0])[1].lower()  # Ambil ekstensi file pertama
    savepath = filedialog.asksaveasfilename(
        title="Simpan Sebagai",
        defaultextension=ext,
        filetypes=[("File Hasil Gabungan", f"*{ext}")]
    )
    
    if not savepath:
        return

    try:
        with open(savepath, 'w', encoding='utf-8') as outfile:
            for filepath in filepaths:
                encoding = detect_encoding(filepath)
                with open(filepath, 'r', encoding=encoding, errors='replace') as infile:
                    content = infile.read()
                    if ext == '.vcf':
                        content = content.strip()
                    outfile.write(content)
                    outfile.write("\n")  # Tambah newline antar file

        messagebox.showinfo("Sukses", f"File berhasil digabungkan ke:\n{savepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# GUI Tkinter
root = tk.Tk()
root.title("Penggabung File Teks / VCF")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Gabungkan beberapa file teks atau VCF menjadi satu.")
label.pack(pady=5)

button = tk.Button(frame, text="Gabungkan File", command=gabungkan_file)
button.pack(pady=5)

root.mainloop()
