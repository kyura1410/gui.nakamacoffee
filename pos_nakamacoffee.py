"""
POS KEDAI KOPI NAKAMA
Kelompok 1

NAMA ANGGOTA KELOMPOK:
1. Nyoman Ardhi Rahmayana (02560001)
2. Gede Angga Kurniawan Saputra (02560003)
3. I Made Angga Wijaya Kusuma (02560002)

PENGGUNAAN AI GEMINI (Ardhi)
Mendiskuikan alur flowchart, treeview, csv database, notebook, dan beberapa fungsi dasar.

PENGGUNAAN AI GPT 5 (Angga Kurniawan)

"""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

file_menu = "db/menu.csv"
file_transaksi = "db/transaksi.csv"
font_utama = ("Montserrat", 12)
font_utama_bold = ("Montserrat", 12, "bold")

USER_LOGIN = {
    "admin": "admin123"
}

# Fungsi helper untuk format mata uang
def format_mata_uang(angka):
    return f"Rp. {angka:,.0f}".replace(",", ".")

# fokus pengelolaan database menu dan transaksi dalam file CSV

def baca_menu():
    menu = []
    if os.path.exists(file_menu):
        with open(file_menu, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                menu.append(row)
        return menu
    
def cek_csv():
    if not os.path.exists(file_menu):
        with open(file_menu, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama", "Harga", "Stok"])
            writer.writerow(["Espresso", "15000", "10"])
        
    if not os.path.exists(file_transaksi):
        with open(file_transaksi, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["no transaksi", "tanggal", "detail", "total"])

def simpan_menu_database(data_menu):
    with open(file_menu, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nama", "Harga", "Stok"])
        for item in data_menu:
            writer.writerow([item["Nama"], item["Harga"], item["Stok"]])

def simpan_transaksi_database(no_transaksi, detail, total):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_transaksi, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([no_transaksi, now, detail, total])

class LoginWindow:
    def __init__(nakama, root):
        nakama.root = root
        nakama.root.title("Login POS Nakama")
        nakama.root.geometry("300x200")

        tk.Label(root, text="Username").pack(pady=5)
        nakama.entry_user = tk.Entry(root)
        nakama.entry_user.pack()

        tk.Label(root, text="Password").pack(pady=5)
        nakama.entry_pass = tk.Entry(root, show="*")
        nakama.entry_pass.pack()

        tk.Button(root, text="Login", command=nakama.login).pack(pady=10)

    def login(nakama):
        user = nakama.entry_user.get()
        pw = nakama.entry_pass.get()

        if user in USER_LOGIN and USER_LOGIN[user] == pw:
            nakama.root.destroy()
            main_app()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah")
            
class POSNakamaCoffee:
    def __init__(nakama, root):
        nakama.root = root
        nakama.root.title("POS Kedai Kopi Nakama")
        nakama.root.geometry("900x600")

        nakama.keranjang = []

        nakama.atur_tab = ttk.Notebook(root)
        nakama.tab_kasir = ttk.Frame(nakama.atur_tab)
        nakama.tab_admin = ttk.Frame(nakama.atur_tab)
        nakama.tab_riwayat = ttk.Frame(nakama.atur_tab)

        nakama.atur_tab.add(nakama.tab_kasir, text="Kasir")
        nakama.atur_tab.add(nakama.tab_admin, text="Admin")
        nakama.atur_tab.add(nakama.tab_riwayat, text="Riwayat Transaksi")
        nakama.atur_tab.pack(expand=1, fill="both")

        nakama.tampilkan_kasir()

    def tampilkan_kasir(nakama):
        frame_kiri = tk.Frame(nakama.tab_kasir, padx=10, pady=10)
        frame_kiri.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_kanan = tk.Frame(nakama.tab_kasir, padx=10, pady=10, bg="#f0f0f0")
        frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH)

        tk.Label(frame_kiri, text="Menu Kedai Kopi:", font=font_utama_bold).pack(pady=5)
        tk.Label(frame_kanan, text="Keranjang Belanja:", font=font_utama_bold, bg="#f0f0f0").pack(pady=5)

        kolom_menu = ("Nama", "Harga", "Stok")
        nakama.tree_menu_kasir = ttk.Treeview(frame_kiri, columns=kolom_menu, show="headings", height=15)
        for kolom in kolom_menu:
            nakama.tree_menu_kasir.heading(kolom, text=kolom)
            nakama.tree_menu_kasir.column(kolom)
        nakama.tree_menu_kasir.pack(fill=tk.BOTH, expand=True)

        nambah_tombol = tk.Button(frame_kiri, text="Tambah ke Keranjang", command=nakama.tambah_ke_keranjang, bg="#4CAF50", fg="white",)
        nambah_tombol.pack(fill=tk.X, pady=5)

        kolom_keranjang = ("Item", "Qty", "Subtotal")
        nakama.tree_keranjang = ttk.Treeview(frame_kanan, columns=kolom_keranjang, show="headings", height=15)
        for kolom in kolom_keranjang:
            nakama.tree_keranjang.heading(kolom, text=kolom)
            nakama.tree_keranjang.column(kolom)
        nakama.tree_keranjang.pack(pady=10)

        nakama.label_total = tk.Label(frame_kanan, text="Total: Rp 0", font=font_utama_bold, bg="#f0f0f0")
        nakama.label_total.pack(pady=5)

        tombol_reset = tk.Button(frame_kanan, text="Reset Keranjang", command=nakama.reset_keranjang, font=font_utama, bg="#4c4a0d", fg="white")
        tombol_reset.pack(fill=tk.X, pady=2)

        tombol_bayar = tk.Button(frame_kanan, text="Proses Pembayaran", command=nakama.proses_pembayaran, font=font_utama_bold, bg="#2196F3", fg="white")
        tombol_bayar.pack(fill=tk.X, pady=2)

        nakama.refresh_tabel_menu()

    def tambah_ke_keranjang(nakama):
        terpilih = nakama.tree_menu_kasir.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Silakan pilih item dari menu terlebih dahulu.")
            return
        
        item = nakama.tree_menu_kasir.item(terpilih)
        nama = item['values'][0]
        harga = int(item['values'][1].replace("Rp. ", "").replace(".", ""))  # Parse harga dari format
        stok = int(item['values'][2])

        if stok <= 0:
            messagebox.showwarning("Peringatan", "Stok item ini habis.")
            return
        
        for i, barang in enumerate(nakama.keranjang):
            if barang['Nama'] == nama:
                nakama.keranjang[i]['Qty'] += 1
                nakama.keranjang[i]['Subtotal'] += harga
                nakama.update_tabel_keranjang()
                return
        
        # Jika item belum ada di keranjang, tambahkan
        nakama.keranjang.append({'Nama': nama, 'Harga': harga, 'Qty': 1, 'Subtotal': harga})
        nakama.update_tabel_keranjang()

    def update_tabel_keranjang(nakama):
        for baris in nakama.tree_keranjang.get_children():
            nakama.tree_keranjang.delete(baris)

        total_bayar = 0
        for barang in nakama.keranjang:
            nakama.tree_keranjang.insert("", tk.END, values=(barang['Nama'], barang['Qty'], format_mata_uang(barang['Subtotal'])))
            total_bayar += barang['Subtotal']

        nakama.label_total.config(text=f"Total: {format_mata_uang(total_bayar)}")

    def reset_keranjang(nakama):
        nakama.keranjang = []
        nakama.update_tabel_keranjang()

    def proses_pembayaran(nakama):
        if not nakama.keranjang:
            messagebox.showwarning("Peringatan", "Keranjang lagi kosong!")
            return

        total_bayar = sum(barang['Subtotal'] for barang in nakama.keranjang)
        
        # Input uang pembeli
        uang_pembeli = simpledialog.askinteger("Input Uang Pembeli", f"Total bayar: {format_mata_uang(total_bayar)}\nMasukkan jumlah uang pembeli (dalam Rupiah):")
        if uang_pembeli is None:
            return  # Batal
        
        if uang_pembeli < total_bayar:
            messagebox.showerror("Error", "Uang pembeli kurang dari total bayar!")
            return
        
        kembalian = uang_pembeli - total_bayar
        
        menu_sekarang = baca_menu()
        detail_id_nota = ""

        for barang in nakama.keranjang:
            detail_id_nota += f"{barang['Nama']} x {barang['Qty']}, "
            for menu_item in menu_sekarang:
                if menu_item['Nama'] == barang['Nama']:
                    stok_baru = int(menu_item['Stok']) - barang['Qty']
                    menu_item['Stok'] = str(stok_baru)

        simpan_menu_database(menu_sekarang)

        id_nota = f"No. {int(datetime.now().timestamp())}"
        simpan_transaksi_database(id_nota, detail_id_nota.strip(", "), total_bayar)

        nota = f"--- Nakama Coffee Shop ---\n"
        nota += f"ID Nota: {id_nota}\n"
        nota += f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        nota += "-"*30 + "\n"
        for item in nakama.keranjang:
            nota += f"{item['Nama']} \t x{item['Qty']} \t = {format_mata_uang(item['Subtotal'])}\n"
        nota += "-"*30 + "\n"
        nota += f"Total Bayar: \t\t {format_mata_uang(total_bayar)}\n"
        nota += f"Uang Pembeli: \t\t {format_mata_uang(uang_pembeli)}\n"
        nota += f"Kembalian: \t\t {format_mata_uang(kembalian)}\n"
        nota += "Terima kasih telah berbelanja di Nakama Coffee Shop!"

        messagebox.showinfo("Struk Pembayaran", nota)

        nakama.reset_keranjang()

    def refresh_tabel_menu(nakama):
        for baris in nakama.tree_menu_kasir.get_children():
            nakama.tree_menu_kasir.delete(baris)
        menu = baca_menu()
        for item in menu:
            harga_formatted = format_mata_uang(int(item['Harga']))
            nakama.tree_menu_kasir.insert('', tk.END, values=(item['Nama'], harga_formatted, item['Stok']))

def main_app():
   root = tk.Tk()
   app = POSNakamaCoffee(root)
   root.mainloop()

if __name__ == "__main__":
    cek_csv()
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()