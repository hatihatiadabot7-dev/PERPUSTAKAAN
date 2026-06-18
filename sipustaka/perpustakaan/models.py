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