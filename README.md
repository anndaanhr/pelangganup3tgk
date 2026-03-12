# Energy Monitor - Dashboard Analisis Tren Listrik PLN

Platform monitoring dan analisis data pelanggan PLN yang membandingkan performa penjualan energi tahun 2024 vs 2025.
Didesain untuk UP3 Tanjung Karang guna memudahkan evaluasi, deteksi anomali, dan pemantauan kinerja ULP.

## Fitur Unggulan

### 📊 Dashboard Analytics (Pusat Komando)
- **Ringkasan Eksekutif**: Total pelanggan, total energi (GWh), dan statistik Churn/New Customer.
- **Filter ULP Terintegrasi**: Dropdown untuk memfilter **SEMUA** data dashboard berdasarkan Unit Layanan Pelanggan (ULP).
- **Grafik Tren Interaktif**: Visualisasi pemakaian energi bulanan (2024 vs 2025).
- **Pencarian Cepat**: Cari data detail pelanggan berdasarkan ID Pelanggan langsung dari dashboard.

### 🔍 Deep Dive Analysis (Analisis Mendalam)
1.  **Analisis Pareto (Top 10)**: Identifikasi 20% pelanggan yang menyumbang 80% pendapatan.
2.  **Monitoring Infrastruktur**: Analisis beban Gardu Distribusi untuk mendeteksi overload atau under-utilization.
3.  **Analisis Daya & Tarif**: Distribusi pelanggan berdasarkan batas daya (VA) dan golongan tarif.
4.  **Siklus Hidup Pelanggan**:
    - **Power Change**: Perubahan daya (Tambah/Turun Daya).
    - **Anomali**: Deteksi pelanggan dengan penggunaan 0 kWh berturut-turut.
5.  **Comparative Analysis**: Head-to-head metrics 2024 vs 2025 (Tarif, Jenis, Layanan).

### 🛡️ Keamanan & Data
- **Sistem Autentikasi**: Login aman menggunakan JWT (JSON Web Tokens) dan Bcrypt hashing.
- **Optimasi Data**: Caching cerdas untuk performa loading yang cepat pada dataset besar.

## Struktur Project

```plaintext
pln2juta/
├── backend/                    # FastAPI Backend Server
│   ├── api/routes/            # Endpoint API (Analytics, Auth, Customers)
│   ├── services/              # Business Logic & Analysis Engines
│   │   ├── analysis.py        # Core Stats Analysis
│   │   ├── advanced_analysis.py # Heavy Data Processing
│   │   ├── auth_service.py    # Authentication Logic
│   │   └── ulp_analysis.py    # ULP Aggregation Logic
│   ├── models.py              # Database Schema (SQLAlchemy)
│   ├── database.py            # DB Connection Config
│   └── main.py                # App Entry Point
│
├── frontend/                   # React + Vite Frontend
│   ├── src/
│   │   ├── pages/             # Halaman Aplikasi
│   │   ├── components/        # Reusable UI Components
│   │   ├── services/          # API Integration Services
│   │   └── App.tsx            # Routing & Auth Protection
│
├── scripts/                    # Utility Scripts (Setup, Start)
└── data/                       # Source Data Files (.xlsx)
```

## Quick Start (Cara Menjalankan)

### 1. Prasyarat
- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL**

### 2. Instalasi & Setup
Jalankan script otomatis untuk setup environment:

Windows:
```cmd
scripts\setup.bat
```
Linux/Mac:
```bash
./scripts/setup.sh
```

### 3. Menjalankan Aplikasi
Gunakan script `start` untuk menjalankan Backend dan Frontend sekaligus:

Windows:
```cmd
scripts\start.bat
```

Aplikasi akan berjalan di:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Dokumentasi API**: http://localhost:8000/docs

## Development Notes

### Backend (Python/FastAPI)
- Menggunakan **SQLAlchemy ORM** untuk query database yang efisien.
- **Pydantic** untuk validasi data request/response.
- **Alembic** untuk manajemen migrasi database.

### Frontend (React/Vite)
- Dibuat dengan **TypeScript** untuk keamanan tipe data.
- Styling menggunakan **Tailwind CSS** untuk desain modern dan responsif.
- Grafik visualisasi menggunakan **Recharts**.

### Kontak & Support
Dikembangkan untuk Tim Strategi Pemasaran PLN UP3 Tanjung Karang.
Hubungi administrator untuk akses kredensial atau bantuan teknis.
