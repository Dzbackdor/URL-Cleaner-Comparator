````markdown
# Python URL / Host / File Comparator

🐍 Script Python untuk membersihkan duplikat dan membandingkan daftar:

- URL
- Domain
- Host/Subdomain
- Nama File

Script ini cocok digunakan untuk mengelola daftar backlink, domain, subdomain, maupun nama file seperti hasil crawl Common Crawl.

<img src="/comparator.png" width="700" alt="Python URL Comparator">

## Rekomendasi Tools

Tools ini dapat digunakan bersama:

- https://github.com/Dzbackdor/moz-pro-without-api-key

---

# Features

- ✅ Membersihkan duplikat URL
- ✅ Membersihkan duplikat Domain
- ✅ Membersihkan duplikat Host/Subdomain
- ✅ Membersihkan duplikat Nama File
- ✅ Membandingkan file baru dengan file lama
- ✅ Normalisasi URL otomatis
- ✅ Opsi penambahan slash (`/`) di akhir URL
- ✅ Opsi menggabungkan file lama dengan data baru (`--merge-old`)
- ✅ Output berwarna (Colorama)

---

# Instalasi

Clone repository

```bash
git clone https://github.com/Dzbackdor/URL-Cleaner-Comparator.git
cd URL-Cleaner-Comparator
```

Install dependency

```bash
pip install -r requirements.txt
```

Melihat bantuan

```bash
python new.py -h
```

---

# Penggunaan

## Membersihkan Duplikat URL

```bash
python new.py \
-l url.txt \
-m url \
-o hasil.txt
```

---

## Membersihkan Duplikat Domain

```bash
python new.py \
-l url.txt \
-m domain \
-o hasil.txt
```

---

## Membersihkan Duplikat Host/Subdomain

```bash
python new.py \
-l host.txt \
-m host \
-o hasil.txt
```

Contoh isi file:

```text
google.com
google.com
mail.google.com
api.google.com
mail.google.com
```

Output:

```text
google.com
mail.google.com
api.google.com
```

---

## Membersihkan Duplikat Nama File

```bash
python new.py \
-l files.txt \
-m file \
-o hasil.txt
```

Contoh isi file:

```text
CC-MAIN-001.txt
CC-MAIN-001.txt
CC-MAIN-002.txt
CC-MAIN-003.txt
```

Output:

```text
CC-MAIN-001.txt
CC-MAIN-002.txt
CC-MAIN-003.txt
```

---

# Membandingkan Dua File

## URL

```bash
python new.py \
-l baru.txt \
-c lama.txt \
-m url \
-o hasil.txt
```

Output hanya berisi URL yang belum ada pada file lama.

---

## Domain

```bash
python new.py \
-l baru.txt \
-c lama.txt \
-m domain \
-o hasil.txt
```

Output hanya berisi domain yang belum ada.

---

## Host/Subdomain

```bash
python new.py \
-l host-baru.txt \
-c host-lama.txt \
-m host \
-o hasil.txt
```

---

## Nama File

```bash
python new.py \
-l file-baru.txt \
-c file-lama.txt \
-m file \
-o hasil.txt
```

---

# Merge Output

Secara default output hanya berisi data baru.

Jika ingin menggabungkan isi file lama dengan data baru gunakan:

```bash
python new.py \
-l baru.txt \
-c lama.txt \
-m domain \
-o hasil.txt \
--merge-old
```

Output:

```text
Isi file lama
+
Semua data baru yang belum ada
```

---

# Menambahkan Slash

Script dapat menambahkan slash (`/`) pada akhir URL.

Contoh:

Input

```text
https://example.com/path
```

Perintah

```bash
python new.py \
-l url.txt \
-m url \
-o hasil.txt \
-s
```

Output

```text
https://example.com/path/
```

Opsi yang sama dapat ditulis sebagai:

```bash
--slash
```

---

# Mode

## URL

Membandingkan URL secara penuh.

Contoh:

```text
https://example.com/a
https://example.com/b
```

Dianggap **berbeda**.

---

## Domain

Membandingkan berdasarkan domain.

Contoh:

```text
https://example.com/a
https://example.com/b
```

Dianggap **sama** karena berasal dari domain yang sama.

Output tetap menggunakan URL pertama yang ditemukan.

---

## Host

Digunakan untuk daftar domain atau subdomain.

Contoh:

```text
example.com
api.example.com
mail.example.com
```

Setiap host dianggap berbeda.

---

## File

Digunakan untuk membandingkan nama file.

Contoh:

```text
CC-MAIN-20251007013002-00574.txt
CC-MAIN-20251007013002-00575.txt
```

---

# Parameter

| Parameter | Keterangan |
|------------|------------|
| `-l`, `--list` | File input |
| `-o`, `--output` | File output |
| `-m`, `--mode` | Mode (`url`, `domain`, `host`, `file`) |
| `-c`, `--compare` | File lama untuk dibandingkan |
| `--merge-old` | Gabungkan isi file lama dengan data baru |
| `-s`, `--slash` | Tambahkan slash (`/`) di akhir URL |

---

# Contoh Penggunaan

Membersihkan URL

```bash
python new.py -l url.txt -m url -o output.txt
```

Membersihkan Domain

```bash
python new.py -l url.txt -m domain -o output.txt
```

Membersihkan Host

```bash
python new.py -l host.txt -m host -o output.txt
```

Membersihkan Nama File

```bash
python new.py -l files.txt -m file -o output.txt
```

Membandingkan URL

```bash
python new.py -l baru.txt -c lama.txt -m url -o hasil.txt
```

Membandingkan Domain

```bash
python new.py -l baru.txt -c lama.txt -m domain -o hasil.txt
```

Merge Output

```bash
python new.py -l baru.txt -c lama.txt -m domain -o hasil.txt --merge-old
```

Tambah Slash

```bash
python new.py -l url.txt -m url -o hasil.txt -s
```

---

# Format File Input

## URL

```text
https://example.com
https://google.com/search
https://github.com
```

---

## Host

```text
google.com
mail.google.com
api.google.com
```

---

## Nama File

```text
CC-MAIN-20251007013002-00574.txt
CC-MAIN-20251007013002-00575.txt
```

---

# Output

Seluruh hasil akan disimpan ke file yang ditentukan menggunakan parameter:

```bash
-o output.txt
```

Parameter ini **wajib** diberikan.

---

# Troubleshooting

## File tidak ditemukan

```text
Error: File tidak ditemukan
```

Pastikan nama file benar atau gunakan path lengkap.

---

## URL tidak valid

URL yang tidak valid akan diabaikan dan dihitung pada statistik akhir.

---

## Encoding

Gunakan file UTF-8 agar seluruh karakter dapat dibaca dengan benar.

---

# Kontribusi

1. Fork repository
2. Buat branch baru

```bash
git checkout -b fitur-baru
```

3. Commit

```bash
git commit -m "Tambah fitur baru"
```

4. Push

```bash
git push origin fitur-baru
```

5. Buat Pull Request

---

# Author

**Dzbackdor**

GitHub:

https://github.com/Dzbackdor

---

# Changelog

## v2.0.0

- ✅ Perbandingan URL
- ✅ Perbandingan Domain
- ✅ Perbandingan Host/Subdomain
- ✅ Perbandingan Nama File
- ✅ Duplicate Cleaner
- ✅ Merge Output
- ✅ Slash Normalization
- ✅ URL Normalization
- ✅ Colored CLI Output

---

Made with ❤️ by **Dzone**
````
