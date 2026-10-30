import sys
import os

# Menambahkan direktori root 'modul 3' ke sys.path agar folder 'models' terbaca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
  # Menginisialisasi Model
  model = BukuModel()

  # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
  model.conn = MagicMock()
  mock_cursor = MagicMock()
  model.conn.cursor.return_value = mock_cursor

  # Melakukan eksekusi fungsi
  hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

  # Memverifikasi apakah fungsi mengembalikan nilai True
  assert hasil is True
  # Memverifikasi apakah cursor.execute benar-benar dipanggil
  mock_cursor.execute.assert_called_once()
  # Memverifikasi apakah perintah commit (simpan) dipanggil
  model.conn.commit.assert_called_once()

def test_get_all_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Menentukan data dummy yang dikembalikan oleh fetchall()
    dummy_data = [
        (1, "Belajar Python", "RPL Untad", 2025),
        (2, "Struktur Data", "Tim Dosen", 2026)
    ]
    mock_cursor.fetchall.return_value = dummy_data

    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()

    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()

    # Memverifikasi apakah hasil kembalian sesuai dengan data dummy
    assert len(hasil) == 2