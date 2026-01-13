-- Script untuk setup database PostgreSQL PLN Trend Analysis
-- Jalankan sebagai superuser PostgreSQL

-- Buat database
CREATE DATABASE pln_trend_db;

-- Buat user (jika belum ada)
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'pln_user') THEN
    CREATE USER pln_user WITH PASSWORD 'pln_password';
  END IF;
END
$$;

-- Berikan privileges
GRANT ALL PRIVILEGES ON DATABASE pln_trend_db TO pln_user;

-- Connect ke database
\c pln_trend_db

-- Berikan schema privileges
GRANT ALL ON SCHEMA public TO pln_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO pln_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO pln_user;

