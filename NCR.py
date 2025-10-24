#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NCR NIK-CHECKER Ultimate Edition (Python CLI)
by Ruiix_.volt

- Re-uploading is strictly prohibited
"""

import os, re, sys, time
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ---------- Tampilan ---------- #

def banner():
    print(Fore.CYAN + "-" * 40)
    print(Fore.YELLOW + "🔍 NCR NIK-CHECKER")
    print(Fore.YELLOW + "ONLY CHECKER!!")
    print(Fore.CYAN + "-" * 40)
    print(Fore.BLUE + "IG:ruiix_.volt")
    print(Fore.LIGHTBLACK_EX + "// UNTUK NIK CARI SENDIRI \\\\")

def loading(teks="Mengecek data", durasi=2.5):
    anim = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    t0 = time.time()
    i = 0
    while time.time() - t0 < durasi:
        sys.stdout.write(Fore.CYAN + f"\r[{anim[i % len(anim)]}] {teks}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")

# ---------- Fungsi Waktu ---------- #

def zodiak(day, month):
    zodiaks = [
        ("Capricorn", (12, 22), (1, 19)), ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)), ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)), ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)), ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)), ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)), ("Sagitarius", (11, 22), (12, 21))
    ]
    for nama, awal, akhir in zodiaks:
        if (month == awal[0] and day >= awal[1]) or (month == akhir[0] and day <= akhir[1]):
            return nama
    return "Capricorn"

def pasaran_jawa(tanggal):
    pasaran = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]
    base = datetime(1900, 1, 1)
    delta = (tanggal - base).days
    return f"{hari[tanggal.weekday()]} {pasaran[delta % 5]}"

def hitung_usia(tgl_lahir):
    now = datetime.now()
    tahun = now.year - tgl_lahir.year - ((now.month, now.day) < (tgl_lahir.month, tgl_lahir.day))
    bulan = (now.month - tgl_lahir.month) % 12
    hari = (now - tgl_lahir.replace(year=now.year if now >= tgl_lahir.replace(year=now.year) else now.year-1)).days
    return f"{tahun} Tahun {bulan} Bulan {hari} Hari"

def ultah_berikutnya(tgl_lahir):
    now = datetime.now()
    next_bday = datetime(now.year, tgl_lahir.month, tgl_lahir.day)
    if next_bday < now:
        next_bday = datetime(now.year + 1, tgl_lahir.month, tgl_lahir.day)
    selisih = next_bday - now
    bulan = selisih.days // 30
    hari = selisih.days % 30
    return f"{bulan} Bulan {hari} Hari Lagi"

# ---------- Parsing ncr.min.js ---------- #

def parse_ncr_js():
    path = os.path.join(os.path.dirname(__file__), "ncr.min.js")
    if not os.path.exists(path):
        print(Fore.RED + "❌ File ncr.min.js tidak ditemukan di folder yang sama!")
        sys.exit(1)
    js = open(path, "r", encoding="utf-8").read()

    def parse_block(label):
        match = re.search(label + r"\s*[:=]\s*\{(.*?)\}", js)
        if not match: return {}
        block = match.group(1)
        # Tangkap semua variasi: "123":"Nama", '123':'Nama', 123:"Nama"
        pairs = re.findall(r"[\"']?(\d+)[\"']?\s*:\s*[\"']([^\"']+)[\"']", block)
        return {k: v for k, v in pairs}

    return {
        "provinsi": parse_block("provinsi"),
        "kabkot": parse_block("kabkot"),
        "kecamatan": parse_block("kecamatan")
    }

# ---------- Parsing NIK ---------- #

def parse_nik(nik):
    if not (nik.isdigit() and len(nik) == 16):
        return None, "NIK harus 16 digit angka."

    kode_prov, kode_kab, kode_kec = nik[:2], nik[:4], nik[:6]
    day, month, year = int(nik[6:8]), int(nik[8:10]), int(nik[10:12])
    unik = nik[12:16]

    kelamin = "Laki - laki"
    if day > 40:
        kelamin = "Perempuan"
        day -= 40

    now = datetime.now()
    year += 1900 if year > now.year % 100 else 2000

    try:
        lahir = datetime(year, month, day)
    except:
        return None, "Tanggal lahir tidak valid."

    return {
        "prov": kode_prov,
        "kab": kode_kab,
        "kec": kode_kec,
        "unik": unik,
        "kelamin": kelamin,
        "lahir": lahir,
        "nik": nik
    }, None

# ---------- Tampilkan Hasil ---------- #

def tampilkan_hasil(nik_data, wilayah):
    prov = wilayah["provinsi"].get(nik_data["prov"])
    kab = wilayah["kabkot"].get(nik_data["kab"])
    kec_data = wilayah["kecamatan"].get(nik_data["kec"])

    # Auto fallback: ambil data level terdekat
    if not prov:
        prov = next((v for k, v in wilayah["provinsi"].items() if k.startswith(nik_data["prov"][:1])), "Tidak diketahui")
    if not kab:
        kab = next((v for k, v in wilayah["kabkot"].items() if k.startswith(nik_data["prov"])), "Tidak diketahui")
    if not kec_data:
        kec_data = next((v for k, v in wilayah["kecamatan"].items() if k.startswith(nik_data["kab"])), "Tidak diketahui")

    kec, kodepos = ("Tidak diketahui", "-")
    if kec_data and isinstance(kec_data, str):
        kec, kodepos = kec_data.split("--") if "--" in kec_data else (kec_data, "-")

    print(Fore.GREEN + "\n✅ STATUS: SUCCESS !\n")
    print(Fore.YELLOW + f"NIK: {Fore.WHITE}{nik_data['nik']}")
    print(Fore.YELLOW + f"KELAMIN: {Fore.WHITE}{nik_data['kelamin']}")
    print(Fore.YELLOW + f"LAHIR: {Fore.WHITE}{nik_data['lahir'].strftime('%d/%m/%Y')}")
    print(Fore.CYAN + f"PROVINSI: {Fore.WHITE}{prov}")
    print(Fore.CYAN + f"KOTAKAB: {Fore.WHITE}{kab}")
    print(Fore.CYAN + f"KECAMATAN: {Fore.WHITE}{kec.strip()}")
    print(Fore.CYAN + f"UNIQCODE: {Fore.WHITE}{nik_data['unik']}")
    print(Fore.MAGENTA + f"KODEPOS: {Fore.WHITE}{kodepos.strip()}")
    print(Fore.LIGHTGREEN_EX + f"PASARAN: {Fore.WHITE}{pasaran_jawa(nik_data['lahir'])} {nik_data['lahir'].strftime('%d %B %Y')}")
    print(Fore.LIGHTGREEN_EX + f"USIA: {Fore.WHITE}{hitung_usia(nik_data['lahir'])}")
    print(Fore.LIGHTGREEN_EX + f"ULTAH: {Fore.WHITE}{ultah_berikutnya(nik_data['lahir'])}")
    print(Fore.LIGHTGREEN_EX + f"ZODIAK: {Fore.WHITE}{zodiak(nik_data['lahir'].day, nik_data['lahir'].month)}\n")

# ---------- Main CLI ---------- #

if __name__ == "__main__":
    banner()
    nik = input(Fore.LIGHTYELLOW_EX + "MASUKAN NIK : " + Fore.WHITE).strip()
    wilayah = parse_ncr_js()
    loading()
    data, err = parse_nik(nik)
    if err:
        print(Fore.RED + f"❌ {err}")
        sys.exit(1)
    tampilkan_hasil(data, wilayah)
