import tkinter as tk
from tkinter import filedialog, messagebox
import os

def split_file():
    try:
        file_path = filedialog.askopenfilename(title="Pilih File Teks", filetypes=[("File Teks", "*.txt")])
        if not file_path:
            return

        # Ambil nama file tanpa ekstensi dan direktori
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        directory = os.path.dirname(file_path)

        # Ambil jumlah baris per file dari input
        lines_per_file = int(lines_entry.get())

        # Baca file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Pisahkan dan simpan file
        for i in range(0, len(lines), lines_per_file):
            output_file_name = os.path.join(directory, f"{base_name}_{i // lines_per_file + 1}.txt")
            with open(output_file_name, 'w') as split_file:
                split_file.writelines(lines[i:i + lines_per_file])

        messagebox.showinfo("Sukses", "File berhasil dipisahkan!")

    except ValueError:
        messagebox.showerror("Error", "Silakan masukkan angka yang valid untuk jumlah baris.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the main application window
root = tk.Tk()
root.title("Pemecah File Teks")
root.geometry("400x200")  # Set ukuran jendela

# Create and place the input fields and buttons using grid
tk.Label(root, text="Jumlah baris per file:").grid(row=0, column=0, padx=10, pady=10)
lines_entry = tk.Entry(root, width=10)
lines_entry.grid(row=0, column=1, padx=10, pady=10)

split_button = tk.Button(root, text="Pisahkan File", command=split_file)
split_button.grid(row=1, columnspan=2, pady=20)

# Start the GUI loop
root.mainloop()
