import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import vobject
import os

def load_vcf():
    global contacts, file_paths, base_name
    file_paths = filedialog.askopenfilenames(filetypes=[("VCF Files", "*.vcf")])
    if not file_paths:
        return
    
    base_name = simpledialog.askstring("Rename Kontak", "Masukkan nama untuk kontak pertama:")
    if not base_name:
        base_name = "Kontak"
    
    contacts.clear()
    listbox.delete(0, tk.END)
    contact_counter = 1  # Mulai dari 1 setiap kali load
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            vcf_data = f.read()
        
        updated_contacts = []
        for vcard in vobject.readComponents(vcf_data):
            new_name = f"{base_name}{contact_counter}"
            
            if hasattr(vcard, 'fn'):
                vcard.fn.value = new_name
            else:
                vcard.add('fn').value = new_name
            
            updated_contacts.append(vcard)
            listbox.insert(tk.END, new_name)
            contact_counter += 1
        
        contacts.append((file_path, updated_contacts))

def save_vcf():
    if not contacts:
        messagebox.showwarning("Peringatan", "Tidak ada kontak untuk disimpan!")
        return
    
    for file_path, updated_contacts in contacts:
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, contact in enumerate(updated_contacts):
                formatted_vcf = contact.serialize().replace("\n", "").replace("END:VCARD", "END:VCARD\n")
                f.write(formatted_vcf)
    
    messagebox.showinfo("Sukses", "File VCF berhasil disimpan dan diperbarui dengan format rapi!")

root = tk.Tk()
root.title("Rename Kontak VCF")
contacts = []
file_paths = []
base_name = ""

frame = tk.Frame(root)
frame.pack(pady=10)

btn_load = tk.Button(frame, text="Pilih File VCF", command=load_vcf)
btn_load.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(frame, text="Simpan VCF", command=save_vcf)
btn_save.pack(side=tk.LEFT, padx=5)

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

root.mainloop()
