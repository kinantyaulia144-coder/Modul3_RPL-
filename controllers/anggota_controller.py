# Kinanty Putri Aulia_004
import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView(self)
        self.selected_id = None

        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_perbarui.configure(command=self.perbarui_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.tree.bind("<ButtonRelease-1>", self.isi_form_dari_tabel)
        self.muat_data_tabel()
        self.view.mainloop()

    def get_all_anggota(self):
        return self.model.get_all_anggota()

    def muat_data_tabel(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        
        data_anggota = self.model.get_all_anggota()
        for anggota in data_anggota:
            self.view.tree.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['alamat']))

    def isi_form_dari_tabel(self, event):
        selected_item = self.view.tree.focus()
        if not selected_item:
            return
        
        row_data = self.view.tree.item(selected_item)["values"]
        if row_data:
            self.selected_id = row_data[0]
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_nama.insert(0, row_data[1])
            self.view.entry_alamat.delete(0, 'end')
            self.view.entry_alamat.insert(0, row_data[2])

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Nama dan Alamat tidak boleh kosong!")
            return

        berhasil = self.model.create_anggota(nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_alamat.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data anggota.")

    def perbarui_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang ingin diperbarui dari tabel!")
            return

        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        berhasil = self.model.update_anggota(self.selected_id, nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_alamat.delete(0, 'end')
            self.selected_id = None
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data anggota.")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang ingin dihapus dari tabel!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data anggota ini?"):
            berhasil = self.model.delete_anggota(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.view.entry_nama.delete(0, 'end')
                self.view.entry_alamat.delete(0, 'end')
                self.selected_id = None
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data anggota.")