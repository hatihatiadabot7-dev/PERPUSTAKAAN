from django.shortcuts import render, redirect
from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# ==========================================
# --- 1. DASHBOARD ---
# ==========================================
def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM perpustakaan_buku")
        total_buku = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM perpustakaan_siswa")
        total_siswa = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM perpustakaan_peminjaman WHERE status = 'Dipinjam'")
        total_dipinjam = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM perpustakaan_peminjaman WHERE status = 'Dikembalikan'")
        total_dikembalikan = cursor.fetchone()[0]

        # Ambil data buku untuk statistik ringkas
        cursor.execute("SELECT judul, stok FROM perpustakaan_buku ORDER BY judul ASC")
        buku_raw = dictfetchall(cursor)
        
        # Hitung persentase kapasitas stok buku
        daftar_buku_dashboard = []
        for b in buku_raw:
            stok_angka = b.get('stok', 0)
            percent = 100 if stok_angka > 10 else (stok_angka * 10)
            daftar_buku_dashboard.append({
                'judul': b['judul'],
                'stok': stok_angka,
                'persen': percent
            })

        # Hitung persentase untuk ringkasan transaksi
        total_transaksi = total_dipinjam + total_dikembalikan
        persen_dipinjam = (total_dipinjam / total_transaksi * 100) if total_transaksi > 0 else 0
        persen_dikembalikan = (total_dikembalikan / total_transaksi * 100) if total_transaksi > 0 else 0

    context = {
        'total_buku': total_buku,
        'total_siswa': total_siswa,
        'total_dipinjam': total_dipinjam,
        'total_dikembalikan': total_dikembalikan,
        'daftar_buku_dashboard': daftar_buku_dashboard,
        'persen_dipinjam': persen_dipinjam,
        'persen_dikembalikan': persen_dikembalikan,
    }
    return render(request, 'index.html', context)


# ==========================================
# --- 2. DATA SISWA (USER) ---
# ==========================================
def list_siswa(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM perpustakaan_siswa ORDER BY id DESC")
        daftar_siswa = dictfetchall(cursor)
    return render(request, 'users.html', {'users': daftar_siswa})

def tambah_siswa(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        nis = request.POST.get('nis')
        status = request.POST.get('status')
        is_active = True if status == 'True' else False
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO perpustakaan_siswa (nama, kelas, nis, is_active)
                VALUES (%s, %s, %s, %s)
            """, [nama, kelas, nis, is_active])
        return redirect('list_siswa')
    return render(request, 'add-user.html', {'siswa': None, 'is_edit': False})

def edit_siswa(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            nama = request.POST.get('nama')
            kelas = request.POST.get('kelas')
            nis = request.POST.get('nis')
            status = request.POST.get('status')
            is_active = True if status == 'True' else False
            
            cursor.execute("""
                UPDATE perpustakaan_siswa
                SET nama=%s, kelas=%s, nis=%s, is_active=%s
                WHERE id=%s
            """, [nama, kelas, nis, is_active, id])
            return redirect('list_siswa')
        else:
            cursor.execute("SELECT * FROM perpustakaan_siswa WHERE id = %s", [id])
            res = dictfetchall(cursor)
            siswa = res[0] if res else None
            return render(request, 'add-user.html', {'siswa': siswa, 'is_edit': True})

def detail_siswa(request, id):
    with connection.cursor() as cursor:
        # Ambil data profil siswa berdasarkan ID (pastiin casting integer aman)
        cursor.execute("SELECT * FROM perpustakaan_siswa WHERE id = %s", [int(id)])
        res = dictfetchall(cursor)
        siswa = res[0] if res else None
        
        # Inisialisasi variabel default
        total_peminjaman = 0
        total_peminjaman_aktif = 0
        persen_aktif = 0
        
        if siswa:
            siswa_id_real = siswa['id']
            
            # Hitung total semua transaksi peminjaman milik siswa ini
            cursor.execute("SELECT COUNT(*) FROM perpustakaan_peminjaman WHERE siswa_id = %s", [siswa_id_real])
            total_peminjaman = cursor.fetchone()[0] or 0
            
            # Hitung peminjaman aktif menggunakan LOWER() agar kebal dari variasi 'Dipinjam' / 'dipinjam'
            cursor.execute("""
                SELECT COUNT(*) 
                FROM perpustakaan_peminjaman 
                WHERE siswa_id = %s AND LOWER(status) = 'dipinjam'
            """, [siswa_id_real])
            total_peminjaman_aktif = cursor.fetchone()[0] or 0
            
            # Kalkulasi persentase untuk progress bar (Batas ideal 5 buku)
            max_pinjam_ideal = 5
            persen_aktif = min(100, int((total_peminjaman_aktif / max_pinjam_ideal) * 100)) if total_peminjaman_aktif > 0 else 0

    context = {
        'siswa': siswa,
        'total_peminjaman': total_peminjaman,
        'total_peminjaman_aktif': total_peminjaman_aktif,
        'persen_aktif': persen_aktif,
    }
    return render(request, 'detail_siswa.html', context)

def hapus_siswa(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            cursor.execute("DELETE FROM perpustakaan_siswa WHERE id = %s", [id])
            return redirect('list_siswa')
        else:
            cursor.execute("SELECT * FROM perpustakaan_siswa WHERE id = %s", [id])
            res = dictfetchall(cursor)
            siswa = res[0] if res else None
            return render(request, 'hapus_user_konfirmasi.html', {'siswa': siswa})


# ==========================================
# --- 3. DATA BUKU ---
# ==========================================
def list_buku(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM perpustakaan_buku ORDER BY id DESC")
        daftar_buku = dictfetchall(cursor)
    return render(request, 'buku.html', {'daftar_buku': daftar_buku})

def tambah_buku(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        pengarang = request.POST.get('pengarang')
        kategori = request.POST.get('kategori')
        penerbit = request.POST.get('penerbit')
        tahun_terbit = request.POST.get('tahun_terbit')
        rak = request.POST.get('rak')
        stok = int(request.POST.get('stok', 0))
        deskripsi = request.POST.get('deskripsi')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO perpustakaan_buku (judul, pengarang, kategori, penerbit, year_terbit, rak, stok, deskripsi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi])
        return redirect('list_buku')
    return render(request, 'tambah_buku.html', {'buku': None, 'is_edit': False})

def edit_buku(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            judul = request.POST.get('judul')
            pengarang = request.POST.get('pengarang')
            kategori = request.POST.get('kategori')
            penerbit = request.POST.get('penerbit')
            tahun_terbit = request.POST.get('tahun_terbit')
            rak = request.POST.get('rak')
            stok = int(request.POST.get('stok', 0))
            deskripsi = request.POST.get('deskripsi')
            cursor.execute("""
                UPDATE perpustakaan_buku
                SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s, tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s
                WHERE id=%s
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi, id])
            return redirect('list_buku')
        else:
            cursor.execute("SELECT * FROM perpustakaan_buku WHERE id = %s", [id])
            res = dictfetchall(cursor)
            buku = res[0] if res else None
            return render(request, 'tambah_buku.html', {'buku': buku, 'is_edit': True})

def detail_buku(request, id):
    with connection.cursor() as cursor:
        # Gunakan int(id) agar tipe data parameter ke SQL mentah selalu berupa integer
        cursor.execute("SELECT * FROM perpustakaan_buku WHERE id = %s", [int(id)])
        res = dictfetchall(cursor)
        buku = res[0] if res else None
        
    return render(request, 'detail_buku.html', {'buku': buku})

def hapus_buku(request, id):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            cursor.execute("DELETE FROM perpustakaan_buku WHERE id = %s", [id])
            return redirect('list_buku')
        else:
            cursor.execute("SELECT * FROM perpustakaan_buku WHERE id = %s", [id])
            res = dictfetchall(cursor)
            buku = res[0] if res else None
            return render(request, 'hapus_buku_konfirmasi.html', {'buku': buku})


# ==========================================
# --- 4. TRANSAKSI PEMINJAMAN ---
# ==========================================
def list_peminjaman(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama AS nama_siswa, b.judul AS judul_buku,
                   p.keperluan, p.tanggal_pinjam, p.jatuh_tempo, p.status
            FROM perpustakaan_peminjaman p
            INNER JOIN perpustakaan_siswa s ON p.siswa_id = s.id
            INNER JOIN perpustakaan_buku b ON p.buku_id = b.id
            ORDER BY p.id DESC
        """)
        peminjaman = dictfetchall(cursor)
    return render(request, 'peminjaman.html', {'peminjaman': peminjaman})

def tambah_peminjaman(request):
    if request.method == 'POST':
        nama_siswa_input = request.POST.get('nama_siswa', '').strip()
        judul_buku_input = request.POST.get('judul_buku', '').strip()
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        jatuh_tempo = request.POST.get('jatuh_tempo')
        keperluan = request.POST.get('keperluan', 'Membaca Mandiri')
        status = request.POST.get('status', 'Dipinjam')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM perpustakaan_siswa WHERE LOWER(nama) = LOWER(%s) LIMIT 1", [nama_siswa_input])
            siswa_row = cursor.fetchone()
            siswa_id = siswa_row[0] if siswa_row else None

            cursor.execute("SELECT id, stok FROM perpustakaan_buku WHERE LOWER(judul) = LOWER(%s) LIMIT 1", [judul_buku_input])
            buku_row = cursor.fetchone()
            buku_id = buku_row[0] if buku_row else None
            buku_stok = buku_row[1] if buku_row else 0

            if not siswa_id or not buku_id or buku_stok <= 0:
                cursor.execute("SELECT nama FROM perpustakaan_siswa ORDER BY nama ASC")
                siswa_list = [row[0] for row in cursor.fetchall()]
                cursor.execute("SELECT judul FROM perpustakaan_buku WHERE stok > 0 ORDER BY judul ASC")
                buku_list = [row[0] for row in cursor.fetchall()]
                
                if not siswa_id or not buku_id:
                    error_msg = "Nama Siswa atau Judul Buku tidak terdaftar di database! Pastikan ketikannya sama."
                else:
                    error_msg = f"Buku '{judul_buku_input}' yang dipilih sedang habis (Stok: 0)!"

                return render(request, 'tambah_peminjaman.html', {
                    'siswa_list': siswa_list, 'buku_list': buku_list, 'error': error_msg
                })

            # Eksekusi simpan transaksi pinjam
            cursor.execute("""
                INSERT INTO perpustakaan_peminjaman
                (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status])
            
            # Pengurangan stok otomatis dijalankan di sini
            cursor.execute("""
                UPDATE perpustakaan_buku
                SET stok = stok - 1
                WHERE id = %s
            """, [buku_id])
            
        return redirect('list_peminjaman')
        
    with connection.cursor() as cursor:
        cursor.execute("SELECT nama FROM perpustakaan_siswa ORDER BY nama ASC")
        siswa_list = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT judul FROM perpustakaan_buku WHERE stok > 0 ORDER BY judul ASC")
        buku_list = [row[0] for row in cursor.fetchall()]

    return render(request, 'tambah_peminjaman.html', {
        'siswa_list': siswa_list,
        'buku_list': buku_list
    })

def kembalikan_buku(request, id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("SELECT buku_id, status FROM perpustakaan_peminjaman WHERE id = %s", [id])
            row = cursor.fetchone()
            
            if row:
                buku_id = row[0]
                status_sekarang = row[1]
                
                if status_sekarang == 'Dipinjam':
                    cursor.execute("UPDATE perpustakaan_peminjaman SET status = 'Dikembalikan' WHERE id = %s", [id])
                    cursor.execute("UPDATE perpustakaan_buku SET stok = stok + 1 WHERE id = %s", [buku_id])
                
    return redirect('list_peminjaman')