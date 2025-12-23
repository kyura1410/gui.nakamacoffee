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

import tkinter as tk
from tkinter import messagebox  
from tkinter.messagebox import showinfo

# Membuat jendela utama
window = tk.Tk()
window.title("Nakama Coffee Shop")
window.geometry("550x550")
window.resizable(False, False)
window.config(bg="#1d1d12")

# Styling teks dan warna
fontstyle = ("Montserrat", 12)
fontstyle_bold = ("Montserrat", 12, "bold")
fontstyle_header = ("Montserrat", 20, "bold")
berhasilAddOrder = "Berhasil, Menambahkan Pesanan!"

# Definisi fungsi-fungsi


# Frame

# Widget
header = tk.Label(window, 
                  text="-- Nakama Coffee --", 
                  font=fontstyle_header, 
                  bg="#1d1d12", 
                  fg="#F9E7B2")
deskripsi = tk.Label(window, 
                     text="nongki sambil ngopi dengan nakama",
                     font=fontstyle, 
                     bg="#1d1d12",
                     fg="#F9E7B2")
header.pack(pady=0)
deskripsi.pack(pady=0)

window.mainloop()
