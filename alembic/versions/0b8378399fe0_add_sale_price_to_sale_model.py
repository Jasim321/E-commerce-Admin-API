"""Add sale_price to Sale model

Revision ID: 0b8378399fe0
Revises: 37e0d3505967
Create Date: 2023-10-08 16:47:15.116642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0b8378399fe0'
down_revision: Union[str, None] = '37e0d3505967'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sales', sa.Column('sale_price', sa.Float, nullable=True))


def downgrade() -> None:
    op.drop_column('sales', 'sale_price')