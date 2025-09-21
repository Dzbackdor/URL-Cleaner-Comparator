#!/usr/bin/env python3
"""
Script untuk:
1) Membersihkan duplikat dari file backlinks (mode 'url' atau 'domain')
2) Membandingkan dua file: append URL baru dari file baru ke akhir file lama
   - Urutan lama tetap
   - URL baru ditambahkan berurutan sesuai kemunculan di file baru
   - SEMUA URL di-output-kan berakhir dengan '/'
"""

import argparse
import os
from urllib.parse import urlparse, urlunparse
from collections import OrderedDict
from colorama import Fore, init

# Initialize Colorama
init(autoreset=True)

# Colors for terminal text
B = Fore.BLUE
W = Fore.WHITE
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW

def clear_terminal():
    """Membersihkan terminal untuk semua OS (Windows, Linux, macOS)"""
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
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

def normalize_url(url):
    """
    Normalisasi URL untuk perbandingan & output konsisten:
    - Tambah scheme bila hilang (http)
    - Lowercase host
    - Hilangkan query/fragment
    - PASTIKAN path berakhir dengan '/'
    """
    if not isinstance(url, str):
        return None
    url = url.strip()
    if not url:
        return None
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    try:
        p = urlparse(url)
        # host lowercase
        netloc = (p.netloc or '').lower()
        # path: pastikan selalu diakhiri '/'
        path = p.path or '/'
        if not path.endswith('/'):
            path = path + '/'
        clean_url = urlunparse((
            (p.scheme or 'http').lower(),
            netloc,
            path,
            '',  # params
            '',  # query
            ''   # fragment
        ))
        return clean_url
    except Exception as e:
        print(f"Error normalisasi URL '{url}': {e}")
        return None

def extract_domain(url):
    """Ekstrak domain bersih dari URL (tanpa 'www.') untuk mode domain"""
    try:
        parsed = urlparse(url.lower())
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return None

def load_urls_from_file(file_path):
    """Muat dan normalisasi URL dari file (set unik)"""
    urls = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url:
                    normalized = normalize_url(url)
                    if normalized:
                        urls.add(normalized)
        return urls
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan!")
        return set()
    except Exception as e:
        print(f"Error membaca file '{file_path}': {e}")
        return set()

def compare_files(new_file, old_file, output_file=None, compare_mode='domain'):
    """
    Bandingkan dua file dan append entri baru (urut sesuai kemunculan di new_file) ke bawah isi lama.
    Output SELALU berakhir dengan '/'.
    Args:
        new_file: path ke file baru (baru.txt)
        old_file: path ke file lama (lama.txt)
        output_file: jika None => overwrite lama.txt; jika diisi => tulis ke file ini
        compare_mode: 'url' (exact) atau 'domain' (default, unik per domain)
    """
    print(f"{W}Membandingkan file:")
    print(f"{W}  File baru : {G}{new_file}")
    print(f"{W}  File lama : {Y}{old_file}")
    print(f"{W}  Mode      : {G}{'Domain (default)' if compare_mode=='domain' else 'URL penuh'}")

    # 1) Baca isi lama (preserve urutan), lalu siapkan versi dinormalisasi (untuk output & perbandingan)
    try:
        with open(old_file, 'r', encoding='utf-8') as f:
            old_lines_raw = [line.rstrip('\n') for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{R}Error{W}: File lama '{old_file}' tidak ditemukan!")
        return
    except Exception as e:
        print(f"{R}Error{W} membaca file lama: {e}")
        return

    print(f"{W}Berhasil memuat {G}{len(old_lines_raw)}{W} baris dari file lama (urutan dipertahankan)")

    normalized_old_lines = []
    comparison_set = set()
    invalid_old = 0

    for s in old_lines_raw:
        norm = normalize_url(s)
        if norm:
            normalized_old_lines.append(norm)
            key = extract_domain(norm) if compare_mode == 'domain' else norm
            if key:
                comparison_set.add(key)
        else:
            # Jika tidak bisa dinormalisasi, tetap tulis apa adanya + tambahkan '/' jika belum ada
            out = s if s.endswith('/') else (s + '/')
            normalized_old_lines.append(out)

    if compare_mode == 'domain':
        print(f"{W}Domain unik awal (dari lama): {G}{len(comparison_set)}")
    else:
        print(f"{W}URL unik awal (dari lama): {G}{len(comparison_set)}")
    if invalid_old:
        print(f"{W}Baris lama tidak valid terabaikan: {R}{invalid_old}")

    # 3) Scan new_file dan siapkan daftar tambahan berurutan (sudah normalized => pasti trailing '/')
    new_items_to_append = []
    duplicate_count = 0
    invalid_new = 0
    total_new_nonempty = 0

    print(f"\n{W}Memproses file baru dan mencari entri yang BELUM ada di lama...")
    try:
        with open(new_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                s = line.strip()
                if not s:
                    continue
                total_new_nonempty += 1
                norm = normalize_url(s)
                if not norm:
                    invalid_new += 1
                    print(f"{W}URL tidak valid ({R}baris {line_num}{W}): {R}{s}")
                    continue

                key = extract_domain(norm) if compare_mode == 'domain' else norm
                if not key:
                    invalid_new += 1
                    print(f"{W}Gagal ekstrak key ({R}baris {line_num}{W}): {R}{s}")
                    continue

                if key in comparison_set:
                    duplicate_count += 1
                    if compare_mode == 'domain':
                        print(f"{W}Sudah ada domain ({R}baris {line_num}{W}): {Y}{key} {W}=❯ {R}{norm}")
                    else:
                        print(f"{W}Sudah ada URL ({R}baris {line_num}{W}): {R}{norm}")
                else:
                    new_items_to_append.append(norm)   # sudah berakhir '/'
                    comparison_set.add(key)
                    if compare_mode == 'domain':
                        print(f"{W}Domain baru: {G}{key} {W}=❯ {Y}{norm}")
                    else:
                        print(f"{W}URL baru: {Y}{norm}")
    except FileNotFoundError:
        print(f"{R}Error{W}: File baru '{new_file}' tidak ditemukan!")
        return
    except Exception as e:
        print(f"{R}Error{W} membaca file baru: {e}")
        return

    # 4) Tulis hasil
    target_path = output_file if output_file else old_file
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            if normalized_old_lines:
                f.write('\n'.join(normalized_old_lines))
                f.write('\n')
            if new_items_to_append:
                f.write('\n'.join(new_items_to_append))
                f.write('\n')

        print(f"\n{Y}" + "═" * 50)
        print(f"{G}PERBANDINGAN & APPEND SELESAI!")
        print(f"{Y}" + "═" * 50)
        print(f"{W}Baris non-kosong di file baru    : {G}{total_new_nonempty}")
        print(f"{W}Tambahan baru yang di-append     : {G}{len(new_items_to_append)}")
        print(f"{W}Sudah ada sebelumnya             : {R}{duplicate_count}")
        print(f"{W}Tidak valid diabaikan            : {R}{invalid_new}")
        print(f"{W}Hasil gabungan ditulis ke        : {G}{target_path}")

        if new_items_to_append:
            max_show = min(10, len(new_items_to_append))
            print(f"\n{G}{max_show}{W} tambahan pertama:")
            for i, u in enumerate(new_items_to_append[:max_show], 1):
                if compare_mode == 'domain':
                    print(f"{i:2d}. {G}{extract_domain(u)} {W}=❯ {Y}{u}")
                else:
                    print(f"{i:2d}. {Y}{u}")
            if len(new_items_to_append) > max_show:
                print(f"{W}    ... dan {G}{len(new_items_to_append) - max_show}{W} lainnya")
        else:
            print(f"\n{W}Tidak ada entri baru untuk ditambahkan.")
    except Exception as e:
        print(f"{R}Error{W} menulis hasil: {e}")

def clean_duplicates(input_file, output_file=None, mode='domain'):
    """Hapus duplikat dari file backlinks; output SELALU trailing '/'."""
    if output_file is None:
        suffix = '_bersih_domain.txt' if mode == 'domain' else '_bersih.txt'
        output_file = input_file.replace('.txt', suffix)

    print(f"{W}Membaca URL dari: {G}{input_file}")
    print(f"{W}Mode: {G}{'Satu URL per domain' if mode == 'domain' else 'Hapus duplikat URL exact'}")

    if mode == 'domain':
        domain_urls = OrderedDict()
        duplicates_count = 0
        invalid_count = 0
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    url = line.strip()
                    if not url:
                        continue
                    normalized = normalize_url(url)
                    if normalized:
                        domain = extract_domain(normalized)
                        if domain:
                            if domain in domain_urls:
                                duplicates_count += 1
                                print(f"{G}" + "═" * 50)
                                print(f"{W}Duplikat domain ditemukan ({R}baris {line_num}{W}): {R}{url}")
                                print(f"  {G}=❯  {W}Tetap gunakan: {Y}{domain_urls[domain]}")
                                print(f"  {R}=❯  {W}Lewati: {R}{normalized}")
                            else:
                                domain_urls[domain] = normalized
                                print(f"{W}Tambahkan domain {G}{domain}{W}: {Y}{normalized}")
                        else:
                            invalid_count += 1
                            print(f"Domain tidak valid (baris {line_num}): {url}")
                    else:
                        invalid_count += 1
                        print(f"URL tidak valid (baris {line_num}): {url}")
        except FileNotFoundError:
            print(f"{R}Error{W}: File {G}{input_file} {R}tidak ditemukan!")
            return
        except Exception as e:
            print(f"Error membaca file: {e}")
            return
        unique_urls = list(domain_urls.values())
    else:
        unique_urls_dict = OrderedDict()
        duplicates_count = 0
        invalid_count = 0
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    url = line.strip()
                    if not url:
                        continue
                    normalized = normalize_url(url)
                    if normalized:
                        if normalized in unique_urls_dict:
                            duplicates_count += 1
                            print(f"Duplikat URL ditemukan (baris {line_num}): {url}")
                        else:
                            unique_urls_dict[normalized] = None
                    else:
                        invalid_count += 1
                        print(f"URL tidak valid (baris {line_num}): {url}")
        except FileNotFoundError:
            print(f"Error: File '{input_file}' tidak ditemukan!")
            return
        except Exception as e:
            print(f"Error membaca file: {e}")
            return
        unique_urls = list(unique_urls_dict.keys())

    # Simpan hasil yang sudah dibersihkan (sudah trailing '/')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_urls))
        print(f"\n{Y}" + "═" * 50)
        print(f"{G}PEMBERSIHAN SELESAI!")
        print(f"{Y}" + "═" * 50)
        if mode == 'domain':
            print(f"{W}URL asli:{G} {len(unique_urls) + duplicates_count + invalid_count}")
            print(f"{W}Domain unik:{G} {len(unique_urls)}")
            print(f"{W}Duplikat domain dihapus:{R} {duplicates_count}")
            print(f"{W}URL tidak valid dihapus:{R} {invalid_count}")
        else:
            print(f"{W}URL asli: {len(unique_urls) + duplicates_count + invalid_count}")
            print(f"{W}URL unik: {len(unique_urls)}")
            print(f"{W}Duplikat URL dihapus: {duplicates_count}")
            print(f"{W}URL tidak valid dihapus: {invalid_count}")
        print(f"{W}File bersih disimpan ke:{G} {output_file}")

        # Statistik domain (opsional)
        domain_count = {}
        for url in unique_urls:
            domain = extract_domain(url)
            if domain:
                domain_count[domain] = domain_count.get(domain, 0) + 1
        print(f"{W}Total domain unik: {G}{len(domain_count)}")
        print(f"{Y}" + "═" * 50)

        if mode == 'domain':
            print(f"{W}\nDomain dan URL yang dipilih:")
            for i, url in enumerate(unique_urls[:10], 1):
                domain = extract_domain(url)
                print(f"{i:2d}. {G}{domain} {W}=❯ {Y}{url}")
            if len(unique_urls) > 10:
                print(f"{W}    ... dan {G}{len(unique_urls) - 10} {W}domain lainnya")
        else:
            print(f"\nDomain dengan multiple URL:")
            multiple_domains = [(domain, count) for domain, count in domain_count.items() if count > 1]
            if multiple_domains:
                for domain, count in sorted(multiple_domains, key=lambda x: x[1], reverse=True)[:10]:
                    print(f"  {domain}: {count} URL")
            else:
                print("  Tidak ada - semua domain hanya memiliki 1 URL")
    except Exception as e:
        print(f"Error menyimpan file bersih: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Bersihkan duplikat atau bandingkan dua file (append URL baru ke file lama). Semua URL di-output berakhir dengan "/".'
    )
    parser.add_argument('input_file',
                        help='File input backlinks (pada --compare berfungsi sebagai file baru)')
    parser.add_argument('--output',
                        help='File output. Pada --compare: jika tidak diisi, overwrite file lama (in-place).')
    parser.add_argument('--mode', choices=['url', 'domain'], default='domain',
                        help='Mode pembersihan: "url" atau "domain" (default: domain)')
    parser.add_argument('--compare', metavar='FILE_LAMA',
                        help='Bandingkan input_file (baru) dengan FILE_LAMA, lalu append entri baru ke bawah.')
    parser.add_argument('--compare-mode', choices=['url', 'domain'], default='domain',
                        help='Mode perbandingan saat --compare (default: domain)')
    args = parser.parse_args()

    if args.compare:
        compare_files(args.input_file, args.compare, args.output, args.compare_mode)
    else:
        clean_duplicates(args.input_file, args.output, args.mode)

if __name__ == "__main__":
    clear_terminal()
    banner()
    main()
