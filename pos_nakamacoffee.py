"""
POS KEDAI KOPI NAKAMA
Kelompok 1
NAMA ANGGOTA KELOMPOK:
1. Nyoman Ardhi Rahmayana (02560001)
2. Gede Angga Kurniawan Saputra ()
3. Gede Angga Wijaya Kusuma ()

PENGGUNAAN AI GEMINI


PENGGUNAAN REFERNSI MATERI


sc:
"""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

class POSNakamaCoffee:
    def __init__(self, root):
        self.root = root
        self.root.title("Nakama Coffee Shop - nongki sambil ngopi with nakama")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.config(bg="#1d1d12")
        self.fontstyle = ("Montserrat", 12, "normal")
        self.fontstyle_bold = ("Montserrat", 12, "bold")
        
        # Ambil data menu dari database .csv
        self.menu_items = self.load_menu()
        
        # Header Label
        tk.Label(root, text="-- Daftar Menu --", font=("Montserrat", 18, "bold"), bg="#1d1d12", fg="white").pack(pady=10)
        
        # Tabel/List untuk menampilkan menu
        self.tree = ttk.Treeview(root, columns=("Nama", "Harga"), show='headings', height=10)
        self.tree.heading("Nama", text="Nama Menu")
        self.tree.heading("Harga", text="Harga")
        self.tree.pack(pady=10)
        
        for item in self.menu_items:
            self.tree.insert("", tk.END, values=(item['nama'], item['harga']))

        # Buttons
        tk.Button(root, text="Buat Transaksi",
                  font=self.fontstyle_bold,
                  command=self.buka_transaksi,
                  bg="#F3E5AB", fg="black").pack(side=tk.LEFT, padx=50)
        tk.Button(root, text="Keluar Aplikasi",
                  font=self.fontstyle_bold,
                  command=self.konfirmasi_keluar,
                  bg="#F3E5AB", fg="black").pack(side=tk.RIGHT, padx=50)

    # Definisi fungsi-fungsi
    def load_menu(self):
        data = []
        try:
            with open('db\menu.csv', mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            messagebox.showerror("Error", "menu.csv tidak ditemukan!")
        return data

    def konfirmasi_keluar(self):
        tanya = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menutup aplikasi?")
        if tanya:
            self.root.destroy() # hentikan program

    def buka_transaksi(self):
        messagebox.showinfo("Info", "Membuka jendela transaksi...")
    
    def set_tabel(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=self.fontstyle_bold)
        style.configure("Treeview", rowheight=35, font=self.fontstyle)

        # frame
        anjay = tk.Frame(self.root, bg="#1a1a1a")
        anjay.pack(pady=20)

        sb = tk.Scrollbar(anjay)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(anjay, columns=("Nama", "Harga"), 
        show='headings', yscrollcommand=sb.set)
        
        # Atur lebar kolom
        self.tree.column("Nama", width=300, anchor="w") # Nama menu rata kiri
        self.tree.column("Harga", width=150, anchor="center") # Harga di tengah
        
        self.tree.pack()
        sb.config(command=self.tree.yview)

if __name__ == "__main__":
    root = tk.Tk()
    app = POSNakamaCoffee(root)
    root.mainloop()