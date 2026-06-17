from django.urls import path
from . import views

urlpatterns = [
    # Halaman Pertama 
    path('', views.dashboard, name='dashboard'),
    
    # Rute Buku
    path('buku/', views.list_buku, name='list_buku'),
    path('buku/tambah/', views.tambah_buku, name='tambah_buku'),
    path('buku/edit/<int:id>/', views.edit_buku, name='edit_buku'),
    path('buku/detail/<int:id>/', views.detail_buku, name='detail_buku'),
    path('buku/hapus/<int:id>/', views.hapus_buku, name='hapus_buku'),
    
    # Rute Siswa
    path('users/', views.list_siswa, name='list_siswa'),
    path('users/tambah/', views.tambah_siswa, name='tambah_siswa'),
    path('users/edit/<int:id>/', views.edit_siswa, name='edit_siswa'),
    path('users/detail/<int:id>/', views.detail_siswa, name='detail_siswa'),
    path('users/hapus/<int:id>/', views.hapus_siswa, name='hapus_siswa'),
    
    # Rute Peminjaman
    path('peminjaman/', views.list_peminjaman, name='list_peminjaman'),
    path('peminjaman/tambah/', views.tambah_peminjaman, name='tambah_peminjaman'),
    path('peminjaman/kembalikan/<int:id>/', views.kembalikan_buku, name='kembalikan_buku'),
]