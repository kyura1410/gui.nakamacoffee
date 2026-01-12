"""
POS KEDAI KOPI NAKAMA
Kelompok 1

NAMA ANGGOTA KELOMPOK:
1. Nyoman Ardhi Rahmayana (02560001) - UI/UX Designer, 
2. Gede Angga Kurniawan Saputra (02560003) - Fitur Login, Query Database
3. I Made Angga Wijaya Kusuma (02560002) -  Fitur Transaksi, Database Management, Nominal Mata Uang

PENGGUNAAN AI GEMINI (Ardhi)
Mendiskuikan alur flowchart, treeview, csv database, notebook, dan beberapa fungsi dasar.

PENGGUNAAN AI GPT 5 (Angga Kurniawan)
mendiskusikan debugging alur login, query database
"""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

file_menu = "db\\menu.csv"
file_transaksi = "db\\transaksi.csv"
font_utama = ("Montserrat", 12)
font_utama_bold = ("Montserrat", 12, "bold")

USER_LOGIN = {
    "1": "1"
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

        #MENAMBAH FITUR BIND KEY UNTUK TOMBOL ENTER DI KEYBOARD SAAT LOGIN
        nakama.root.bind('<Return>', lambda event: nakama.login())

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
        nakama.tampilkan_admin()
        nakama.tampilkan_riwayat()

    def tampilkan_kasir(nakama):
        frame_kiri = tk.Frame(nakama.tab_kasir, padx=10, pady=10)
        frame_kiri.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_kanan = tk.Frame(nakama.tab_kasir, padx=10, pady=10, bg="#f0f0f0")
        frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH)

        tk.Label(frame_kiri, text="Menu Kedai Kopi:", font=font_utama_bold).pack(pady=5)
        
        # --- FITUR PENCARIAN BARU ---
        frame_cari = tk.Frame(frame_kiri)
        frame_cari.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_cari, text="Cari Menu: ", font=font_utama).pack(side=tk.LEFT)
        nakama.entry_cari = tk.Entry(frame_cari, font=font_utama)
        nakama.entry_cari.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Event binding agar pencarian otomatis saat mengetik
        nakama.entry_cari.bind("<KeyRelease>", lambda event: nakama.refresh_tabel_menu())
        
        tk.Label(frame_kanan, 
                 text="Keranjang Belanja:", 
                 font=font_utama_bold, 
                 bg="#f0f0f0").pack(pady=5)
  

        kolom_menu = ("Nama", "Harga", "Stok")
        nakama.tree_menu_kasir = ttk.Treeview(frame_kiri,
                                              columns=kolom_menu, 
                                              show="headings", 
                                              height=15)
        for kolom in kolom_menu:
            nakama.tree_menu_kasir.heading(kolom, text=kolom)
            nakama.tree_menu_kasir.column(kolom)
        nakama.tree_menu_kasir.pack(fill=tk.BOTH, expand=True)

        nambah_tombol = tk.Button(frame_kiri, text="Tambah ke Keranjang",
                                  command=nakama.tambah_ke_keranjang,
                                  font=font_utama_bold,
                                  bg="#114F13",
                                  fg="white",)
        nambah_tombol.pack(fill=tk.X, pady=5)

        kolom_keranjang = ("Item", "Qty", "Subtotal")
        nakama.tree_keranjang = ttk.Treeview(frame_kanan, 
                                             columns=kolom_keranjang, 
                                             show="headings", 
                                             height=15)
        for kolom in kolom_keranjang:
            nakama.tree_keranjang.heading(kolom, text=kolom)
            nakama.tree_keranjang.column(kolom)
        nakama.tree_keranjang.pack(pady=10)

        nakama.label_total = tk.Label(frame_kanan, 
                                      text="Total: Rp 0", 
                                      font=font_utama_bold, 
                                      bg="#f0f0f0")
        nakama.label_total.pack(pady=5)

        tombol_reset = tk.Button(frame_kanan,
                                 text="Reset Keranjang", 
                                 command=nakama.reset_keranjang, 
                                 font=font_utama_bold, 
                                 bg="#4c4a0d", 
                                 fg="white")
        tombol_reset.pack(fill=tk.X, pady=2)

        tombol_bayar = tk.Button(frame_kanan, 
                                 text="Proses Pembayaran", 
                                 command=nakama.proses_pembayaran, 
                                 font=font_utama_bold, 
                                 bg="#254055", 
                                 fg="white")
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
        nakama.refresh_tabel_menu()
        nakama.refresh_tabel_riwayat()
        nakama.refresh_tabel_admin()


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
        nakama.refresh_tabel_menu()
        nakama.refresh_tabel_riwayat()
        nakama.refresh_tabel_admin()

    def refresh_tabel_menu(nakama):
        # Ambil kata kunci dari entry pencarian (jika ada)
        kata_kunci = nakama.entry_cari.get().lower() if hasattr(nakama, 'entry_cari') else ""
        
        # Bersihkan tabel sebelum diisi ulang
        for baris in nakama.tree_menu_kasir.get_children():
            nakama.tree_menu_kasir.delete(baris)

        menu = baca_menu()
        #   print(f"DEBUG: Total menu terbaca: {len(menu)}") # <--- TAMBAHKAN INI
        #   print(f"DEBUG: Isi menu pertama: {menu[0] if menu else 'Kosong'}") # <--- TAMBAHKAN INI

        for item in menu:
            
            #Filter: jika nama menu mengandung kata kunci
            if kata_kunci in item['Nama'].lower():
                harga_formatted = format_mata_uang(int(item['Harga']))
                nakama.tree_menu_kasir.insert('', tk.END, values=(item['Nama'], harga_formatted, item['Stok']))

    # menampilkan halaman admin
    def tampilkan_admin(nakama):
        frame_input = tk.Frame(nakama.tab_admin,
                               padx=10,
                               pady=10)
        frame_input.pack(side=tk.TOP, fill=tk.X)

        tk.Label(frame_input, text="Nama Menu:").grid(row=0,
                                                      column=0, 
                                                      padx=5,
                                                      pady=5)
        nakama.entry_nama = tk.Entry(frame_input)
        nakama.entry_nama.grid(row=0,
                               column=1,
                               padx=5,
                               pady=5)

        tk.Label(frame_input, text="Harga:").grid(row=0,
                                                  column=2,
                                                  padx=5,
                                                  pady=5)
        
        nakama.entry_harga = tk.Entry(frame_input)
        nakama.entry_harga.grid(row=0,
                                column=3,
                                padx=5,
                                pady=5)

        tk.Label(frame_input, text="Stok:").grid(row=0,
                                                 column=4,
                                                 padx=5, 
                                                 pady=5)
        nakama.entry_stok = tk.Entry(frame_input)
        nakama.entry_stok.grid(row=0, column=5, padx=5, pady=5)

        tombol_simpan = tk.Button(frame_input,
                                  text="SImpan/Update Menu",
                                  command=nakama.simpan_menu_admin,
                                  bg="#1E5420",
                                  fg="white")
        tombol_simpan.grid(row=1,
                           column=0,
                           columnspan=2,
                           sticky="ew",
                           padx=5,
                           pady=5)
        
        tombol_hapus = tk.Button(frame_input,
                                 text="Hapus Menu Terpilih",
                                 command=nakama.hapus_menu_admin,
                                 bg="#5f1e1a",
                                 fg="white")
        tombol_hapus.grid(row=1,
                           column=2,
                           columnspan=2,
                           sticky="ew",
                           padx=5,
                           pady=5)
        tombol_clear = tk.Button(frame_input,
                                 text="Bersihkan Input",
                                 command=nakama.clear_form_admin,
                                 bg="#18588B",
                                 fg="white")
        tombol_clear.grid(row=1,
                          column=4,
                          columnspan=2,
                          sticky="ew",
                          padx=5,
                          pady=5)
        
        nakama.tree_admin = ttk.Treeview(nakama.tab_admin,
                                        columns=('Nama', 'Harga', 'Stok'),
                                        show='headings')
        nakama.tree_admin.heading('Nama', text='Nama')
        nakama.tree_admin.heading('Harga', text='Harga')
        nakama.tree_admin.heading('Stok', text='Stok')
        nakama.tree_admin.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        nakama.tree_admin.bind('<<TreeviewSelect>>', nakama.pilih_baris_admin)

        nakama.refresh_tabel_admin()

    def refresh_tabel_admin(nakama):
        for baris in nakama.tree_admin.get_children():
            nakama.tree_admin.delete(baris)
        menu = baca_menu()
        for item in menu:
            nakama.tree_admin.insert('', tk.END, values=(item['Nama'], item['Harga'], item['Stok']))
    
    def refresh_tabel_menu(nakama):
        for baris in nakama.tree_menu_kasir.get_children():
            nakama.tree_menu_kasir.delete(baris)
        menu = baca_menu()
        for item in menu:
            nakama.tree_menu_kasir.insert('', tk.END, values=(item['Nama'], item['Harga'], item['Stok']))

    def clear_form_admin(nakama):
        nakama.entry_nama.delete(0, tk.END)
        nakama.entry_harga.delete(0, tk.END)
        nakama.entry_stok.delete(0, tk.END)

    def pilih_baris_admin(nakama, event):
        terpilih = nakama.tree_admin.selection()
        if terpilih:
            item = nakama.tree_admin.item(terpilih)
            stok = item['values']
            nakama.clear_form_admin()
            nakama.entry_nama.insert(0, stok[0])
            nakama.entry_harga.insert(0, stok[1])
            nakama.entry_stok.insert(0, stok[2])

    def simpan_menu_admin(nakama):
        nama = nakama.entry_nama.get()
        harga = nakama.entry_harga.get()
        stok = nakama.entry_stok.get()

        if not nama or not harga or not stok:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return
        
        try:
            int(harga)
            int(stok)
        except ValueError:
            messagebox.showerror("Error", "Harga dan Stok harus berupa angka!")
            return
        
        menu = baca_menu()
        update_baris = False

        for item in menu:
            if item['Nama'].lower() == nama.lower():
                item['Harga'] = harga
                item['Stok'] = stok
                update_baris = True
                break

        if not update_baris:
            menu.append({'Nama': nama, 'Harga': harga, 'Stok': stok})

        simpan_menu_database(menu)
        nakama.refresh_tabel_admin()
        nakama.refresh_tabel_menu()
        nakama.clear_form_admin()
        messagebox.showinfo("Sukses", "Menu berhasil disimpan/diupdate.")

    def hapus_menu_admin(nakama):
        terpilih = nakama.tree_admin.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih menu yang akan dihapus.")
            return
        
        item = nakama.tree_admin.item(terpilih)
        nama_hapus = item['values'][0]

        konfirmasi = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus menu '{nama_hapus}'?")
        if konfirmasi:
            menu = baca_menu()
            menu = [m for m in menu if m['Nama'] != nama_hapus]
            simpan_menu_database(menu)
            nakama.refresh_tabel_admin()
            nakama.refresh_tabel_menu()
            nakama.clear_form_admin()

    # menampilkan riwayat transaksi
    def tampilkan_riwayat(nakama):
        tombol_refresh = tk.Button(nakama.tab_riwayat,
                                   text="Segarkan Data",
                                   command=nakama.refresh_tabel_riwayat,
                                   bg="#2196F3",
                                   fg="white")
        tombol_refresh.pack(fill=tk.X, padx=10, pady=5)

        kolom_riwayat = ('No Transaksi', 'Tanggal', 'Detail', 'Total')
        nakama.tree_riwayat = ttk.Treeview(nakama.tab_riwayat,
                                          columns=kolom_riwayat,
                                          show='headings')
        
        nakama.tree_riwayat.heading('No Transaksi', text='No Transaksi')
        nakama.tree_riwayat.column("No Transaksi", width=120)
        nakama.tree_riwayat.heading('Tanggal', text='Tanggal')
        nakama.tree_riwayat.column("Tanggal", width=120)
        nakama.tree_riwayat.heading('Detail', text='Detail Item')
        nakama.tree_riwayat.column("Detail", width=200)
        nakama.tree_riwayat.heading('Total', text='Total (Rp)')
        nakama.tree_riwayat.column("Total", width=120)

        nakama.tree_riwayat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        nakama.refresh_tabel_riwayat()

    def refresh_tabel_riwayat(nakama):
        for baris in nakama.tree_riwayat.get_children():
            nakama.tree_riwayat.delete(baris)
        
        if os.path.exists(file_transaksi):
            with open(file_transaksi, mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)

                data = list(reader)
                for baris in reversed(data):
                    nakama.tree_riwayat.insert('', tk.END, values=baris)

def main_app():
   root = tk.Tk()
   app = POSNakamaCoffee(root)
   root.mainloop()

if __name__ == "__main__":
    cek_csv()
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
