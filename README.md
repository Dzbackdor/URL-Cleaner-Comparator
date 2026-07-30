# Python URL / Host / File Comparator

Python script untuk membersihkan duplikat dan membandingkan daftar URL, Domain, Host/Subdomain, maupun Nama File.

## Features

- Membersihkan duplikat URL
- Membersihkan duplikat Domain
- Membersihkan duplikat Host/Subdomain
- Membersihkan duplikat Nama File
- Membandingkan file baru dengan file lama
- Normalisasi URL otomatis
- Menambahkan trailing slash pada URL (`-s` / `--slash`)
- Menggabungkan file lama dengan data baru (`--merge-old`)
- Output terminal berwarna

## Requirements

- Python 3.8+
- colorama

## Installation

```bash
git clone https://github.com/Dzbackdor/URL-Cleaner-Comparator.git
cd URL-Cleaner-Comparator
pip install -r requirements.txt
```

Melihat bantuan:

```bash
python new.py -h
```

## Command Line Options

| Parameter | Keterangan |
|-----------|------------|
| `-l`, `--list` | File input |
| `-o`, `--output` | File output |
| `-m`, `--mode` | `url`, `domain`, `host`, `file` |
| `-c`, `--compare` | File lama untuk dibandingkan |
| `--merge-old` | Gabungkan isi file lama dengan data baru |
| `-s`, `--slash` | Tambahkan `/` di akhir URL |

## Mode

### url

Membandingkan URL secara penuh.

```bash
python new.py -l url.txt -m url -o hasil.txt
```

### domain

Membandingkan berdasarkan domain.

```bash
python new.py -l url.txt -m domain -o hasil.txt
```

Satu URL pertama akan dipertahankan untuk setiap domain.

### host

Digunakan untuk daftar host atau subdomain.

```bash
python new.py -l host.txt -m host -o hasil.txt
```

Contoh input:

```text
example.com
mail.example.com
api.example.com
```

### file

Digunakan untuk membandingkan nama file.

```bash
python new.py -l files.txt -m file -o hasil.txt
```

Contoh input:

```text
list-001.txt
list-002.txt
```

## Compare Mode

Bandingkan file baru dengan file lama.

### URL

```bash
python new.py -l baru.txt -c lama.txt -m url -o hasil.txt
```

### Domain

```bash
python new.py -l baru.txt -c lama.txt -m domain -o hasil.txt
```

### Host

```bash
python new.py -l host-baru.txt -c host-lama.txt -m host -o hasil.txt
```

### File

```bash
python new.py -l file-baru.txt -c file-lama.txt -m file -o hasil.txt
```

Output hanya berisi data yang belum ada pada file lama.

## Merge Output

```bash
python new.py -l baru.txt -c lama.txt -m domain -o hasil.txt --merge-old
```

Output akan berisi:

- Seluruh isi file lama
- Data baru yang belum ada

## Trailing Slash

Tambahkan slash di akhir URL.

```bash
python new.py -l url.txt -m url -o hasil.txt -s
```

Input:

```text
https://example.com/path
```

Output:

```text
https://example.com/path/
```

## Format Input

### URL

```text
https://example.com
https://example.com/page
```

### Host

```text
example.com
mail.example.com
```

### File

```text
list-20251007013002-00574.txt
```

## Notes

- Mode `url` membandingkan URL secara penuh.
- Mode `domain` membandingkan berdasarkan domain tetapi menyimpan URL pertama.
- Mode `host` digunakan untuk daftar host/subdomain.
- Mode `file` digunakan untuk daftar nama file.
- Parameter `-o` wajib digunakan.
- URL yang tidak valid akan dilewati otomatis.

## Troubleshooting

### File tidak ditemukan

Pastikan nama file benar atau gunakan path lengkap.

### URL tidak valid

URL yang tidak valid akan diabaikan dan tidak dimasukkan ke output.

### Encoding

Gunakan file UTF-8.

## Contributing

1. Fork repository.
2. Buat branch baru.
3. Commit perubahan.
4. Push ke repository.
5. Buat Pull Request.

## Author

Dzbackdor

https://github.com/Dzbackdor

## Changelog

### v2.0.0

- URL compare
- Domain compare
- Host compare
- File compare
- Duplicate cleaner
- Merge output
- Slash normalization
- URL normalization
