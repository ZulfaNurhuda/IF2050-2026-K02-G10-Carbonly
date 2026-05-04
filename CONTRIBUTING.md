# Panduan Kontribusi Perangkat Lunak Carbonly

Baca panduan ini sebelum mulai mengerjakan apapun agar alur kerja tim tetap rapi dan konsisten.

---

## Alur Kerja (_Git Flow_)

```
main ← (Kode yang bener-bener final & siap dibuat _release_, harus lewat acc maintainer)
 └── development ← (Integrasi semua fitur, sama harus lewat acc maintainer)
       └── feat/nama-fitur    ← lu pada ngerjain di branch beginian (bikin aja)
       └── fix/nama-bug
       └── docs/nama-doc
```

**Jangan pernah push langsung ke `main` atau `development` tanpa lewat PR.** _Selain gabisa, nanti rusak juga kalo langsung push main_

---

## Konvensi Penamaan Branch

Format: `<tipe>/<nama-fitur>`

| Tipe | Contoh |
|------|--------|
| `feat` | `feat/log-aktivitas` |
| `fix` | `fix/kalkulasi-emisi` |
| `docs` | `docs/update-readme` |
| `refactor` | `refactor/controller-layer` |
| `test` | `test/unit-log-aktivitas` |

Pake **huruf kecil** dan **tanda hubung** (-), bukan spasi atau underscore.

---

## Konvensi Commit Message (_Semantic Commit_)

Format: `<tipe>(<scope>): <deskripsi>`

> `<scope>` ini kalo kata guideline bersifat _opsional_, tapi sangat dianjurkan untuk kejelasan.

| Tipe | Kapan dipakai |
|------|---------------|
| `feat` | Menambah fitur baru |
| `fix` | Memperbaiki bug |
| `docs` | Mengubah dokumentasi |
| `style` | Perubahan formatting, spasi, dll (tidak mengubah logika) |
| `refactor` | Perubahan kode yang tidak menambah fitur |
| `test` | Menambahkan atau memperbaiki pengujian |
| `chore` | Tugas rutin (build, dependency, dll) |

**Contoh orang baik kalo commit:** `[+1000 social credit]`
```
feat(log-aktivitas): tambah form input transportasi
fix(kalkulasi): perbaiki emisi saat nilai input kosong
docs(readme): update daftar modul implementasi
refactor(controller): pisahkan LogAktivitasController
test(entity): tambah unit test KoefisienEmisi
chore(deps): update requirements.txt
```

**Contoh orang jahat kalo commit:**
```
update kode
Fix Bug
ubah semua file
```

---

## Langkah Kontribusi

1. **Ambil task** dari GitHub Issues, pastiin sudah di-assign ke lu (nanti _discuss_ bareng lah buat bagi tugas).

2. **Buat branch** dari `development` ← PASTIIN DARI SINI YGY
   ```bash
   git checkout development
   git pull origin development
   git checkout -b feat/nama-fitur
   ```
3. **Kerjakan dan commit** kalo kata asisten mah secara kecil dan sering, biar kalo ada _brain error_ (tipikal anak STI _vibecoding_ gg geming) bisa di-revert.
   ```bash
   git add .
   git commit -m "feat(log-aktivitas): tambah form input transportasi"
   ```
4. **Push branch** ke remote
   ```bash
   git push origin feat/nama-fitur
   ```
5. **Buat Pull Request** ke branch `development` di GitHub

6. **Isi PR template** dengan lengkap (templatenya nanti gua sediain ygy biar seragam), sertakan deskripsi dan screenshot jika ada perubahan UI.

7. **Tunggu review** dari minimal 1 anggota lain (sama harus diacc maintainer). BTW nanti ada autoreview dari copilot (kalo copilot lu belom limit harian) tentang kode yang di bikin PR.

8. **Maintainer** (Zulfa & Ark) yang nanti bakal merge ke branch `main`.

---

## Track Tasks via GitHub Issues

- Pecah fitur besar menjadi task yang lebih kecil
- Assign issue ke anggota yang mengerjakan
- Hubungkan PR dengan issue: tulis `Closes #[nomor]` di deskripsi PR
- Tutup (close) issue jika pengerjaan selesai

---

## Sebelum Bikin PR, Pastiin Beberapa Hal Ini Ye

- [ ] Kode sudah dicoba jalan di lokal
- [ ] Tidak ada konflik dengan branch target
- [ ] Nama branch sesuai konvensi
- [ ] Commit message sesuai format semantic commit
- [ ] Tidak ada file yang tidak perlu ikut ter-commit (`.env`, `__pycache__`, file IDE, dll)
- [ ] PR template sudah diisi lengkap
- [ ] Screenshot dilampirkan jika ada perubahan UI
