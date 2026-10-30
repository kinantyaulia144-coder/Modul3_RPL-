# Kinanty Putri Aulia_004
import customtkinter as ctk
from tkinter import ttk, messagebox

class AnggotaView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Sistem Manajemen Perpustakaan - Data Anggota")
        self.geometry("800x500")

        # Frame Form (Kiri)
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.form_frame, text="Form Data Anggota", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(self.form_frame, text="Nama Anggota:").pack(anchor="w", padx=10)
        self.entry_nama = ctk.CTkEntry(self.form_frame, width=250)
        self.entry_nama.pack(padx=10, pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Alamat:").pack(anchor="w", padx=10)
        self.entry_alamat = ctk.CTkEntry(self.form_frame, width=250)
        self.entry_alamat.pack(padx=10, pady=(0, 10))

        self.btn_simpan = ctk.CTkButton(self.form_frame, text="Simpan", fg_color="green", command=self.simpan_data)
        self.btn_simpan.pack(fill="x", padx=10, pady=5)

        self.btn_perbarui = ctk.CTkButton(self.form_frame, text="Perbarui", fg_color="orange", command=self.perbarui_data)
        self.btn_perbarui.pack(fill="x", padx=10, pady=5)

        self.btn_hapus = ctk.CTkButton(self.form_frame, text="Hapus", fg_color="red", command=self.hapus_data)
        self.btn_hapus.pack(fill="x", padx=10, pady=5)

        # Frame Tabel (Kanan)
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.table_frame, text="Daftar Anggota", font=("Arial", 16, "bold")).pack(pady=10)

        # Tabel hanya 3 kolom: ID, Nama, Alamat
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Nama", "Alamat"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Alamat", text="Alamat")

        self.tree.column("ID", width=50)
        self.tree.column("Nama", width=150)
        self.tree.column("Alamat", width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.pilih_data)

        self.selected_id = None
        self.tampil_data()

    def tampil_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = self.controller.get_all_anggota()
        for item in data:
            self.tree.insert("", "end", values=(item['id_anggota'], item['nama'], item['alamat']))

    def simpan_data(self):
        nama = self.entry_nama.get()
        alamat = self.entry_alamat.get()
        success, message = self.controller.tambah_anggota(nama, alamat)
        messagebox.showinfo("Informasi", message)
        if success:
            self.clear_form()
            self.tampil_data()

    def perbarui_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diperbarui!")
            return
        nama = self.entry_nama.get()
        alamat = self.entry_alamat.get()
        success, message = self.controller.ubah_anggota(self.selected_id, nama, alamat)
        messagebox.showinfo("Informasi", message)
        if success:
            self.clear_form()
            self.tampil_data()

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
            return
        success, message = self.controller.hapus_anggota(self.selected_id)
        messagebox.showinfo("Informasi", message)
        if success:
            self.clear_form()
            self.tampil_data()

    def pilih_data(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_id = values[0]
            self.entry_nama.delete(0, 'end')
            self.entry_nama.insert(0, values[1])
            self.entry_alamat.delete(0, 'end')
            self.entry_alamat.insert(0, values[2])

    def clear_form(self):
        self.selected_id = None
        self.entry_nama.delete(0, 'end')
        self.entry_alamat.delete(0, 'end')