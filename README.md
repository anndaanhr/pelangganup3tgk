# ⚡ Sistem Analisis Pelanggan & Tren Pemakaian Listrik PLN UP3

Sistem ini adalah platform analitik cerdas berbasis web (*Web-based Executive Dashboard*) yang dirancang khusus untuk memonitor, menganalisis, dan mengekstraksi wawasan berharga dari jutaan baris riwayat data pelanggan operasional **PT. PLN (Persero)** pada rentang tahun 2024 dan 2025. Sistem ini dirancang dengan pendekatan *Big Data Analysis* dalam arsitektur skala mikro.

---

## 🌟 Fitur Utama (Core Features)

Sistem ini tidak sekadar menampilkan data, namun memproses operasi matematis mutakhir untuk membantu pimpinan PLN dalam mengambil keputusan:

1. **Dashboard Eksekutif Komparatif**
   Menyajikan perbandingan kumulatif secara berdampingan antara tahun operasional 2024 dan 2025 meliputi Total Tagihan (KWh), Pendapatan Nilai Konversi (Rupiah), serta Pertumbuhan Volume Konsumen.
   
2. **Kecerdasan Deteksi Anomali Pemakaian (Anomaly Detection)**
   * **Zero Usage Tracker:** Mendeteksi deretan rumah tangga/pelanggan yang secara ganjil menorehkan angka meteran listrik statis 0 KWh selama beberapa bulan berturut-turut.
   * **High Variance Deviation:** Melacak anomali fluktuasi (*Spike/Drop*) pelanggan secara ekstrem (misal penyimpangan angka tagihan terjun drastis hingga >200% dalam sebulan).

3. **Hukum Pareto Bisnis (Top Contributors)**
   Mengurutkan daftar pelanggan raksasa (*High Value Customers*) yang mendominasi penggunaan tegangan terbesar di sebuah wilayah instansi ULP/UP3 PLN.

4. **Kalkulator Distribusi Infrastruktur & Daya**
   Memvisualisasikan beban trafo sebaran Gardu listrik dan mengevaluasi komposisi konsumen berdasarkan Golongan Tarif Daya (450 VA, 900 VA, dst).
   
5. **Autentikasi Terpusat Berbasis Otorisasi Bertingkat**
   Melindungi rute privasi data PLN berbasis penguncian Token akses (*Role-Based Access Control* JWT).

---

## 🏗️ Arsitektur Teknologi Utama (Tech Stack)

Aplikasi ini dibagi menjadi tiga ekosistem monolitik yang saling berbicara lewat integrasi REST API modern.

### 1. 🖥️ Frontend (Sisi Klien/Antarmuka)
Berfokus pada kecepatan muat yang lincah berlapis keindahan estetika UI interaktif.
* **Framework:** React.js (berpadu kokoh dengan **TypeScript** untuk stabilitas tipe bahasa)
* **Styling Engine:** Tailwind CSS
* **Data Visualization:** Recharts (untuk meramu kurva responsif diagram garis komparasi dan *pie-charts*)
* **Library Ekstra:** Axios (klien HTTP API), Lucide-React (aset ikon tata letak)
* **Deployment System:** Vercel Hosting (Serverless Deployment)

### 2. ⚙️ Backend (Sisi Peladen & Otak Algoritma)
Bertanggung jawab sebagai mesin komputasi matematis penarik database tanpa merusak kestabilan RAM skala sempit.
* **Framework:** Python **FastAPI** (Desain Asynchronous I/O dan eksekusi non-blocking)
* **Authentication:** Passlib + Bcrypt + OAuth2/JWT Bearer
* **Database ORM:** SQLAlchemy (pemeta kode objek relasional menjadi konversi barisan SQL murni)
* **API Documentation:** Swaager UI (otomatis menyatu melalui standar OpenAPI bawaan Python)
* **Deployment System:** Render App (PaaS Cloud Runtime Linux Terminal)

### 3. 🗄️ Database (Sisi Gudang Data)
* **Platform:** PostgreSQL hosted by **Supabase** (Platform awan *Database as a Service*)

---

## 🔬 Arsitektur Optimasi Performa (Backend Innovations)
Karena keterbatasan operasional dari mesin server gratis (*Free Tier RAM 512MB*), arsitektur menancapkan optimisasi tingkat lanjut:

1. **Server-Side Cursor Streaming (`yield_per`)** 
   Meniadakan serangan kerusakan *Out Of Memory* (OOM). Skrip akan mengisap jutaan rincian tagihan dari DB Supabase secara rapi menggunakan blok-blok iterator potongan kecil ke dalam RAM sebelum menghitung agregasinya.
   
2. **Permanent JSON Disk Caching** 
   Mengeliminasi rintangan memuat antarmuka yang sangat lama (*1 menit delay*). Data anomali dan Pareto yang dikalkulasi pada hari perintis akan ditebarkan dan dibekukan ke dalam penyimpanan *file* berkas internal sistem. Untuk penarikan pelaporan *dashboard* di waktu selanjutnya, respon melesat ke batas ekstrem yakni `~0.1 mili-detik`.
   
3. **Persistensi Connection Pooling**
   Mencegah tabrakan di perbatasan sirkulasi port koneksi *database* (kematian sesak napas koneksi) menggunakan properti *Connection Timeouts*, `pool_pre_ping`, dan *Recycle Hooks* dari mesin SQLAlchemy.
   
4. **Alat Pacu Jantung Server Otomatis (Keep Awake)**
   Tiga lapis ekosistem ditenagai menggunakan *GitHub Actions (Cron Job)* `.github/workflows/keep_awake.yml` untuk memanggil paksa mesin Render dari potensi terseret masuk ke masa "istirahat/hibernasi mesin awan." Pemanggilan ini menumbuhkan jembatan respons bebas jeda bagi Direksi PLN yang bermaksud login masuk di luar jam normal.

---

## 🧩 Tata Cara Komunikasi Alur Proses (Data Flow)
1. **[Eksternal]** Administrator/Pegawai TU mem-forward lembar data master CSV Excel historis Pelanggan (2024 & 2025) untuk diserap secara struktural ke badan Supabase.
2. **[Klien]** Pengguna (*User* PLN) membuka pranala Vercel situs dan mengakses halaman dengan mandat kredensial rahasianya.
3. **[Proksi]** FastAPI mengirimkan persetujuan mandat *Access Token* JWT.
4. **[Eksekusi]** Bereaksi dari ketukan tombol rentang tabel Dasbor, FastAPI beringsut membuka gulungan relasional dari Supabase dan melakukan *filtering* kompleks (semisal: Melacak idpel yang tagihannya melompat sebesar > 200%).
5. **[Resolusi]** Himpunan balasan algoritme diubah susunannya meniru standar struktur balasan web JSON (*Pagination Limits diterapkan* jika perlu), lalu dilemparkan ke Recharts-React guna dibedah secara grafis. Seluruh proses pengiriman selesai dalam hitungan fraksi detik menggunakan *engine Cache Disk* awan.

---
*Dibuat ekslusif dan dioperasikan sepenuhnya untuk pengembangan kapabilitas intelektual struktural oleh Departemen Tim KP (Kerja Praktik) Instansi Pelayanan PT. PLN.*
