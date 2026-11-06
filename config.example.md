# Petunjuk config.example.json (FREQ-GAN)

Sumber resmi: https://www.freqtrade.io/en/stable/configuration/
Bitget: https://www.freqtrade.io/en/stable/exchanges/#bitget
Futures/Leverage: https://www.freqtrade.io/en/stable/leverage/

## Cara pakai
1. Salin: `cp config.example.json user_data/config.json`
2. Ganti semua nilai berawalan `ISI_` / `GANTI_`.
3. Kunci: `chmod 600 user_data/config.json`
4. Validasi: `docker compose run --rm freqtrade show-config --config user_data/config.json`
Bot hanya membaca `user_data/config.json` (file asli). File contoh ini tidak dibaca bot.

## Bagian penting
| Kunci | Contoh | Arti |
|---|---|---|
| dry_run | true | true = simulasi, tanpa uang asli. Wajib true sampai diizinkan live. |
| dry_run_wallet | 1000 | Saldo simulasi (USDT). |
| stake_currency | "USDT" | Mata uang modal. |
| stake_amount | "unlimited" / 50 | Modal per trade; unlimited = bagi rata saldo / max_open_trades. |
| max_open_trades | 3 | Maksimal posisi terbuka bersamaan. |
| timeframe | "5m" | Timeframe candle strategi. |
| trading_mode | "futures" | Mode futures (perpetual). |
| margin_mode | "isolated" | Bitget futures HANYA mendukung isolated (resmi). |
| exchange.name | "bitget" | Exchange. |
| exchange.key / secret | "" | API key Bitget. Kosong saat dry-run. |
| exchange.password | "" | Passphrase API Bitget (wajib untuk Bitget saat live). |
| pair_whitelist | "BTC/USDT:USDT" | Format pair futures: BASE/QUOTE:SETTLE. |
| pairlists | StaticPairList | Pakai daftar pair_whitelist apa adanya. |
| api_server.listen_ip_address | "0.0.0.0" | Wajib 0.0.0.0 di Docker; tetap aman karena port compose 127.0.0.1:8080. |
| api_server.jwt_secret_key / ws_token | acak | Generate: `openssl rand -hex 32` |
| api_server.username / password | - | Login FreqUI. Jangan dibagikan. |

## Catatan keamanan
- JANGAN commit `user_data/config.json` (sudah di-ignore git).
- Saat live: API key tanpa izin withdraw + IP whitelist 108.61.201.96.
- Bitget: freqtrade otomatis set akun ke One-way Mode saat start.
- Leverage diatur di strategi lewat callback `leverage()` (default 1x).
