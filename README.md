# Carbonly

**Carbonly** adalah perangkat lunak pencatat jejak karbon (carbon footprint tracker) berbasis aplikasi desktop yang memungkinkan pengguna individu untuk mencatat dan mengelola log aktivitas harian, menghitung estimasi emisi karbon yang dihasilkan dari setiap aktivitas berdasarkan koefisien emisi yang telah ditetapkan, serta menetapkan dan memantau ketercapaian target emisi karbon harian.

Aplikasi ini dibangun menggunakan bahasa pemrograman **Python 3.10+** dengan framework antarmuka pengguna **PyQt6** dan **PyQt6-Fluent-Widgets** untuk tampilan modern, basis data **SQLite** lokal, serta pustaka **PyQt6-Charts** untuk visualisasi data rekapitulasi emisi.

---

## Prasyarat dan Instalasi

### Prasyarat
- Python 3.10 atau lebih baru
- pip (Python package manager)
- Git

### Instalasi

1. Clone repository ini:
   ```bash
   git clone <repository-url>
   cd IF2050-2026-K02-G10-Carbonly
   ```

2. Buat virtual environment (disarankan):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. Install semua dependency:
   ```bash
   pip install -r requirements.txt
   ```

---

## Cara Menjalankan Aplikasi

Untuk menjalankan aplikasi, gunakan perintah berikut dari root direktori proyek:

```bash
python main.py
```

Aplikasi akan otomatis membuat tabel-tabel basis data yang diperlukan pada pertama kali dijalankan.

### Mode Debug (Opsional)
Untuk mengisi data demo user secara otomatis, set environment variable:
```bash
export CARBONLY_DEBUG="MinimalKasiSpesifikasiYangKonsistenMasMba"
python main.py
```

---

## Daftar Modul yang Diimplementasikan

| No | Nama Modul | Kelas yang Diimplementasikan |
|---|---|---|
| 1 | **Autentikasi & Profil** | `User`, `AuthController`, `AuthService`, `LoginView`, `ProfileView` |
| 2 | **Log Aktivitas** | `ActivityLog`, `EmissionCoefficient`, `ActivityLogController`, `ActivityLogFormView` |
| 3 | **Target Emisi** | `EmissionTarget`, `EmissionTargetController`, `EmissionTargetFormView` |
| 4 | **Rekapitulasi Emisi** | `SummaryController` (terintegrasi dalam `HomePage`) |
| 5 | **Halaman Utama & Window** | `HomePage`, `MainWindow` |
| 6 | **Basis Data & Utilitas** | `DBContext`, `AppPaths` |

### Use Case yang Diimplementasikan
- **UC01** — Menambahkan Log Aktivitas
- **UC02** — Melihat Daftar Log Aktivitas
- **UC03** — Melihat Rekapitulasi Emisi (Harian & Mingguan)
- **UC04** — Mengubah Log Aktivitas
- **UC05** — Menghapus Log Aktivitas
- **UC06** — Menetapkan Target Emisi Harian
- **UC07** — Mengubah Target Emisi Harian
- **UC08** — Login
- **UC09** — Register
- **UC10** — Logout
- **UC11** — Lihat Profile
- **UC12** — Ubah Profile (Username & Password)

---

## Daftar Tabel Basis Data

Berikut adalah tabel-tabel basis data SQLite yang diimplementasikan beserta atributnya:

### 1. `users`
Tabel untuk menyimpan data pengguna aplikasi.

| Atribut | Tipe Data | Constraints |
|---------|-----------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| username | TEXT | UNIQUE NOT NULL |
| password_hash | TEXT | NOT NULL |

### 2. `log_aktivitas`
Tabel untuk menyimpan data log aktivitas harian pengguna.

| Atribut | Tipe Data | Constraints |
|---------|-----------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| user_id | INTEGER | REFERENCES users(id) |
| tanggal | TEXT | NOT NULL |
| kategori | TEXT | NOT NULL |
| nilai_aktivitas | REAL | NOT NULL |
| satuan_aktivitas | TEXT | NOT NULL |
| total_emisi | REAL | — |

### 3. `koefisien_emisi`
Tabel untuk menyimpan koefisien emisi default berdasarkan kategori aktivitas.

| Atribut | Tipe Data | Constraints |
|---------|-----------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| kategori | TEXT | NOT NULL UNIQUE |
| nilai_koefisien | REAL | NOT NULL |
| satuan | TEXT | NOT NULL |

**Data Awal (Seed):**
| Kategori | Nilai Koefisien | Satuan |
|----------|-----------------|--------|
| Transportasi | 0.21 | kg CO2e/km |
| Listrik | 0.87 | kg CO2e/kWh |
| Gas Alam | 2.04 | kg CO2e/m³ |
| Makanan | 0.50 | kg CO2e/kg |
| Sampah | 0.44 | kg CO2e/kg |

### 4. `target_emisi`
Tabel untuk menyimpan target emisi harian pengguna.

| Atribut | Tipe Data | Constraints |
|---------|-----------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| user_id | INTEGER | REFERENCES users(id) |
| nilai_target | REAL | NOT NULL |
| satuan | TEXT | — |
| tahun | INTEGER | NOT NULL |

---

## Pembagian Tugas Implementasi

Berikut adalah pembagian tugas implementasi per anggota kelompok K02-G10 beserta kelas yang diimplementasikan:

| NIM | Nama | Kelas yang Diimplementasikan | Modul |
|-----|------|------------------------------|-------|
| 18224052 | Arkandhiya Ibrahim Dewantara | `User`, `LoginView`, `AuthController` (login/register), `AuthService`, `DBContext`, `AppPaths`, `MainWindow`, `HomePage` | Autentikasi, Basis Data, Window & Home |
| 18224064 | Muhammad Zulfa Fauzan Nurhuda | `ProfileView`, `AuthController` (update username/password) | Modifikasi Profil |
| 18224070 | Almer Zain Farisseno | `ActivityLog`, `EmissionCoefficient`, `ActivityLogController`, `ActivityLogFormView` | Log Aktivitas (Form Input) |
| 18224076 | Bram Sebastian Pangaribuan | `SummaryController`, `HomePage` (bagian rekapitulasi & grafik) | Rekapitulasi Emisi |
| 18224098 | Nicholas Putra Halim | `EmissionTarget`, `EmissionTargetController`, `EmissionTargetFormView` | Target Emisi |
| 18224038 | Christian Wilfredo Pakpahan | `ActivityLogFormView` (assist), `HomePage` (bagian daftar log) | Log Aktivitas (Daftar & Integrasi) |

> **Catatan:** Seluruh anggota turut berkontribusi dalam integrasi, perbaikan bug, dan refinement UI secara kolaboratif melalui branch `development`.

---

## Informasi Tambahan

- **Tim Pengembang:** Kelompok K02-G10 — Program Studi Sistem dan Teknologi Informasi, STEI-ITB
- **Lisensi:** MIT
- **Tech Stack:** Python 3.10+, PyQt6, PyQt6-Fluent-Widgets, PyQt6-Charts, SQLite, argon2-cffi, cryptography
