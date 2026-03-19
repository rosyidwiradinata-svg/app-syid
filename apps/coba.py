import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

# Jika pakai Windows, set lokasi Tesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_image(image_path):
    # Baca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Preprocessing: Ubah ke hitam-putih dan tingkatkan kontras
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Ekstrak teks dengan OCR
    text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
    
    # Cari nama grup dan jumlah anggota
    lines = text.split("\n")
    group_name = "Tidak Diketahui"
    member_count = "Tidak Diketahui"

    for line in lines:
        if "grup" in line.lower() or "Group" in line:
            group_name = line.strip()
        elif "anggota" in line.lower() or "member" in line.lower():
            member_count = line.strip()

    return group_name, member_count

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        # Tampilkan gambar
        img = Image.open(file_path)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk)
        panel.image = img_tk
        
        # Proses OCR
        group_name, member_count = process_image(file_path)
        group_label.config(text=f"📌 Nama Grup: {group_name}")
        member_label.config(text=f"👥 Jumlah Anggota: {member_count}")

# GUI Tkinter
root = tk.Tk()
root.title("WhatsApp Group Scanner")
root.geometry("400x500")

# Label Judul
Label(root, text="🔍 Scan Nama Grup WhatsApp", font=("Arial", 14, "bold")).pack(pady=10)

# Panel Gambar
panel = Label(root)
panel.pack()

# Tombol Upload
Button(root, text="📂 Pilih Gambar", command=upload_image).pack(pady=10)

# Label Hasil
group_label = Label(root, text="📌 Nama Grup: -", font=("Arial", 12))
group_label.pack(pady=5)

member_label = Label(root, text="👥 Jumlah Anggota: -", font=("Arial", 12))
member_label.pack(pady=5)

# Jalankan GUI
root.mainloop()
