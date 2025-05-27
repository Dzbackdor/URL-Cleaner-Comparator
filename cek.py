#!/usr/bin/env python3
"""
Script untuk membersihkan duplikat dari file backlinks yang sudah ada
Hanya menyimpan 1 URL per domain
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
    """
    Membersihkan terminal untuk semua OS (Windows, Linux, macOS)
    """
    try:
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # Linux/macOS
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
    """Normalisasi URL untuk mencegah duplikat"""
    if not isinstance(url, str):
        return None
        
    url = url.strip()
    if not url:
        return None
        
    # Tambahkan protokol jika tidak ada
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    try:
        parsed = urlparse(url.lower())
        clean_url = urlunparse((
            parsed.scheme or 'http',
            parsed.netloc,
            parsed.path.rstrip('/'),
            '', '', ''
        ))
        return clean_url
    except Exception as e:
        print(f"Error normalisasi URL '{url}': {e}")
        return None

def extract_domain(url):
    """Ekstrak domain bersih dari URL"""
    try:
        parsed = urlparse(url.lower())
        domain = parsed.netloc
        
        # Hapus prefix www untuk perbandingan domain
        if domain.startswith('www.'):
            domain = domain[4:]
            
        return domain
    except:
        return None

def load_urls_from_file(file_path):
    """Muat dan normalisasi URL dari file"""
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

def compare_files(new_file, old_file, output_file=None, compare_mode='url'):
    """Bandingkan dua file dan ekstrak URL yang ada di new_file tapi tidak di old_file
    
    Args:
        new_file: Path ke file baru (baru.txt)
        old_file: Path ke file lama (lama.txt)
        output_file: Path file output
        compare_mode: 'url' untuk perbandingan URL exact, 'domain' untuk perbandingan berbasis domain
    """
    if output_file is None:
        suffix = '_domain_baru.txt' if compare_mode == 'domain' else '_url_baru.txt'
        output_file = new_file.replace('.txt', suffix)
    
    print(f"{W}Membandingkan file:")
    print(f"{W}File baru: {G}{new_file}")
    print(f"{W}File lama: {Y}{old_file}")
    print(f"{W}Mode: {G}{'Perbandingan berbasis domain' if compare_mode == 'domain' else 'Perbandingan berbasis URL'}")
    
    # Muat URL dari file lama
    print(f"\n{W}Memuat URL dari file lama...")
    old_urls = load_urls_from_file(old_file)
    if not old_urls:
        print(f"{R}Tidak ada URL valid ditemukan di file lama!")
        return
    
    print(f"{W}Berhasil memuat {G}{len(old_urls)} URL {W}dari file lama")
    
    # Buat set perbandingan berdasarkan mode
    if compare_mode == 'domain':
        # Ekstrak domain dari URL lama
        old_domains = set()
        for url in old_urls:
            domain = extract_domain(url)
            if domain:
                old_domains.add(domain)
        print(f"{W}Ditemukan {G}{len(old_domains)} {W}domain unik di file lama")
        comparison_set = old_domains
    else:
        comparison_set = old_urls
    
    # Proses file baru dan temukan URL/domain unik
    new_items = []
    duplicate_count = 0
    invalid_count = 0
    total_lines = 0  # Tambahkan counter untuk total baris
    
    print(f"\n{W}Memproses file baru...")
    try:
        with open(new_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                url = line.strip()
                if not url:
                    continue
                    
                total_lines += 1  # Hitung setiap baris yang tidak kosong
                normalized = normalize_url(url)
                if normalized:
                    if compare_mode == 'domain':
                        domain = extract_domain(normalized)
                        if domain:
                            if domain in comparison_set:
                                duplicate_count += 1
                                print(f"{W}Domain sudah ada ({R}baris {line_num}){W}: {Y}{domain} {W}=❯ {R}{normalized}")
                            else:
                                new_items.append(normalized)
                                comparison_set.add(domain)  # Tambahkan untuk mencegah duplikat dalam file baru
                                print(f"{W}Domain baru ditemukan: {G}{domain} {W}=❯ {Y}{normalized}")
                        else:
                            invalid_count += 1
                            print(f"{W}Domain tidak valid ({R}baris {line_num}){W}: {R}{url}")
                    else:
                        if normalized in comparison_set:
                            duplicate_count += 1
                            print(f"{W}URL sudah ada ({R}baris {line_num}{W}): {R}{normalized}")
                        else:
                            new_items.append(normalized)
                            comparison_set.add(normalized)  # Tambahkan untuk mencegah duplikat dalam file baru
                            print(f"{W}URL baru ditemukan: {Y}{normalized}")
                else:
                    invalid_count += 1
                    print(f"{W}URL tidak valid ({R}baris {line_num}{W}): {R}{url}")
    
    except FileNotFoundError:
        print(f"{W}Error: File {R}{new_file} {W}tidak ditemukan!")
        return
    except Exception as e:
        print(f"{W}Error membaca file baru: {R}{e}")
        return
    
    # Simpan hasil
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_items))
        
        print(f"\n{Y}" + "═" * 50)
        print(f"{G}PERBANDINGAN SELESAI!")
        print(f"{Y}═" * 50)
        
        print(f"{W}URL diproses dari file baru: {G}{total_lines}")
        print(f"{W}{'Domain' if compare_mode == 'domain' else 'URL'} baru ditemukan:{G} {len(new_items)}")
        print(f"{W}Sudah ada sebelumnya: {R}{duplicate_count}")
        print(f"{W}URL tidak valid: {R}{invalid_count}")
        print(f"{W}Hasil disimpan ke: {G}{output_file}")
        
        if new_items:
            # Perbaiki logika tampilan
            max_show = min(10, len(new_items))  # Tampilkan maksimal 10 atau sesuai jumlah yang ada
            print(f"\n{G}{max_show} {W}{'domain' if compare_mode == 'domain' else 'URL'} baru{'pertama' if len(new_items) > max_show else ''}:")
            for i, url in enumerate(new_items[:max_show], 1):
                if compare_mode == 'domain':
                    domain = extract_domain(url)
                    print(f"{i:2d}. {G}{domain} {W}=❯ {Y}{url}")
                else:
                    print(f"{i:2d}. {Y}{url}")
            
            if len(new_items) > 10:
                print(f"{W}    ... dan {G}{len(new_items) - 10} {W}lainnya")
        else:
            print(f"\nTidak ada {'domain' if compare_mode == 'domain' else 'URL'} baru ditemukan!")
        
        # Tambahkan verifikasi
        # print(f"\nVerifikasi: {len(new_items)} + {duplicate_count} + {invalid_count} = {len(new_items) + duplicate_count + invalid_count} (harus sama dengan {total_lines})")
        
    except Exception as e:
        print(f"Error menyimpan file hasil: {e}")

def clean_duplicates(input_file, output_file=None, mode='url'):
    """Hapus duplikat dari file backlinks
    
    Args:
        input_file: Path file input
        output_file: Path file output
        mode: 'url' untuk duplikat URL exact, 'domain' untuk satu URL per domain
    """
    if output_file is None:
        suffix = '_bersih_domain.txt' if mode == 'domain' else '_bersih.txt'
        output_file = input_file.replace('.txt', suffix)
    
    print(f"{W}Membaca URL dari: {G}{input_file}")
    print(f"{W}Mode: {G}{'Satu URL per domain' if mode == 'domain' else 'Hapus duplikat URL exact'}")
    
    if mode == 'domain':
        # Gunakan dict untuk menyimpan URL pertama untuk setiap domain
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
        
        # Simpan hasil
        unique_urls = list(domain_urls.values())
        
    else:
        # Deduplikasi berbasis URL original
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
    
    # Simpan hasil yang sudah dibersihkan
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_urls))
        
        print(f"\n{Y}" + "═" * 50)
        print(f"{G}PEMBERSIHAN SELESAI!")
        print(f"{Y}═" * 50)
        
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
        
        # Tampilkan statistik domain
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
    parser = argparse.ArgumentParser(description='Bersihkan duplikat dari file backlinks atau bandingkan dua file')
    parser.add_argument('input_file', help='File input dengan backlinks (atau file baru saat menggunakan --compare)')
    parser.add_argument('--output', help='File output (default: otomatis dibuat)')
    parser.add_argument('--mode', choices=['url', 'domain'], default='domain',
                       help='Mode pembersihan: "url" untuk duplikat URL exact, "domain" untuk satu URL per domain (default: domain)')
    parser.add_argument('--compare', metavar='FILE_LAMA', 
                       help='Bandingkan input_file (baru) dengan FILE_LAMA dan output URL yang baru')
    parser.add_argument('--compare-mode', choices=['url', 'domain'], default='domain',
                       help='Mode perbandingan saat menggunakan --compare: "url" untuk perbandingan URL exact, "domain" untuk perbandingan domain (default: domain)')
    
    args = parser.parse_args()
    
    if args.compare:
        # Mode perbandingan: input_file adalah file baru, args.compare adalah file lama
        compare_files(args.input_file, args.compare, args.output, args.compare_mode)
    else:
        # Mode pembersihan original
        clean_duplicates(args.input_file, args.output, args.mode)

if __name__ == "__main__":
    clear_terminal()
    banner()
    main()
