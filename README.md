# Rebel Football Calculator

Simple, offline, bilingual (Indonesian / English) football match prediction calculator.
Kalkulator prediksi pertandingan sepak bola yang sederhana, offline, dua bahasa (Indonesia / Inggris).

**Live demo:** enable GitHub Pages (Settings → Pages → branch `main`, folder `/root`) and open the link.

## Features / Fitur
- Enter home and away team names, handicap and Over/Under line. The **last 5 real results of each team are fetched automatically** (TheSportsDB); you can still edit them by hand (e.g. `2-1`). / Hasil 5 laga terakhir diambil otomatis dari data nyata, tetap bisa diedit manual.
- Output: suggested pick, most likely final score, win/draw/win chances, handicap and Over/Under chances, top 5 scorelines, confidence level.
- Supports quarter lines (-0.25, +0.75, 2.75, ...). Language switch ID/EN, history of last 5 predictions, light/dark mode.
- No server, no tracking, no dependencies: one `index.html`.

## Data source / Sumber data
Results come from the free [TheSportsDB](https://www.thesportsdb.com/) API (test key `3`, attribution required). The free key is rate limited and some leagues may have incomplete data. For heavier use, get your own key and paste it into the app ("API key" field). Always check the match list shown under the form. Use English team names (e.g. `Man City`, `Arsenal`).
Kunci gratis dibatasi dan data sebagian liga bisa kurang lengkap; cek daftar laga yang tampil di bawah form.

## How it works / Cara kerja
Poisson goal model. Each team's attack and defence strength comes from its last 5 matches, blended 70/30 with a league average (1.35 goals), plus a small home advantage. The score grid (0–8 goals) gives all probabilities.
Model Poisson: kekuatan serang dan bertahan tiap tim dari 5 laga terakhir, dicampur 70/30 dengan rata-rata liga, ditambah keunggulan kandang kecil.

## Accuracy / Akurasi
This repo makes **no accuracy claim**. Measure it yourself with the backtest:
Repo ini **tidak mengklaim akurasi**. Ukur sendiri dengan backtest:

```bash
# 1. Download season CSVs from https://www.football-data.co.uk/data.php (oldest first)
# 2. Run:
python backtest.py E0.csv
```

It prints 1X2 accuracy, a baseline (always pick home), Over/Under 2.5 accuracy and the Brier score. Put the real numbers here once you have 300+ matches tested.
Setelah menguji 300+ laga, tulis angka aslinya di sini.

| League / Liga | Matches / Laga | 1X2 accuracy | Baseline | O/U 2.5 |
|---|---|---|---|---|
| _(run backtest)_ | | | | |

## Disclaimer
Predictions are statistical estimates and can be wrong; real matches depend on many things on the pitch (injuries, red cards, weather, motivation). Not betting advice.
Prediksi hanyalah perkiraan statistik dan bisa salah; hasil di lapangan bergantung banyak hal. Bukan saran berjudi.

## License
MIT
