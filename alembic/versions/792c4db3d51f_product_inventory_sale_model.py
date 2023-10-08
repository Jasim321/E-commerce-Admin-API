"""product_inventory_sale_model

Revision ID: 792c4db3d51f
Revises: 
Create Date: 2023-10-04 02:25:37.644407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '792c4db3d51f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), index=True),
        sa.Column('description', sa.String()),
        sa.Column('price', sa.Float()),
        sa.Column('image_url', sa.String(), index=True),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime())
    )

    op.create_table(
        'inventory',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id')),
        sa.Column('quantity', sa.Integer()),
        sa.Column('created_at', sa.DateTime())
    )

    op.create_table(
        'sales',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id')),
        sa.Column('sale_date', sa.DateTime()),
        sa.Column('sale_quantity', sa.Integer())
    )


def downgrade():
    op.drop_table('sales')
    op.drop_table('inventory')
    op.drop_table('products')
