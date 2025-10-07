# 📚 Aplikasi Perpustakaan Digital

Aplikasi **Perpustakaan Digital** ini dibuat menggunakan **Streamlit** dan **Supabase** sebagai backend database.  
Proyek ini bertujuan untuk mempermudah proses peminjaman, pengembalian, serta pengelolaan data buku secara digital dan real-time.

---

## 🧩 Fitur Utama

- 🔐 **Login dan Manajemen Akun**
  - Admin dan User memiliki hak akses berbeda.
  - Login menggunakan data dari tabel `akun`.

- 📖 **Manajemen Buku**
  - Tambah, ubah, hapus, dan cari buku berdasarkan judul, genre, atau tahun.
  - Upload cover dan file PDF buku ke database.

- 🔄 **Peminjaman Buku**
  - User dapat mengajukan peminjaman buku.
  - Admin dapat menyetujui, menolak, atau menandai buku sebagai dikembalikan.
  - Sistem otomatis menghitung stok buku.

- ⚙️ **Manajemen Data & Status**
  - Status buku dan peminjaman disesuaikan otomatis.
  - Validasi penghapusan buku: tidak bisa dihapus jika masih dipinjam.

---

## 🗂️ Struktur Database (Supabase)

Berikut tabel dan relasi antar tabel pada database:

![Database Schema](supabase-schema-bcalrkqeeoaalfpjrwvx.svg)

### 1. Tabel `akun`
| Kolom | Tipe Data | Deskripsi |
|-------|------------|-----------|
| id_user | int8 (PK) | ID unik pengguna |
| username | varchar | Nama pengguna |
| password | varchar | Kata sandi |
| level | varchar | Level akses (admin/user) |

### 2. Tabel `buku`
| Kolom | Tipe Data | Deskripsi |
|-------|------------|-----------|
| id_buku | int8 (PK) | ID unik buku |
| judul | varchar | Judul buku |
| penulis | text | Nama penulis |
| tahun | int8 | Tahun terbit |
| genre | text | Jenis/genre buku |
| stok | int8 | Jumlah stok buku |
| cover_url | varchar | URL cover buku |
| pdf_url | varchar | URL file PDF buku |
| deskripsi | text | Deskripsi singkat buku |

### 3. Tabel `peminjaman`
| Kolom | Tipe Data | Deskripsi |
|-------|------------|-----------|
| id_peminjaman | int8 (PK) | ID peminjaman |
| id_user | int8 (FK → akun.id_user) | Pengguna yang meminjam |
| id_buku | int8 (FK → buku.id_buku) | Buku yang dipinjam |
| tanggal_pinjam | date | Tanggal peminjaman |
| tanggal_kembali | date | Tanggal pengembalian |
| status | varchar | Status (dipinjam/dikembalikan) |
| denda | int8 | Denda (jika terlambat) |
| alamat | varchar | Alamat peminjam |
| nomor | int8 | Nomor telepon |
| ajuan | varchar | Status ajuan (menunggu/disetujui/ditolak) |
| created_at | timestamp | Waktu data dibuat |

### 4. Tabel `settings`
| Kolom | Tipe Data | Deskripsi |
|-------|------------|-----------|
| id | int4 (PK) | ID unik |
| hapus_buku_kembali | int4 | Pengaturan hapus otomatis |
| created_at | timestampz | Waktu dibuat |

---

## 🧠 Alur Sistem

1. **Login**
   - User atau admin masuk ke sistem menggunakan akun terdaftar.
2. **Dashboard**
   - Menampilkan daftar buku dan status peminjaman.
3. **Ajuan Peminjaman**
   - User memilih buku dan mengajukan peminjaman.
   - Admin menerima atau menolak pengajuan.
4. **Pengembalian Buku**
   - Setelah dikembalikan, status berubah menjadi *dikembalikan* dan stok bertambah.
5. **Manajemen Buku**
   - Admin bisa menambah, mengedit, atau menghapus buku (jika tidak sedang dipinjam).

---

## ⚙️ Teknologi yang Digunakan

| Komponen | Teknologi |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Supabase (PostgreSQL) |
| Bahasa | Python |
| Framework | Streamlit |
| Database Cloud | Supabase |
| Library tambahan | pandas, datetime, io |

---

## 🚀 Cara Menjalankan Proyek

1. **Clone Repository**
   ```bash
   git clone https://github.com/Andka670/perpustakaandigital.git
   cd perpustakaandigital
Instal Dependensi

bash
Salin kode
pip install -r requirements.txt
Konfigurasi Supabase

Buka file .py utama.

Isi variabel berikut sesuai dengan kredensial Supabase kamu:

python:
Salin kode
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
Jalankan Aplikasi

bash:
Salin kode
streamlit run app.py
Buka di Browser

arduino:
Salin kode
http://localhost:8501
🧑‍💻 Pengembang
Dibuat oleh Andka670(M. Andika Setiawan)
📎 GitHub: Andka670

