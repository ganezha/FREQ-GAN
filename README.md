<div align="center">

# ⚡ FREQ-GAN

**Bot trading futures Bitget berbasis freqtrade — strategi GanTrendEma4h, scanner realtime, VectorBT, dan dashboard Sci-Fi HUD.**

[![Mode](https://img.shields.io/badge/mode-DRY--RUN-yellow?style=for-the-badge)](#%EF%B8%8F-peringatan)
[![License](https://img.shields.io/badge/license-GPLv3-blue?style=for-the-badge)](LICENSE)
[![freqtrade](https://img.shields.io/badge/freqtrade-2026.10-2ea44f?style=for-the-badge)](https://github.com/freqtrade/freqtrade)
[![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Bitget](https://img.shields.io/badge/Bitget-Futures-00F0FF?style=for-the-badge)](https://www.bitget.com/)

[Fitur](#-fitur) •
[Arsitektur](#%EF%B8%8F-arsitektur) •
[Instalasi](#-instalasi) •
[Kontrol](#%EF%B8%8F-kontrol-satu-jalur-saklar) •
[Keamanan](#-keamanan) •
[Backtest](#-hasil-backtest) •
[Lisensi](#-lisensi)

<br>

<table>
<tr>
<td align="center"><img src="docs/images/hud-landscape.png" alt="FREQ-GAN HUD landscape" height="260"><br><sub>Landscape</sub></td>
<td align="center"><img src="docs/images/hud-portrait.png" alt="FREQ-GAN HUD potret" height="260"><br><sub>Potret (iPad)</sub></td>
</tr>
</table>

<sub>Dashboard Sci-Fi HUD 1.8.0 — System Connectome &amp; panel telemetri (mode simulasi)</sub>

</div>

> [!NOTE]
> **Fork dari [freqtrade](https://github.com/freqtrade/freqtrade), dimodifikasi oleh ganezha sejak 2026.**

> [!WARNING]
> Proyek ini berjalan dalam mode **DRY-RUN** (simulasi, tanpa dana nyata). Trading futures dengan leverage berisiko sangat tinggi dan dapat menghabiskan modal. Gunakan dengan risiko Anda sendiri.

---

## 📑 Daftar Isi

- [Fitur](#-fitur)
- [Arsitektur](#%EF%B8%8F-arsitektur)
- [Instalasi](#-instalasi)
- [Kontrol (satu jalur saklar)](#%EF%B8%8F-kontrol-satu-jalur-saklar)
- [Keamanan](#-keamanan)
- [Hasil Backtest](#-hasil-backtest)
- [Kredit](#-kredit)
- [Lisensi](#-lisensi)

---

## ✨ Fitur

| Komponen | Keterangan |
|:--|:--|
| 🎯 **Strategi** | `GanTrendEma4h` — timeframe 4h, long + short, leverage 2x isolated |
| 🧪 **Strategy Lab** | 10 strategi futures diuji in-sample / out-of-sample (IS/OOS) |
| 📡 **Scanner** | Data pasar realtime Bitget USDT perpetuals via cryptofeed |
| 📈 **VectorBT** | Grid 21.168 kombinasi IS/OOS, top-3 berjalan sebagai paper account |
| 🛰️ **Dashboard** | Sci-Fi HUD 1.8.0 satu layar: System Connectome (19 node / 42 relasi), RSI &amp; MACD (TA-Lib), panel telemetri |

> Kode dashboard dikelola sebagai komponen terpisah (repositori privat).

---

## 🏗️ Arsitektur

```mermaid
flowchart LR
    EX[(Bitget Futures)]
    subgraph Docker["Docker network (internal)"]
        FT["freqtrade<br/>GanTrendEma4h"]
        GW["ccxt-gateway<br/>:8091 · order off"]
        VBT["vbt-engine<br/>:8092"]
        SC["scanner / HUD<br/>:8090"]
    end
    U([Pengguna · 127.0.0.1])
    EX <--> FT
    EX --> GW
    GW --> SC
    GW --> VBT
    VBT --> SC
    FT --> SC
    U --> FT
    U --> SC
```

| Layanan | Alamat | Fungsi |
|:--|:--|:--|
| `freqtrade` | `127.0.0.1:8080` | Bot trading + FreqUI |
| `freqgan-scanner` | `127.0.0.1:8090` | Scanner + dashboard Sci-Fi HUD |
| `freqgan-ccxt-gateway` | internal `8091` | Data exchange via ccxt (order dinonaktifkan) |
| `freqgan-vbt-engine` | internal `8092` | Mesin backtest VectorBT |

---

## 🚀 Instalasi

```bash
git clone https://github.com/ganezha/FREQ-GAN.git
cd FREQ-GAN
git checkout gan-stable

# Siapkan konfigurasi (panduan lengkap di config.example.md)
cp config.example.json user_data/config.json

# Jalankan layanan
docker compose up -d
```

> [!TIP]
> Isi rahasia (API key, password) hanya di file `.env`, jangan di `config.json` yang ter-commit.

---

## 🎛️ Kontrol (satu jalur saklar)

Semua layanan dikendalikan hanya lewat tiga perintah:

| Perintah | Fungsi |
|:--|:--|
| `~/bin/bot-on` | Menyalakan semua layanan |
| `~/bin/bot-off` | Mematikan semua layanan |
| `~/bin/bot-status` | Menampilkan status layanan |

---

## 🔐 Keamanan

- 🔑 Rahasia disimpan di `.env` dengan izin `chmod 600` dan **tidak pernah di-commit**.
- 🚫 API key exchange **tanpa izin withdraw** dan dibatasi **IP whitelist**.
- 🧱 Port hanya terikat ke `127.0.0.1` atau jaringan internal Docker.
- 🕵️ Setiap commit dipindai dengan [gitleaks](https://github.com/gitleaks/gitleaks).

---

## 📊 Hasil Backtest

| Periode | Rentang | Trade | Win rate | Profit |
|:--|:--|--:|--:|--:|
| In-sample | 2024-09-01 → 2026-08-01 | — | 83,5% | **+70,5%** |
| Out-of-sample | 2026-08 → 2026-11-06 | 20 | 75% | **+2,6%** |

> [!CAUTION]
> Hasil backtest masa lalu **tidak menjamin** hasil di masa depan. Bukan nasihat keuangan.

---

## 🙏 Kredit

Dibangun di atas **[freqtrade](https://github.com/freqtrade/freqtrade)** © tim dan kontributor freqtrade. README asli proyek tersimpan di riwayat repositori upstream.

## 📄 Lisensi

Didistribusikan di bawah **GNU General Public License v3.0**, sama dengan proyek asli. Lihat [LICENSE](LICENSE).

<div align="center"><sub>FREQ-GAN · dimodifikasi oleh ganezha · 2026</sub></div>
