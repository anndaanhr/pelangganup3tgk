#!/bin/bash

echo "========================================"
echo "Setup Database PostgreSQL untuk PLN Trend Analysis"
echo "========================================"
echo ""

# Cek apakah PostgreSQL terinstall
if ! command -v psql &> /dev/null; then
    echo "ERROR: PostgreSQL tidak ditemukan!"
    echo "Silakan install PostgreSQL terlebih dahulu."
    exit 1
fi

echo "PostgreSQL ditemukan!"
echo ""

# Minta input password PostgreSQL superuser
read -sp "Masukkan password PostgreSQL superuser (postgres): " PG_PASSWORD
echo ""

# Set password untuk psql
export PGPASSWORD=$PG_PASSWORD

echo "Membuat database dan user..."
echo ""

# Jalankan script SQL
psql -U postgres -h localhost -f setup_database.sql

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Gagal membuat database!"
    echo "Pastikan PostgreSQL berjalan dan password benar."
    exit 1
fi

echo ""
echo "========================================"
echo "Database berhasil dibuat!"
echo "Database: pln_trend_db"
echo "User: pln_user"
echo "Password: pln_password"
echo "========================================"
echo ""

