from django.db import models

class Buku(models.Model):
    # Contoh kolom/field (sesuaikan dengan proyek kamu):
    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    
    # Jika kamu menggunakan Raw SQL manual, kamu bisa mengunci nama tabelnya di sini:
    class Meta:
        db_table = 'perpustakaan_buku'
        