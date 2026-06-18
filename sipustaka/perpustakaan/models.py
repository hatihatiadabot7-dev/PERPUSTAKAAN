from django.db import models  # <-- Pastikan baris ini ada di paling atas!

class Siswa(models.Model):
    nis = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)

    class Meta:
        db_table = 'perpustakaan_siswa'