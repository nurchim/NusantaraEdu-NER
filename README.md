# NusantaraEdu-NER — Web Deployment

Aplikasi web publik untuk mengenali entitas budaya Indonesia dari teks Bahasa Indonesia menggunakan model spaCy NER hasil pipeline NusantaraEdu-NER.

## Jalankan lokal

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pytest -q
python -m uvicorn api.index:app --reload
```

Buka `http://127.0.0.1:8000`.

Endpoint utama:

- `GET /`
- `GET /api/health`
- `GET /api/model-info`
- `POST /api/predict`
- `POST /api/quiz`
- `GET /api/docs`

## GitHub

```bash
git init
git add .
git commit -m "feat: deploy NusantaraEdu-NER web app"
git branch -M main
git remote add origin https://github.com/USERNAME/nusantaraedu-ner.git
git push -u origin main
```

## Vercel

1. Import repository GitHub di Vercel.
2. Root Directory: repository root.
3. Deploy.
4. Verifikasi `/api/health`, `/api/model-info`, lalu halaman `/`.

Model produksi berada di `models/production/model-best` dan sengaja ikut repository agar fungsi inferensi dapat berjalan di Vercel.

## Catatan

Metrik pada interface dibaca dari `models/production/manifest.json`. Metrik test set tidak menjamin setiap prediksi selalu benar.
