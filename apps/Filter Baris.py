import os
from tkinter import Tk, filedialog, messagebox, simpledialog


def select_files():
    # Dialog untuk memilih beberapa file
    file_paths = filedialog.askopenfilenames(title="Pilih File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_paths:
        ask_line_limit(file_paths)


def ask_line_limit(file_paths):
    # Meminta pengguna menentukan batas baris
    line_limit = simpledialog.askinteger(
        "Input",
        "Masukkan jumlah baris yang ingin disimpan:",
        minvalue=1,
    )
    if line_limit:
        process_files(file_paths, line_limit)


def process_files(file_paths, line_limit):
    summary = []  # Menyimpan ringkasan hasil pemrosesan
    for file_path in file_paths:
        # Proses setiap file
        result = process_file(file_path, line_limit)
        if result:
            summary.append(result)

    # Tampilkan ringkasan
    summary_message = "\n".join(summary)
    messagebox.showinfo("Ringkasan Pemrosesan", f"Berikut hasil pemrosesan file:\n\n{summary_message}")


def process_file(file_path, line_limit):
    # Baca isi file
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca file {file_path}:\n{e}")
        return None

    # Filter sesuai batas baris yang dimasukkan
    allowed_lines = lines[:line_limit]
    removed_lines = lines[line_limit:]

    # Konfirmasi pengguna
    preview = "".join(allowed_lines[:10]) + ("...\n" if len(allowed_lines) > 10 else "")
    message = f"File: {os.path.basename(file_path)}\n"
    message += f"Total baris: {len(lines)}\n"
    message += f"Baris yang disimpan: {len(allowed_lines)}\n"
    message += f"Baris yang dihapus: {len(removed_lines)}\n\n"
    message += "Pratinjau baris yang disimpan:\n"
    message += f"{preview}\n\n"
    message += "Apakah Anda ingin menyimpan perubahan?"

    proceed = messagebox.askyesno("Konfirmasi", message)

    if proceed:
        return save_file(file_path, allowed_lines)
    else:
        return f"File {os.path.basename(file_path)}: Perubahan dibatalkan."


def save_file(file_path, lines):
    # Tulis ulang file dengan baris yang disimpan
    try:
        with open(file_path, "w") as file:
            file.writelines(lines)
        return f"File {os.path.basename(file_path)}: Berhasil disimpan."
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file {file_path}:\n{e}")
        return f"File {os.path.basename(file_path)}: Gagal disimpan."


def main():
    # Buat GUI Tkinter
    root = Tk()
    root.withdraw()  # Sembunyikan jendela utama
    select_files()


if __name__ == "__main__":
    main()
