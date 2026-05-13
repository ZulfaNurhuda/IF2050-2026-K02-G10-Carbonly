# Carbonly

**Carbonly** adalah perangkat lunak pencatat jejak karbon (carbon footprint tracker) berbasis aplikasi desktop yang memungkinkan pengguna individu untuk mencatat dan mengelola log aktivitas harian, menghitung estimasi emisi karbon yang dihasilkan dari setiap aktivitas berdasarkan koefisien emisi yang telah ditetapkan, serta menetapkan dan memantau ketercapaian target emisi karbon harian.

---

## Teknologi

- **Bahasa:** Python 3.10+
- **GUI:** PyQt6 + PyQt6-Fluent-Widgets (Fluent Design) + PyQt6-Charts
- **Database:** SQLite3
- **Keamanan:** Argon2id (hashing password), Fernet AES (enkripsi session)
- **Build:** PyInstaller + Velopack

---

## Menjalankan Aplikasi

### Alternatif 1 — Via Release Installer (Direkomendasikan)

Unduh installer sesuai platform dari halaman [Releases](https://github.com/ZulfaNurhuda/IF2050-2026-K02-G10-Carbonly/releases):

| Platform | File |
|---|---|
| Windows | `Carbonly-win-Setup.exe` — jalankan langsung |
| macOS | `Carbonly-osx-Setup.pkg` — klik kanan lalu **Open** untuk bypass Gatekeeper |
| Linux | `Carbonly.AppImage` |

**Linux — prasyarat:**

Ubuntu 22.04+ tidak menyertakan `libfuse2` secara default. Pilih salah satu:

```bash
# Opsi A: install libfuse2 (sekali saja)
sudo apt-get install libfuse2
chmod +x Carbonly.AppImage
./Carbonly.AppImage

# Opsi B: jalankan tanpa install FUSE
chmod +x Carbonly.AppImage
APPIMAGE_EXTRACT_AND_RUN=1 ./Carbonly.AppImage
```

Data pengguna (database dan session) disimpan otomatis di direktori app data sistem dan tidak akan terhapus saat update:

| Platform | Lokasi |
|---|---|
| Windows | `%APPDATA%\Carbonly\Carbonly\` |
| macOS | `~/Library/Application Support/Carbonly/` |
| Linux | `~/.local/share/Carbonly/` |

---

### Alternatif 2 — Via Source (Development)

**Prasyarat:**
- Python 3.10 atau lebih baru
- pip (Python package manager)
- Git

**Langkah:**

1. Clone repository ini:
   ```bash
   git clone https://github.com/ZulfaNurhuda/IF2050-2026-K02-G10-Carbonly.git
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

4. Jalankan aplikasi:
   ```bash
   python main.py
   ```

Aplikasi akan otomatis membuat tabel-tabel basis data yang diperlukan pada pertama kali dijalankan.

**Mode Debug (Opsional)** — isi data demo user secara otomatis:
```bash
export CARBONLY_DEBUG="MinimalKasiSpesifikasiYangKonsistenMasMba"
python main.py
```

---

## Daftar Modul yang Diimplementasikan

| No | Nama Modul | Kelas yang Diimplementasikan |
|---|---|---|
| 1 | **Autentikasi & Profil** | `User`, `AuthController`, `AuthService`, `LoginView`, `ProfileView` |
| 2 | **Log Aktivitas** | `ActivityLog`, `ActivityCategory`, `EmissionCoefficient`, `ActivityLogController`, `ActivityLogFormView` |
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

### 1. `users`
Tabel untuk menyimpan data pengguna aplikasi.

| Atribut | Tipe Data | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `username` | TEXT | UNIQUE NOT NULL |
| `password_hash` | TEXT | NOT NULL |

### 2. `log_aktivitas`
Tabel untuk menyimpan data log aktivitas harian pengguna.

| Atribut | Tipe Data | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `user_id` | INTEGER | REFERENCES users(id) |
| `tanggal` | TEXT | NOT NULL |
| `kategori` | TEXT | NOT NULL |
| `nilai_aktivitas` | REAL | NOT NULL |
| `satuan_aktivitas` | TEXT | NOT NULL |
| `total_emisi` | REAL | — |

### 3. `koefisien_emisi`
Tabel untuk menyimpan koefisien emisi default berdasarkan kategori aktivitas.

| Atribut | Tipe Data | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `kategori` | TEXT | NOT NULL UNIQUE |
| `nilai_koefisien` | REAL | NOT NULL |
| `satuan` | TEXT | NOT NULL |

**Data Awal (Seed):**

| Kategori | Nilai Koefisien | Satuan |
|---|---|---|
| Transportasi | 0.21 | kg CO2e/km |
| Listrik | 0.87 | kg CO2e/kWh |
| Gas Alam | 2.04 | kg CO2e/m³ |
| Makanan | 0.50 | kg CO2e/kg |
| Sampah | 0.44 | kg CO2e/kg |

### 4. `target_emisi`
Tabel untuk menyimpan target emisi harian pengguna.

| Atribut | Tipe Data | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `user_id` | INTEGER | REFERENCES users(id) |
| `nilai_target` | REAL | NOT NULL |
| `satuan` | TEXT | — |
| `tahun` | INTEGER | NOT NULL |

---

## Pembagian Tugas Implementasi

| NIM | Nama | GitHub | Modul | Kelas yang Diimplementasikan |
|---|---|---|---|---|
| 18224052 | Arkandhiya Ibrahim Dewantara | @snailsquid | Account Creation, Framework Initialization | `User`, `AuthController` (login, register), `AuthService`, `LoginView`, `DBContext`, `AppPaths`, `MainWindow`, `HomePage` |
| 18224064 | Muhammad Zulfa Fauzan Nurhuda | @ZulfaNurhuda | Account Modification, Build & Infrastructure | `AuthController` (update_username, update_password), `ProfileView`, CI/CD, build pipeline |
| 18224070 | Almer Zain Farisseno | @Almerosaurus | Log Aktivitas Form | `ActivityLog`, `ActivityCategory`, `EmissionCoefficient`, `ActivityLogController`, `ActivityLogFormView` |
| 18224076 | Bram Sebastian Pangaribuan | @KimoonTheCreator | Rekapitulasi | `SummaryController`, `HomePage` (bagian rekapitulasi & grafik) |
| 18224098 | Nicholas Putra Halim | @nicholasphalim | Target Harian | `EmissionTarget`, `EmissionTargetController`, `EmissionTargetFormView` |
| 18224038 | Christian Wilfredo Pakpahan | @willeosix | Log Aktivitas View | `HomePage` (bagian daftar log aktivitas) |
