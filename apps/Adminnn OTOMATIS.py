import os
import re
import time
import ctypes
import ctypes.wintypes as wt
import keyboard
import pyperclip
import customtkinter as ctk
from tkinter import messagebox, simpledialog

# ----------------------
# STATE
# ----------------------
STATE = {"admin_buffer": None}  # simpan admin sementara

# ----------------------
# HELPERS
# ----------------------
def get_vcf_folder() -> str:
    folder = os.path.join(os.path.expanduser("~"), "Downloads", "Telegram Desktop", "VCF")
    os.makedirs(folder, exist_ok=True)
    return folder

def normalize_number(raw: str) -> str:
    """Normalisasi nomor: hapus karakter asing dan ubah sesuai aturan"""
    if not raw:
        return ""
    # hapus semua karakter kecuali angka dan + di awal
    s = re.sub(r"[^\d+]", "", raw.strip())
    if not s:
        return ""
    if s.startswith("+"):
        digits = s[1:]
        if digits.startswith("62"):
            return "+62" + digits[2:]
        return "+" + digits
    if s.startswith("0"):
        return "+62" + s[1:]
    if s.startswith("62"):
        return "+62" + s[2:]
    return "+" + s

def clipboard_to_lines() -> list:
    """Ambil teks dari clipboard, pecah baris"""
    try:
        keyboard.press_and_release("ctrl+c")
        time.sleep(0.06)
    except Exception:
        pass
    data = pyperclip.paste() or ""
    return [line.strip() for line in data.splitlines() if line.strip()]

# ----------------------
# COPY FILE -> CLIPBOARD (Windows)
# ----------------------
class DROPFILES(ctypes.Structure):
    _fields_ = [
        ("pFiles", ctypes.wintypes.DWORD),
        ("pt", ctypes.wintypes.POINT),
        ("fNC", ctypes.wintypes.BOOL),
        ("fWide", ctypes.wintypes.BOOL),
    ]

def copy_file_to_clipboard(filepath: str) -> None:
    if os.name != "nt":
        raise OSError("Fungsi ini hanya berjalan di Windows.")
    filepath = os.path.abspath(filepath)
    buf = (filepath + "\0\0").encode("utf-16le")
    df = DROPFILES()
    df.pFiles = ctypes.sizeof(DROPFILES)
    df.fWide = 1
    total_size = ctypes.sizeof(DROPFILES) + len(buf)
    GHND = 0x0042
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    hGlobal = kernel32.GlobalAlloc(GHND, total_size)
    if not hGlobal:
        raise OSError("GlobalAlloc failed")
    ptr = kernel32.GlobalLock(hGlobal)
    if not ptr:
        kernel32.GlobalFree(hGlobal)
        raise OSError("GlobalLock failed")
    try:
        ctypes.memmove(ptr, ctypes.byref(df), ctypes.sizeof(df))
        dest = ptr + ctypes.sizeof(df)
        ctypes.memmove(dest, buf, len(buf))
    finally:
        kernel32.GlobalUnlock(hGlobal)
    if not user32.OpenClipboard(None):
        kernel32.GlobalFree(hGlobal)
        raise OSError("OpenClipboard failed")
    try:
        user32.EmptyClipboard()
        CF_HDROP = 15
        if not user32.SetClipboardData(CF_HDROP, hGlobal):
            kernel32.GlobalFree(hGlobal)
            raise OSError("SetClipboardData failed")
    finally:
        user32.CloseClipboard()

# ----------------------
# SAVE VCF
# ----------------------
def save_vcf(contact_name: str, file_name: str, numbers: list[str]):
    cleaned, vcard_lines, invalid = [], [], []
    valid_idx = 1
    for n in numbers:
        norm = normalize_number(n)
        if not norm:
            invalid.append(n)
            continue
        cleaned.append(norm)
        vcard_lines.append(
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{contact_name} {valid_idx}\n"
            f"TEL:{norm}\n"
            "END:VCARD\n"
        )
        valid_idx += 1
    if not vcard_lines:
        return None, invalid, False
    folder = get_vcf_folder()
    filename = os.path.join(folder, f"{file_name}.vcf")
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(vcard_lines)
    if invalid:
        with open(os.path.join(folder, "error_log.txt"), "a", encoding="utf-8") as f:
            f.write(f"\n--- {file_name}.vcf ---\n")
            for item in invalid:
                f.write(item + "\n")
    copy_ok = True
    try:
        copy_file_to_clipboard(filename)
    except Exception as e:
        copy_ok = False
        print("Gagal copy file ke clipboard:", e)
    return (filename, cleaned[0], cleaned[-1], len(cleaned)), invalid, copy_ok

def show_summary(info, invalid, copy_ok, title="Ringkasan"):
    if not info:
        messagebox.showerror(title, "❌ Tidak ada nomor valid yang bisa disimpan.")
        return
    filepath, first, last, total = info
    msg = f"📂 {os.path.basename(filepath)}\n"
    msg += f"   • Total   : {total} kontak\n"
    msg += f"   • Pertama : {first}\n"
    msg += f"   • Terakhir: {last}\n"
    if invalid:
        msg += f"\n⚠️ {len(invalid)} nomor dibuang (lihat error_log.txt)"
    if copy_ok:
        msg += f"\n\n✅ File sudah tersalin ke clipboard (tinggal Ctrl+V untuk kirim file)."
    else:
        msg += f"\n\n⚠️ Gagal menyalin file ke clipboard. File tetap tersimpan di:\n{os.path.dirname(filepath)}"
    messagebox.showinfo(title, msg)

# ----------------------
# PROSES HOTKEY
# ----------------------
def proses_admin():
    lines = clipboard_to_lines()
    if not lines:
        messagebox.showwarning("Kosong", "Clipboard kosong.")
        return
    tambahan = simpledialog.askstring("Admin", "Masukkan nama tambahan Admin:")
    if not tambahan:
        return
    info, invalid, copy_ok = save_vcf("Admin " + tambahan.strip(), f"Admin {tambahan.strip()}", lines)
    show_summary(info, invalid, copy_ok, "Admin - Selesai")

def proses_navy():
    lines = clipboard_to_lines()
    if not lines:
        messagebox.showwarning("Kosong", "Clipboard kosong.")
        return
    tambahan = simpledialog.askstring("Navy", "Masukkan nama tambahan Navy:")
    if not tambahan:
        return
    info, invalid, copy_ok = save_vcf("Navy " + tambahan.strip(), f"Navy {tambahan.strip()}", lines)
    show_summary(info, invalid, copy_ok, "Navy - Selesai")

def proses_admin_navy():
    lines = clipboard_to_lines()
    if not lines:
        messagebox.showwarning("Kosong", "Clipboard kosong.")
        return
    if STATE["admin_buffer"] is None:
        STATE["admin_buffer"] = lines
        messagebox.showinfo("Step 1", "✅ Nomor Admin tersimpan.\n\nSekarang blok nomor Navy lalu tekan Ctrl+B lagi.")
        return
    navy_lines = lines
    tambahan = simpledialog.askstring("Admin + Navy", "Masukkan nama tambahan untuk Admin & Navy:")
    if not tambahan:
        STATE["admin_buffer"] = None
        return

    # Pisahkan Admin & Navy
    admin_contacts, navy_contacts, invalid = [], [], []
    for n in STATE["admin_buffer"]:
        norm = normalize_number(n)
        if norm:
            admin_contacts.append(norm)
        else:
            invalid.append(n)
    for n in navy_lines:
        norm = normalize_number(n)
        if norm:
            navy_contacts.append(norm)
        else:
            invalid.append(n)

    if not admin_contacts and not navy_contacts:
        messagebox.showerror("Gagal", "Tidak ada nomor valid.")
        STATE["admin_buffer"] = None
        return

    folder = get_vcf_folder()
    filename = os.path.join(folder, f"Admin Navy {tambahan.strip()}.vcf")
    with open(filename, "w", encoding="utf-8") as f:
        # Tulis Admin mulai dari 1
        for idx, num in enumerate(admin_contacts, start=1):
            f.write("BEGIN:VCARD\n")
            f.write("VERSION:3.0\n")
            f.write(f"FN:Admin {tambahan.strip()} {idx}\n")
            f.write(f"TEL:{num}\n")
            f.write("END:VCARD\n")

        # Tulis Navy mulai dari 1 lagi
        for idx, num in enumerate(navy_contacts, start=1):
            f.write("BEGIN:VCARD\n")
            f.write("VERSION:3.0\n")
            f.write(f"FN:Navy {tambahan.strip()} {idx}\n")
            f.write(f"TEL:{num}\n")
            f.write("END:VCARD\n")

    if invalid:
        with open(os.path.join(folder, "error_log.txt"), "a", encoding="utf-8") as f:
            f.write(f"\n--- {os.path.basename(filename)} ---\n")
            for item in invalid:
                f.write(item + "\n")

    copy_ok = True
    try:
        copy_file_to_clipboard(filename)
    except Exception as e:
        copy_ok = False
        print("Gagal copy file ke clipboard:", e)

    # Ringkasan tetap
    first_num = (admin_contacts[0] if admin_contacts else navy_contacts[0])
    last_num = (navy_contacts[-1] if navy_contacts else admin_contacts[-1])
    total = len(admin_contacts) + len(navy_contacts)

    show_summary((filename, first_num, last_num, total), invalid, copy_ok, "Admin + Navy - Selesai")
    STATE["admin_buffer"] = None

# ----------------------
# REGISTER HOTKEY
# ----------------------
keyboard.add_hotkey("ctrl+k", proses_admin, suppress=False)
keyboard.add_hotkey("ctrl+n", proses_navy, suppress=False)
keyboard.add_hotkey("ctrl+b", proses_admin_navy, suppress=False)

print(
    "✅ Tool siap dipakai.\n"
    "   Ctrl+K = Admin  (select teks daftar nomor lalu tekan)\n"
    "   Ctrl+N = Navy   (select teks daftar nomor lalu tekan)\n"
    "   Ctrl+B = Admin+Navy (1x: seleksi Admin + Ctrl+B, lalu seleksi Navy + Ctrl+B)\n"
    "📂 Hasil: Downloads/Telegram Desktop/VCF/\n"
    "📋 File .vcf otomatis disalin ke clipboard sebagai FILE (tinggal Ctrl+V untuk kirim)\n"
)

keyboard.wait()
