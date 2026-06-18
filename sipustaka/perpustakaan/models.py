from django.db import models

# 1. Model Buku (Jangan sampai hilang!)
class Buku(models.Model):
    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)

    class Meta:
        db_table = 'perpustakaan_buku'

# 2. Model Siswa (Tambahan baru)
class Siswa(models.Model):
    nis = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)

    class Meta:
        db_table = 'perpustakaan_siswa'

class Peminjaman(models.Model):
    # Field standar untuk transaksi peminjaman:
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField(auto_now_add=True)
    tanggal_kembali = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Dipinjam')

    # Mengunci nama tabel agar terbaca oleh Raw SQL di views.py
    class Meta:
        db_table = 'perpustakaan_peminjaman'