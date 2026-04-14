"""Add link_imagem to produtos and media_avaliacoes to produtos and pedidos

Revision ID: 002
Revises: 001
Create Date: 2026-04-13 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add link_imagem column to produtos
    op.add_column('produtos', sa.Column('link_imagem', sa.String(500), nullable=True))
    
    # Add media_avaliacoes column to produtos
    op.add_column('produtos', sa.Column('media_avaliacoes', sa.Float, nullable=True))
    
    # Add media_avaliacoes column to pedidos
    op.add_column('pedidos', sa.Column('media_avaliacoes', sa.Float, nullable=True))


def downgrade() -> None:
    # Remove media_avaliacoes column from pedidos
    op.drop_column('pedidos', 'media_avaliacoes')
    
    # Remove media_avaliacoes column from produtos
    op.drop_column('produtos', 'media_avaliacoes')
    
    # Remove link_imagem column from produtos
    op.drop_column('produtos', 'link_imagem')
