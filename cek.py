import argparse
import os
import re
from urllib.parse import urlparse, urlunparse
from collections import OrderedDict
from colorama import Fore, init
from textwrap import dedent

# Initialize Colorama
init(autoreset=True)

# Colors
B = Fore.BLUE
W = Fore.WHITE
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW

HOST_CHARS_RE = re.compile(r'^[a-z0-9.-]+$')  # izinkan subdomain numerik
HAS_ALNUM = re.compile(r'[a-z0-9]')

def clear_terminal():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"{R}Gagal membersihkan terminal: {e}{W}")

def banner():
    print(rf"""{Y}
                                                __                
  ____  ____   _____ ___________ ____________ _/  |_  ___________ 
_/ ___\/  _ \ /     \\____ \__  \\_  __ \__  \\   __\/  _ \_  __ \
\  \__(  <_> )  Y Y  \  |_> > __ \|  | \// __ \|  | (  <_> )  | \/
 \___  >____/|__|_|  /   __(____  /__|  (____  /__|  \____/|__|   
     \/            \/|__|       \/           \/{W}Backlink Url Cleaner                    
{R}═══════════════════════════════════════════════════════════════════""")

# ---------------- Normalizers ---------------- #

def _valid_netloc(netloc: str) -> bool:
    # netloc harus ada, mengandung setidaknya 1 alnum, dan punya titik (untuk domain publik biasa)
    if not netloc:
        return False
    n = netloc.lower()
    if ':' in n:  # buang port utk cek
        n = n.split(':', 1)[0]
    return '.' in n and bool(HAS_ALNUM.search(n))

def normalize_url(s: str, add_slash: bool = False):
    """
    Normalisasi URL (untuk mode url/domain):
      - Tambah scheme 'http' bila hilang
      - Lowercase host
      - Buang query/fragment
      - TIDAK menghapus 'www.'
      - Menolak URL tanpa host (mis. 'http:///')
      - Tambahkan '/' di akhir path jika add_slash=True
    """
    if not isinstance(s, str):
        return None
    s = s.strip()
    if not s:
        return None
    if not s.startswith(('http://', 'https://')):
        s = 'http://' + s
    try:
        p = urlparse(s)
        netloc = (p.netloc or '').lower()
        if not _valid_netloc(netloc):
            return None
        path = p.path or '/'
        if add_slash and not path.endswith('/'):
            path += '/'
        return urlunparse(((p.scheme or 'http').lower(), netloc, path, '', '', ''))
    except Exception:
        return None

def normalize_host(s: str):
    """
    Normalisasi host (untuk mode host / list domain):
      - Jika input berupa URL → ekstrak host-nya (pakai normalize_url)
      - Lowercase, buang port (jika ada)
      - TIDAK menghapus 'www.'
      - Menolak yang tanpa titik/aneh
    """
    if not isinstance(s, str):
        return None
    s = s.strip()
    if not s:
        return None

    # Jika terlihat seperti URL, ekstrak host via normalize_url → urlparse
    if '://' in s or '/' in s:
        u = normalize_url(s, add_slash=False)  # Jangan tambah slash untuk host
        if not u:
            return None
        host = urlparse(u).netloc
    else:
        host = s.lower()
        # buang port bila ada
        if ':' in host:
            host = host.split(':', 1)[0]
        # validasi host
        if not _valid_netloc(host):
            return None

    return host

# ---------------- Core Ops ---------------- #

def extract_domain_from_url(u: str):
    """Ambil domain dari URL normalized (mempertahankan 'www.' jika ada)."""
    try:
        netloc = urlparse(u).netloc.lower()
        return netloc if _valid_netloc(netloc) else None
    except Exception:
        return None

def compare_files(new_file, old_file, output_file, mode='domain', merge_old=False, add_slash=False):
    """
    Perbandingan:
      - Default: OUTPUT hanya ENTRI BARU (unik per mode) dari file baru.
      - merge_old=True: gabung isi lama + append entri baru.
    """
    print(f"{W}Membandingkan file:")
    print(f"{W}  File baru : {G}{new_file}")
    print(f"{W}  File lama : {Y}{old_file}")
    label = {'url': 'URL penuh', 'domain': 'Domain (URL output)', 'host': 'Host/Subdomain (list domain)'}[mode]
    print(f"{W}  Mode      : {G}{label}")
    print(f"{W}  Slash     : {G}{'Ya' if add_slash else 'Tidak'}")
    print(f"{W}  Output    : {G}{'Hanya entri BARU' if not merge_old else 'Gabung lama + append baru'}")

    # Baca lama
    try:
        with open(old_file, 'r', encoding='utf-8') as f:
            old_raw = [ln.rstrip('\n') for ln in f if ln.strip()]
    except FileNotFoundError:
        print(f"{R}Error{W}: File lama '{old_file}' tidak ditemukan!")
        return
    except Exception as e:
        print(f"{R}Error{W} membaca file lama: {e}")
        return

    print(f"{W}Berhasil memuat {G}{len(old_raw)}{W} baris dari file lama (urutan dipertahankan)")

    normalized_old_lines = []
    keys_seen = set()

    def normalize_for_mode(s):
        if mode == 'host':
            return normalize_host(s)
        else:
            return normalize_url(s, add_slash=add_slash)

    def key_for(value):
        if value is None:
            return None
        if mode == 'url':
            return value                       # URL normalized (unik per URL)
        if mode == 'domain':
            return extract_domain_from_url(value)  # netloc (www dipertahankan)
        if mode == 'host':
            return value                       # host normalized
        return None

    # Normalisasi isi lama & kumpulkan key
    for s in old_raw:
        n = normalize_for_mode(s)
        if n is None:
            # skip total jika tidak valid (jangan ikut kunci)
            continue
        k = key_for(n)
        if k:
            keys_seen.add(k)
        if merge_old:
            # hanya tulis lama jika mode gabungan
            normalized_old_lines.append(n)

    print(f"{W}Unik awal (berdasar mode): {G}{len(keys_seen)}")

    # Proses baru
    new_items = []
    dup = inv = total = 0
    print(f"\n{W}Memproses file baru dan mencari entri yang BELUM ada di lama...")
    try:
        with open(new_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                s = line.strip()
                if not s:
                    continue
                total += 1
                n = normalize_for_mode(s)
                if not n:
                    inv += 1
                    print(f"{W}Baris tidak valid ({R}{i}{W}): {R}{s}")
                    continue
                k = key_for(n)
                if not k:
                    inv += 1
                    print(f"{W}Gagal ambil key ({R}{i}{W}): {R}{s}")
                    continue
                if k in keys_seen:
                    dup += 1
                    what = 'host' if mode == 'host' else ('domain' if mode == 'domain' else 'URL')
                    print(f"{W}Sudah ada {what} ({R}baris {i}{W}): {Y}{k}")
                else:
                    keys_seen.add(k)
                    new_items.append(n)
                    if mode == 'host':
                        print(f"{W}Host baru: {G}{k}")
                    elif mode == 'domain':
                        print(f"{W}Domain baru: {G}{k} {W}=❯ {Y}{n}")
                    else:
                        print(f"{W}URL baru: {Y}{n}")
    except FileNotFoundError:
        print(f"{R}Error{W}: File baru '{new_file}' tidak ditemukan!")
        return
    except Exception as e:
        print(f"{R}Error{W} membaca file baru: {e}")
        return

    # Tulis hasil
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            if merge_old and normalized_old_lines:
                f.write('\n'.join(normalized_old_lines) + '\n')
            if new_items:
                f.write('\n'.join(new_items) + '\n')
        print(f"\n{Y}" + "═" * 50)
        print(f"{G}COMPARE SELESAI!")
        print(f"{Y}" + "═" * 50)
        print(f"{W}Baris non-kosong di file baru    : {G}{total}")
        print(f"{W}Tambahan BARU yang ditulis       : {G}{len(new_items)}")
        print(f"{W}Sudah ada sebelumnya             : {R}{dup}")
        print(f"{W}Tidak valid diabaikan            : {R}{inv}")
        print(f"{W}Output                           : {G}{output_file}")

        if not new_items:
            print(f"\n{W}Tidak ada entri baru.")
        else:
            preview = new_items[:10]
            print(f"\n{G}{len(preview)}{W} contoh pertama:")
            for idx, val in enumerate(preview, 1):
                if mode == 'domain':
                    print(f"{idx:2d}. {G}{extract_domain_from_url(val)} {W}=❯ {Y}{val}")
                else:
                    print(f"{idx:2d}. {Y}{val}")
            if len(new_items) > len(preview):
                print(f"{W}    ... dan {G}{len(new_items) - len(preview)}{W} lainnya")
    except Exception as e:
        print(f"{R}Error{W} menulis hasil: {e}")

def clean_duplicates(input_file, output_file, mode='domain', add_slash=False):
    """Hapus duplikat sesuai mode; output konsisten."""
    print(f"{W}Membaca dari: {G}{input_file}")
    label = {'url': 'Hapus duplikat URL exact', 'domain': 'Satu URL per domain', 'host': 'Satu baris per host/subdomain'}[mode]
    print(f"{W}Mode: {G}{label} (www dipertahankan)")
    print(f"{W}Slash di akhir path: {G}{'Ya' if add_slash else 'Tidak'}")

    def normalize_for_mode(s):
        if mode == 'host':
            return normalize_host(s)
        else:
            return normalize_url(s, add_slash=add_slash)
    
    key_fn = (lambda v: v) if mode in ('url', 'host') else extract_domain_from_url

    store = OrderedDict()
    dup = inv = total = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                s = line.strip()
                if not s:
                    continue
                total += 1
                n = normalize_for_mode(s)
                if not n:
                    inv += 1
                    print(f"{W}Baris tidak valid ({R}{line_num}{W}): {R}{s}")
                    continue
                k = key_fn(n)
                if not k:
                    inv += 1
                    print(f"{W}Gagal ambil key ({R}{line_num}{W}): {R}{s}")
                    continue
                if k in store:
                    dup += 1
                    print(f"{W}Duplikat ({R}{line_num}{W}): {Y}{s}")
                else:
                    store[k] = n
                    if mode == 'domain':
                        print(f"{W}Tambahkan domain {G}{k}{W}: {Y}{n}")
                    else:
                        print(f"{W}Tambah: {Y}{n}")
    except FileNotFoundError:
        print(f"{R}Error{W}: File {G}{input_file}{W} tidak ditemukan!")
        return
    except Exception as e:
        print(f"{R}Error{W} membaca file: {e}")
        return

    unique_lines = list(store.values())

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_lines))
        print(f"\n{Y}" + "═" * 50)
        print(f"{G}PEMBERSIHAN SELESAI!")
        print(f"{Y}" + "═" * 50)
        print(f"{W}Baris asli: {G}{total}")
        print(f"{W}Unik ({mode}) : {G}{len(unique_lines)}")
        print(f"{W}Duplikat dihapus: {R}{dup}")
        print(f"{W}Baris tidak valid: {R}{inv}")
        print(f"{W}File bersih disimpan ke: {G}{output_file}")
    except Exception as e:
        print(f"{R}Error{W} menyimpan file bersih: {e}")

# ---------------- CLI ---------------- #
def build_parser():
    # Formatter gabungan: raw text (respect newline) + tampilkan default;
    # atur lebar & posisi kolom supaya tidak mudah terbungkus.
    class NeatFormatter(argparse.ArgumentDefaultsHelpFormatter,
                        argparse.RawTextHelpFormatter):
        pass

    epi = (
        "Contoh:\n"
        "  Hanya entri domain baru:  python3 new.py -l baru.txt -c lama.txt -m domain -o tt.txt\n"
        "  Gabung lama + append baru: python3 new.py -l baru.txt -c lama.txt -m domain -o tt.txt --merge-old"
    )

    parser = argparse.ArgumentParser(
        # description=desc,
        epilog=epi,
        formatter_class=lambda prog: NeatFormatter(prog, width=120, max_help_position=28)
    )

    parser.add_argument(
        '-l', '--list', dest='input_file', required=True, metavar='INPUT_FILE',
        help='File input (pada -c berfungsi sebagai file BARU).'
    )
    parser.add_argument(
        '-o', '--output', dest='output', required=True, metavar='OUTPUT',
        help='File output hasil (WAJIB).'
    )
    parser.add_argument(
        '-m', '--mode', dest='mode', choices=['url', 'domain', 'host'], default='domain',
        help="Mode proses: {url,domain,host}; 'host' untuk list domain (tanpa '/')."
    )
    parser.add_argument(
        '-s', '--slash', dest='add_slash', action='store_true',
        help='Tambahkan "/" di akhir setiap path URL (untuk mode url/domain).'
    )
    parser.add_argument(
        '-c', '--compare', dest='compare', metavar='FILE_LAMA',
        help='Aktifkan perbandingan: bandingkan -l (baru) dengan FILE_LAMA (lama).'
    )
    parser.add_argument(
        '--merge-old', dest='merge_old', action='store_true',
        help='Gabungkan isi lama + append entri baru (default: hanya entri baru).'
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.compare:
        compare_files(args.input_file, args.compare, args.output, args.mode, args.merge_old, args.add_slash)
    else:
        clean_duplicates(args.input_file, args.output, args.mode, args.add_slash)

if __name__ == '__main__':
    clear_terminal()
    banner()
    main()
