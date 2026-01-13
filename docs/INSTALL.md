# Panduan Instalasi Lengkap - PLN Trend Analysis

## Persyaratan Sistem

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/) atau Docker
- **File Excel** - `JUAL PERPELANGGAN 2024 BL.xlsx` dan `JUAL PERPELANGGAN 2025 BL.xlsx` di folder root

## Metode Instalasi

### Metode 1: Menggunakan Docker (Paling Mudah)

#### Langkah 1: Install Docker Desktop
- Download dari: https://www.docker.com/products/docker-desktop
- Install dan jalankan Docker Desktop

#### Langkah 2: Start PostgreSQL
```bash
docker-compose up -d postgres
```

Ini akan membuat container PostgreSQL dengan konfigurasi:
- Database: `pln_trend_db`
- User: `pln_user`
- Password: `pln_password`
- Port: `5432`

#### Langkah 3: Setup Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
python scripts/import_excel.py
```

#### Langkah 4: Setup Frontend
```bash
cd frontend
npm install
```

#### Langkah 5: Jalankan Sistem

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

Atau manual di 2 terminal terpisah:
- Terminal 1: `cd backend && uvicorn main:app --reload`
- Terminal 2: `cd frontend && npm run dev`

### Metode 2: PostgreSQL Manual

#### Langkah 1: Install PostgreSQL
- Download dari: https://www.postgresql.org/download/
- Install dengan default settings
- Catat password superuser (postgres)

#### Langkah 2: Setup Database

**Windows:**
```bash
setup_database.bat
```

**Linux/Mac:**
```bash
chmod +x setup_database.sh
./setup_database.sh
```

Atau manual:
```bash
psql -U postgres -f setup_database.sql
```

#### Langkah 3: Konfigurasi Backend
File `backend/.env` sudah dibuat dengan konfigurasi default:
```
DATABASE_URL=postgresql://pln_user:pln_password@localhost:5432/pln_trend_db
```

Jika menggunakan kredensial berbeda, edit file ini.

#### Langkah 4: Setup Lengkap

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Script ini akan:
1. Install dependencies Python
2. Run database migrations
3. Import data Excel (~1000 records)
4. Install dependencies Node.js

#### Langkah 5: Jalankan Sistem

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

## Verifikasi Instalasi

1. **Cek Backend:**
   - Buka: http://localhost:8000
   - Harus menampilkan: `{"message": "PLN Trend Analysis API", "version": "1.0.0"}`
   - API Docs: http://localhost:8000/docs

2. **Cek Frontend:**
   - Buka: http://localhost:3000
   - Harus menampilkan halaman pencarian IDPEL

3. **Cek Database:**
   ```bash
   psql -U pln_user -d pln_trend_db -c "SELECT COUNT(*) FROM customers_2024;"
   psql -U pln_user -d pln_trend_db -c "SELECT COUNT(*) FROM customers_2025;"
   ```
   Harus menampilkan ~1000 records untuk masing-masing tabel.

## Troubleshooting

### Error: "connection to server failed"
**Solusi:**
- Pastikan PostgreSQL berjalan
- Windows: Cek Services → PostgreSQL
- Docker: `docker ps` harus menampilkan container `pln_postgres`
- Cek port 5432 tidak digunakan aplikasi lain

### Error: "ModuleNotFoundError: No module named 'pandas'"
**Solusi:**
```bash
pip install pandas openpyxl --user
# atau
python -m pip install pandas openpyxl --user
```

### Error: "Failed to import Excel"
**Solusi:**
- Pastikan file Excel ada di folder root project
- Nama file harus tepat: `JUAL PERPELANGGAN 2024 BL.xlsx` dan `JUAL PERPELANGGAN 2025 BL.xlsx`
- Pastikan file tidak sedang dibuka di aplikasi lain

### Error: "Port 8000/3000 already in use"
**Solusi:**
- Tutup aplikasi yang menggunakan port tersebut
- Atau ubah port di konfigurasi:
  - Backend: `uvicorn main:app --reload --port 8001`
  - Frontend: Edit `package.json` atau gunakan `PORT=3001 npm run dev`

### Error: "Permission denied" (Linux/Mac)
**Solusi:**
```bash
chmod +x setup.sh setup_database.sh start.sh
```

## Struktur File Setup

```
plncursor/
├── setup_database.sql      # Script SQL untuk membuat database
├── setup_database.bat      # Script Windows untuk setup database
├── setup_database.sh       # Script Linux/Mac untuk setup database
├── setup.bat                # Script Windows untuk setup lengkap
├── setup.sh                 # Script Linux/Mac untuk setup lengkap
├── start.bat                # Script Windows untuk menjalankan sistem
├── start.sh                 # Script Linux/Mac untuk menjalankan sistem
├── docker-compose.yml       # Konfigurasi Docker untuk PostgreSQL
├── QUICKSTART.md            # Panduan quick start
└── INSTALL.md               # File ini
```

## Default Credentials

⚠️ **PENTING:** Ganti password di production!

- **Database:** pln_trend_db
- **User:** pln_user
- **Password:** pln_password
- **Host:** localhost
- **Port:** 5432

## Next Steps

Setelah instalasi berhasil:
1. Buka http://localhost:3000
2. Cari pelanggan dengan IDPEL
3. Lihat analisis dan grafik
4. Explore halaman pelanggan baru/hilang

## Support

Jika mengalami masalah:
1. Cek file log di console
2. Pastikan semua prerequisites terinstall
3. Cek file `.env` di backend
4. Pastikan database berjalan dan accessible

