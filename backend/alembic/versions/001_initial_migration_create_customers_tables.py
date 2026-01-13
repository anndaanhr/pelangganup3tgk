"""Initial migration - create customers tables

Revision ID: 001
Revises: 
Create Date: 2025-01-27

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create customers_2024 table
    op.create_table(
        'customers_2024',
        sa.Column('idpel', sa.BigInteger(), nullable=False),
        sa.Column('unitup', sa.Integer(), nullable=True),
        sa.Column('nama', sa.String(), nullable=True),
        sa.Column('alamat', sa.String(), nullable=True),
        sa.Column('tarif', sa.String(), nullable=True),
        sa.Column('daya', sa.Integer(), nullable=True),
        sa.Column('kddk', sa.String(), nullable=True),
        sa.Column('gardu', sa.String(), nullable=True),
        sa.Column('merk_kwh', sa.String(), nullable=True),
        sa.Column('nomor_meter', sa.BigInteger(), nullable=True),
        sa.Column('jenis', sa.String(), nullable=True),
        sa.Column('layanan', sa.String(), nullable=True),
        sa.Column('kd_proses', sa.String(), nullable=True),
        sa.Column('dec_2023', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('jan_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('feb_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('mar_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('apr_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('may_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('jun_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('jul_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('aug_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('sep_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('oct_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('nov_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('dec_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.PrimaryKeyConstraint('idpel')
    )
    op.create_index(op.f('ix_customers_2024_idpel'), 'customers_2024', ['idpel'], unique=True)
    op.create_index(op.f('ix_customers_2024_tarif'), 'customers_2024', ['tarif'], unique=False)
    op.create_index(op.f('ix_customers_2024_gardu'), 'customers_2024', ['gardu'], unique=False)
    op.create_index(op.f('ix_customers_2024_jenis'), 'customers_2024', ['jenis'], unique=False)
    op.create_index(op.f('ix_customers_2024_layanan'), 'customers_2024', ['layanan'], unique=False)
    op.create_index(op.f('ix_customers_2024_kd_proses'), 'customers_2024', ['kd_proses'], unique=False)

    # Create customers_2025 table
    op.create_table(
        'customers_2025',
        sa.Column('idpel', sa.BigInteger(), nullable=False),
        sa.Column('unitup', sa.Integer(), nullable=True),
        sa.Column('nama', sa.String(), nullable=True),
        sa.Column('alamat', sa.String(), nullable=True),
        sa.Column('tarif', sa.String(), nullable=True),
        sa.Column('daya', sa.Integer(), nullable=True),
        sa.Column('kddk', sa.String(), nullable=True),
        sa.Column('gardu', sa.String(), nullable=True),
        sa.Column('nomor_meter', sa.BigInteger(), nullable=True),
        sa.Column('jenis', sa.String(), nullable=True),
        sa.Column('layanan', sa.String(), nullable=True),
        sa.Column('kd_proses', sa.String(), nullable=True),
        sa.Column('dec_2024', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('jan_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('feb_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('mar_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('apr_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('may_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('jun_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('jul_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('aug_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('sep_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('oct_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('nov_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.Column('dec_2025', sa.NUMERIC(15, 2), nullable=True),
        sa.PrimaryKeyConstraint('idpel')
    )
    op.create_index(op.f('ix_customers_2025_idpel'), 'customers_2025', ['idpel'], unique=True)
    op.create_index(op.f('ix_customers_2025_tarif'), 'customers_2025', ['tarif'], unique=False)
    op.create_index(op.f('ix_customers_2025_gardu'), 'customers_2025', ['gardu'], unique=False)
    op.create_index(op.f('ix_customers_2025_jenis'), 'customers_2025', ['jenis'], unique=False)
    op.create_index(op.f('ix_customers_2025_layanan'), 'customers_2025', ['layanan'], unique=False)
    op.create_index(op.f('ix_customers_2025_kd_proses'), 'customers_2025', ['kd_proses'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_customers_2025_kd_proses'), table_name='customers_2025')
    op.drop_index(op.f('ix_customers_2025_layanan'), table_name='customers_2025')
    op.drop_index(op.f('ix_customers_2025_jenis'), table_name='customers_2025')
    op.drop_index(op.f('ix_customers_2025_gardu'), table_name='customers_2025')
    op.drop_index(op.f('ix_customers_2025_tarif'), table_name='customers_2025')
    op.drop_index(op.f('ix_customers_2025_idpel'), table_name='customers_2025')
    op.drop_table('customers_2025')
    
    op.drop_index(op.f('ix_customers_2024_kd_proses'), table_name='customers_2024')
    op.drop_index(op.f('ix_customers_2024_layanan'), table_name='customers_2024')
    op.drop_index(op.f('ix_customers_2024_jenis'), table_name='customers_2024')
    op.drop_index(op.f('ix_customers_2024_gardu'), table_name='customers_2024')
    op.drop_index(op.f('ix_customers_2024_tarif'), table_name='customers_2024')
    op.drop_index(op.f('ix_customers_2024_idpel'), table_name='customers_2024')
    op.drop_table('customers_2024')

