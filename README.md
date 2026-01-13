# PLN Trend Analysis Website

Website analisis tren pemakaian listrik pelanggan PLN dengan perbandingan data tahun 2024 dan 2025.

## Struktur Project

plncursor/
├── backend/                    # FastAPI backend
│   ├── api/                   # API routes
│   │   └── routes/
│   │       └── customers.py   # Customer endpoints
│   ├── services/              # Business logic
│   │   └── analysis.py        # Analysis service
│   ├── scripts/               # Business scripts (import, etc)
│   │   └── import_excel.py   # Excel import script
│   ├── alembic/               # Database migrations
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── database.py            # Database connection
│   └── main.py                # FastAPI app
├── frontend/                   # Next.js frontend
│   ├── app/                   # App router pages
│   │   ├── page.tsx           # Homepage (search)
│   │   └── ...
│   ├── components/            # React components
│   └── ...
├── scripts/                    # Setup and Utility scripts
│   ├── setup.bat
│   ├── setup.sh
│   ├── analyze_data.py
│   └── ...
├── data/                       # Data Excel files
│   └── *.xlsx
├── docs/                       # Documentation
│   ├── INSTALL.md
│   ├── QUICKSTART.md
│   └── ...
├── database/                   # Database scripts
└── README.md                   # Main documentation

## Fitur

✅ **Pencarian Pelanggan** - Cari berdasarkan IDPEL dengan validasi
✅ **Analisis Perbandingan** - Total konsumsi, selisih, persentase perubahan
✅ **Tren Bulanan** - Grafik line chart interaktif 2024 vs 2025
✅ **Pelanggan Baru** - Daftar pelanggan baru di 2025 dengan filter & pagination
✅ **Pelanggan Hilang** - Daftar pelanggan hilang dari 2024 dengan filter & pagination
✅ **Deteksi Anomali** - Identifikasi perubahan konsumsi >50%
✅ **Perubahan Atribut** - Deteksi perubahan TARIF, DAYA, JENIS, LAYANAN
✅ **Desain PLN** - Branding dengan warna biru PLN (#0066CC) dan kuning (#FFD700)

## Quick Start (Paling Mudah)

### Opsi 1: Menggunakan Docker (Recommended)

1. **Start PostgreSQL dengan Docker:**
   ```bash
   docker-compose up -d postgres
   ```

2. **Setup dan jalankan sistem:**
   ```bash
   # Windows
   scripts\setup.bat
   
   # Linux/Mac
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Jalankan aplikasi:**
   ```bash
   # Windows
   scripts\start.bat
   
   # Linux/Mac
   chmod +x scripts/start.sh
   ./scripts/start.sh
   ```

### Opsi 2: PostgreSQL Manual

1. **Setup database:**
   ```bash
   # Windows
   scripts\setup_database.bat
   
   # Linux/Mac
   chmod +x scripts/setup_database.sh
   ./scripts/setup_database.sh
   ```

2. **Setup lengkap:**
   ```bash
   # Windows
   scripts\setup.bat
   
   # Linux/Mac
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

Lihat **docs/QUICKSTART.md** untuk panduan lengkap.

## Setup Manual

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (atau Docker)
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (atau Docker)
- File Excel: `data/JUAL PERPELANGGAN 2024 BL.xlsx` dan `data/JUAL PERPELANGGAN 2025 BL.xlsx`

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
# atau jika menggunakan user install:
python -m pip install -r requirements.txt --user
```

2. Setup database PostgreSQL dan buat file `.env`:
```bash
cd backend
cp .env.example .env
# Edit .env dengan kredensial database Anda:
# DATABASE_URL=postgresql://user:password@localhost:5432/pln_trend_db
```

3. Buat database:
```sql
CREATE DATABASE pln_trend_db;
```

4. Run migrations:
```bash
cd backend
python -m alembic upgrade head
```

5. Import data Excel (sampling 1000 records):
```bash
cd backend
python scripts/import_excel.py
```

6. Start server:
```bash
cd backend
python -m uvicorn main:app --reload
# atau
uvicorn main:app --reload
```

Backend akan berjalan di `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. (Optional) Buat file `.env.local` untuk custom API URL:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start development server:
```bash
cd frontend
npm run dev
```

Frontend akan berjalan di `http://localhost:3000`

## API Endpoints

- `GET /api/customers/{idpel}` - Get customer data by IDPEL
- `GET /api/customers/{idpel}/analysis` - Get complete analysis
- `GET /api/customers/{idpel}/trends` - Get monthly trends
- `GET /api/customers/new` - Get new customers (with filters & pagination)
- `GET /api/customers/lost` - Get lost customers (with filters & pagination)

## Teknologi

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, pandas, Alembic
- **Frontend**: Next.js 14 (App Router), TypeScript, TailwindCSS, Recharts
- **Database**: PostgreSQL 15+

## Catatan

- Data di-sample menjadi ~1000 pelanggan untuk performa (semua common + sample dari new/lost)
- Format angka menggunakan format Indonesia (ribuan dengan titik)
- Sistem dirancang scalable dan mudah dikembangkan untuk fitur tambahan
