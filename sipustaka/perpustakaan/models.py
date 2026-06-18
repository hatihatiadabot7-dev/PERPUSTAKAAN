from django.db import models

# 1. Model Buku - Disamakan dengan input Form & Raw SQL
class Buku(models.Model):
    judul = models.CharField(max_length=200)
    pengarang = models.CharField(max_length=100) # Menggantikan 'penulis' agar sesuai SQL
    kategori = models.CharField(max_length=100, default='Novel')
    penerbit = models.CharField(max_length=100, default='-')
    year_terbit = models.IntegerField(default=2020) # Sesuai dengan field year_terbit di SQL
    rak = models.CharField(max_length=50, default='Rak Utama')
    stok = models.IntegerField(default=0)
    deskripsi = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'perpustakaan_buku'

# 2. Model Siswa - Menambahkan field is_active
class Siswa(models.Model):
    nis = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True) # Tambahan baru agar sinkron dengan views.py

    class Meta:
        db_table = 'perpustakaan_siswa'

# 3. Model Peminjaman - Menambahkan keperluan dan jatuh_tempo
class Peminjaman(models.Model):
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    jatuh_tempo = models.DateField() # Menggantikan tanggal_kembali saat awal pinjam
    keperluan = models.CharField(max_length=255, default='Membaca Mandiri')
    status = models.CharField(max_length=20, default='Dipinjam')

    class Meta:
        db_table = 'perpustakaan_peminjaman'