"""
POS KEDAI KOPI NAKAMA
Kelompok 1
NAMA ANGGOTA KELOMPOK:
1. Nyoman Ardhi Rahmayana (02560001)
2. Gede Angga Kurniawan Saputra (02560003)
3. Gede Angga Wijaya Kusuma ()

PENGGUNAAN AI GEMINI
PENGGUNAAN AI GPT 5

PENGGUNAAN REFERNSI MATERI


sc:
"""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

file_menu = "db/menu.csv"
file_transaksi = "db/transaksi.csv"
font_utama = ("Montserrat", 12)
font_utama_bold = ("Montserrat", 12, "bold")

USER_LOGIN = {
    "admin": "admin123"

}

def cek_csv():
    if not os.path.exists(file_menu):
        with open(file_menu, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["nama", "harga", "stok"])
            writer.writerow(["Espresso", "15000", "10"])
        
    if not os.path.exists(file_transaksi):
        with open(file_transaksi, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["no transaksi", "tanggal", "detail", "total"])

def load_menu():
        if not os.path.exists(file_menu):
            return[]
        items = []
        with open(file_menu, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                items.append(row)
        return items


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login POS Nakama")
        self.root.geometry("300x200")

        tk.Label(root, text="Username").pack(pady=5)
        self.entry_user = tk.Entry(root)
        self.entry_user.pack()

        tk.Label(root, text="Password").pack(pady=5)
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        user = self.entry_user.get()
        pw = self.entry_pass.get()

        if user in USER_LOGIN and USER_LOGIN[user] == pw:
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah")
            
class POSNakamaCoffee:
    def __init__(self, root):
        self.root = root
        self.root.title("POS Kedai Kopi Nakama")
        self.root.geometry("900x600")

        self.keranjang = []

        self.atur_tab = ttk.Notebook(root)
        self.tab_kasir = ttk.Frame(self.atur_tab)
        self.tab_admin = ttk.Frame(self.atur_tab)
        self.tab_riwayat = ttk.Frame(self.atur_tab)

        self.atur_tab.add(self.tab_kasir, text="Kasir")
        self.atur_tab.add(self.tab_admin, text="Admin")
        self.atur_tab.add(self.tab_riwayat, text="Riwayat Transaksi")
        self.atur_tab.pack(expand=1, fill="both")

        self.tampilkan_kasir()

    def tampilkan_kasir(self):
        frame_kiri = tk.Frame(self.tab_kasir, padx=10, pady=10)
        frame_kiri.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_kanan = tk.Frame(self.tab_kasir, padx=10, pady=10, bg="#f0f0f0")
        frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH)

        tk.Label(frame_kanan, text="Keranjang Belanja:", font=font_utama_bold, bg="#f0f0f0").pack(pady=5)

        kolom_menu = ("Nama", "Harga", "Stok")
        self.tree_menu_kasir = ttk.Treeview(frame_kiri, columns=kolom_menu, show="headings", height=15)
        for kolom in kolom_menu:
            self.tree_menu_kasir.heading(kolom, text=kolom)
            self.tree_menu_kasir.column(kolom)
        self.tree_menu_kasir.pack(pady=10)

        nambah_tombol = tk.Button(frame_kiri, text="Tambah ke Keranjang", font=font_utama, bg="#4CAF50", fg="white",)
        nambah_tombol.pack(fill=tk.X, pady=5)

        kolom_keranjang = ("Item", "Qty", "Subtotal")
        self.tree_keranjang = ttk.Treeview(frame_kanan, columns=kolom_keranjang, show="headings", height=15)
        for kolom in kolom_keranjang:
            self.tree_keranjang.heading(kolom, text=kolom)
            self.tree_keranjang.column(kolom)
        self.tree_keranjang.pack(pady=10)

        self.label_total = tk.Label(frame_kanan, text="Total: Rp 0", font=font_utama_bold, bg="#f0f0f0")
        self.label_total.pack(pady=5)

def main_app():
   root = tk.Tk()
   app = POSNakamaCoffee(root)
   root.mainloop()

if __name__ == "__main__":
    cek_csv()
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
