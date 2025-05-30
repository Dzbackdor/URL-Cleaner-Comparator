# Python SEO Tools - URL Cleaner & Comparator

🐍 Script Python untuk membersihkan duplikat URL dari file backlinks dan membandingkan dua file URL untuk menemukan URL yang belum ada.

<img src="/comparator.png" width="600" alt="URL-Cleaner-Comparator">

Rekomendasi menggunakan tools ini dengan tools pelengkapnya
- [moz-pro-without-api-key](https://github.com/Dzbackdor/moz-pro-without-api-key)

## Fitur

- ✅ **Pembersihan Duplikat**: Hapus duplikat URL berdasarkan URL exact atau domain
- ✅ **Perbandingan File**: Bandingkan file baru dengan file lama untuk menemukan URL yang belum ada
- ✅ **Normalisasi URL**: Otomatis menormalisasi URL untuk konsistensi
- ✅ **Mode Fleksibel**: Pilih perbandingan berdasarkan domain atau URL lengkap
- ✅ **Statistik Detail**: Laporan lengkap tentang proses pembersihan/perbandingan

## 📦 Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/Dzbackdor/URL-Cleaner-Comparator.git
cd URL-Cleaner-Comparator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Melihat bantuan:**
```bash
python cek.py -h
```

## 🎯 Penggunaan

### 1. Membersihkan Duplikat URL

#### Hapus duplikat berdasarkan domain (1 URL per domain):
```bash
python cek.py lama.txt --mode domain
```

#### Hapus duplikat URL exact:
```bash
python cek.py lama.txt --mode url
```

#### Dengan output file custom:
```bash
python cek.py backlinks.txt --mode domain --output hasil_bersih.txt
```

### 2. Membandingkan Dua File URL

#### Perbandingan berdasarkan domain:
```bash
python cek.py baru.txt --compare lama.txt --compare-mode domain
```

#### Perbandingan berdasarkan URL lengkap:
```bash
python cek.py baru.txt --compare lama.txt --compare-mode url
```

#### Dengan output file custom:
```bash
python cek.py baru.txt --compare lama.txt --compare-mode domain --output url_belum_ada.txt
```



## 🎮 Contoh Penggunaan

### Contoh 1: Membersihkan Duplikat Domain

**File input (`backlinks.txt`):**
```
https://google.com
https://google.com/search
https://facebook.com/page1
https://facebook.com/page2
https://twitter.com
```

**Perintah:**
```bash
python cek.py backlinks.txt --mode domain
```

**Output (`backlinks_bersih_domain.txt`):**
```
https://google.com
https://facebook.com/page1
https://twitter.com
```



### Contoh 2: Perbandingan File (Mode Domain)

**File lama (`lama.txt`):**
```
https://google.com
https://facebook.com/page1
```

**File baru (`baru.txt`):**
```
https://google.com/search
https://google.com/maps
https://facebook.com/page2
https://twitter.com
https://instagram.com/profile
```

**Perintah:**
```bash
python cek.py baru.txt --compare lama.txt --compare-mode domain
```

**Output (`baru_domain_baru.txt`):**
```
https://twitter.com
https://instagram.com/profile
```


### Contoh 3: Perbandingan File (Mode URL)

**Dengan file yang sama seperti Contoh 2:**

**Perintah:**
```bash
python cek.py baru.txt --compare lama.txt --compare-mode url
```

**Output (`baru_url_baru.txt`):**
```
https://google.com/search
https://google.com/maps
https://facebook.com/page2
https://twitter.com
https://instagram.com/profile
```


## 🔗 Parameter dan Opsi

### Parameter Wajib
- `input_file`: File input dengan daftar URL

### Parameter Opsional

#### Mode Pembersihan
- `--mode {url,domain}`: Mode pembersihan (default: domain)
  - `url`: Hapus duplikat URL exact
  - `domain`: Satu URL per domain

#### Mode Perbandingan
- `--compare FILE_LAMA`: Bandingkan dengan file lama
- `--compare-mode {url,domain}`: Mode perbandingan (default: domain)
  - `url`: Perbandingan URL exact
  - `domain`: Perbandingan berdasarkan domain

#### Output
- `--output FILE`: Nama file output (default: otomatis)

## 📋 Format File Input

File input harus berupa file teks (.txt) dengan satu URL per baris:

```
https://example.com
http://google.com/search
facebook.com/page
www.twitter.com
```

**Catatan:** Script akan otomatis menormalisasi URL (menambah http://, menghapus www untuk perbandingan, dll.)

## Nama File Output Otomatis

| Mode | Suffix File Output |
|------|-------------------|
| Pembersihan domain | `_bersih_domain.txt` |
| Pembersihan URL | `_bersih.txt` |
| Perbandingan domain | `_domain_baru.txt` |
| Perbandingan URL | `_url_baru.txt` |

**Contoh:**
- Input: `backlinks.txt` → Output: `backlinks_bersih_domain.txt`
- Input: `baru.txt` dengan `--compare` → Output: `baru_domain_baru.txt`

## Perbedaan Mode Domain vs URL

### Mode Domain
- **Tujuan**: Diversifikasi domain
- **Logika**: Satu URL per domain
- **Hasil**: Lebih sedikit URL, fokus pada domain unik
- **Use case**: Mencari website/domain baru untuk backlink

### Mode URL
- **Tujuan**: Mencari halaman/konten baru
- **Logika**: Setiap URL unik disimpan
- **Hasil**: Lebih banyak URL, termasuk halaman berbeda dari domain sama
- **Use case**: Mencari artikel/halaman baru untuk guest post

## 🔧 Troubleshooting

### Error "File tidak ditemukan"
```bash
Error: File 'namafile.txt' tidak ditemukan!
```
**Solusi**: Pastikan file ada di direktori yang sama atau gunakan path lengkap.

### URL tidak valid
Script akan otomatis melewati URL yang tidak valid dan melaporkannya di statistik akhir.

### Encoding error
Pastikan file input menggunakan encoding UTF-8.

## Kontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -am 'Tambah fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## Author

**Dzbackdor** - [GitHub](https://github.com/Dzbackdor)

## Changelog

### v1.0.0
- ✅ Fitur pembersihan duplikat URL
- ✅ Fitur perbandingan dua file
- ✅ Mode domain dan URL
- ✅ Normalisasi URL otomatis
- ✅ Statistik detail
---

**Made with ❤️ by Dzone**
