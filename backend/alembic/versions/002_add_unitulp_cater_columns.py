"""Add penyulang (Unit ULP) and cater columns

Revision ID: 002_add_unitulp_cater
Revises: 001_initial_migration
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_unitulp_cater'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add penyulang and cater columns to customers_2024
    op.add_column('customers_2024', sa.Column('penyulang', sa.String(), nullable=True))
    op.add_column('customers_2024', sa.Column('cater', sa.String(), nullable=True))
    op.create_index(op.f('ix_customers_2024_penyulang'), 'customers_2024', ['penyulang'], unique=False)
    op.create_index(op.f('ix_customers_2024_unitup'), 'customers_2024', ['unitup'], unique=False)
    
    # Add penyulang and cater columns to customers_2025
    op.add_column('customers_2025', sa.Column('penyulang', sa.String(), nullable=True))
    op.add_column('customers_2025', sa.Column('cater', sa.String(), nullable=True))
    op.create_index(op.f('ix_customers_2025_penyulang'), 'customers_2025', ['penyulang'], unique=False)
    op.create_index(op.f('ix_customers_2025_unitup'), 'customers_2025', ['unitup'], unique=False)


def downgrade():
    # Remove indexes
    op.drop_index(op.f('ix_customers_2025_unitup'), table_name='customers_2025')
    op.drop_index(op.f('ix_customers_2025_penyulang'), table_name='customers_2025')
    op.drop_index(op.f('ix_customers_2024_unitup'), table_name='customers_2024')
    op.drop_index(op.f('ix_customers_2024_penyulang'), table_name='customers_2024')
    
    # Remove columns from customers_2025
    op.drop_column('customers_2025', 'cater')
    op.drop_column('customers_2025', 'penyulang')
    
    # Remove columns from customers_2024
    op.drop_column('customers_2024', 'cater')
    op.drop_column('customers_2024', 'penyulang')

