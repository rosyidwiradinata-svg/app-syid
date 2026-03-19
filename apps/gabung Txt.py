import tkinter as tk
from tkinter import filedialog, messagebox
import chardet  # Library untuk deteksi encoding

def detect_encoding(filepath):
    """Mendeteksi encoding file untuk memastikan semua teks bisa dibaca."""
    with open(filepath, 'rb') as f:
        rawdata = f.read(100000)  # Baca sebagian data untuk deteksi
    result = chardet.detect(rawdata)
    return result['encoding'] if result['encoding'] else 'utf-8'

def gabungkan_file():
    filepaths = filedialog.askopenfilenames(
        title="Pilih File Teks",
        filetypes=[("File Teks", "*.txt")]
    )
    
    if not filepaths:
        return  

    savepath = filedialog.asksaveasfilename(
        title="Simpan Sebagai",
        defaultextension=".txt",
        filetypes=[("File Teks", "*.txt")]
    )
    
    if not savepath:
        return  

    try:
        with open(savepath, 'w', encoding='utf-8') as outfile:
            for filepath in filepaths:
                encoding = detect_encoding(filepath)  # Deteksi encoding file
                with open(filepath, 'r', encoding=encoding, errors='replace') as infile:
                    for line in infile:
                        outfile.write(line)  
                outfile.write("\n")  # Tambahkan baris baru antar file
        
        messagebox.showinfo("Sukses", f"File berhasil digabungkan ke:\n{savepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# GUI Tkinter
root = tk.Tk()
root.title("Penggabung File Teks")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Gabungkan beberapa file teks menjadi satu.")
label.pack(pady=5)

button = tk.Button(frame, text="Gabungkan File", command=gabungkan_file)
button.pack(pady=5)

root.mainloop()
