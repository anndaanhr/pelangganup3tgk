from sqlalchemy import Column, BigInteger, String, Integer, Float, Index, Numeric
from sqlalchemy.dialects.postgresql import NUMERIC
from database import Base

class Customer2024(Base):
    __tablename__ = "customers_2024"
    
    idpel = Column(BigInteger, primary_key=True, index=True)
    unitup = Column(Integer, index=True)
    nama = Column(String)
    alamat = Column(String)
    tarif = Column(String, index=True)
    daya = Column(Integer)
    kddk = Column(String)
    cater = Column(String)
    penyulang = Column(String, index=True)  # Unit ULP
    gardu = Column(String, index=True)
    merk_kwh = Column(String)
    nomor_meter = Column(BigInteger)
    jenis = Column(String, index=True)
    layanan = Column(String, index=True)
    kd_proses = Column(String, index=True)
    
    # Kolom bulanan 2024
    dec_2023 = Column(NUMERIC(15, 2))
    jan_2024 = Column(NUMERIC(15, 2))
    feb_2024 = Column(NUMERIC(15, 2))
    mar_2024 = Column(NUMERIC(15, 2))
    apr_2024 = Column(NUMERIC(15, 2))
    may_2024 = Column(NUMERIC(15, 2))
    jun_2024 = Column(NUMERIC(15, 2))
    jul_2024 = Column(NUMERIC(15, 2))
    aug_2024 = Column(NUMERIC(15, 2))
    sep_2024 = Column(NUMERIC(15, 2))
    oct_2024 = Column(NUMERIC(15, 2))
    nov_2024 = Column(NUMERIC(15, 2))
    dec_2024 = Column(NUMERIC(15, 2))

class Customer2025(Base):
    __tablename__ = "customers_2025"
    
    idpel = Column(BigInteger, primary_key=True, index=True)
    unitup = Column(Integer, index=True)
    nama = Column(String)
    alamat = Column(String)
    tarif = Column(String, index=True)
    daya = Column(Integer)
    kddk = Column(String)
    cater = Column(String)
    penyulang = Column(String, index=True)  # Unit ULP
    gardu = Column(String, index=True)
    nomor_meter = Column(BigInteger)
    jenis = Column(String, index=True)
    layanan = Column(String, index=True)
    kd_proses = Column(String, index=True)
    
    # Kolom bulanan 2025
    dec_2024 = Column(NUMERIC(15, 2))
    jan_2025 = Column(NUMERIC(15, 2))
    feb_2025 = Column(NUMERIC(15, 2))
    mar_2025 = Column(NUMERIC(15, 2))
    apr_2025 = Column(NUMERIC(15, 2))
    may_2025 = Column(NUMERIC(15, 2))
    jun_2025 = Column(NUMERIC(15, 2))
    jul_2025 = Column(NUMERIC(15, 2))
    aug_2025 = Column(NUMERIC(15, 2))
    sep_2025 = Column(NUMERIC(15, 2))
    oct_2025 = Column(NUMERIC(15, 2))
    nov_2025 = Column(NUMERIC(15, 2))
    dec_2025 = Column(NUMERIC(15, 2))


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") # 'admin' or 'user'
