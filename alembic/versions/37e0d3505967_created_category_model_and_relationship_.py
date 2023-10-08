"""created_category_model_and_relationship_with_product_model

Revision ID: 37e0d3505967
Revises: 792c4db3d51f
Create Date: 2023-10-05 03:19:52.935896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '37e0d3505967'
down_revision: Union[str, None] = '792c4db3d51f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('products', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_products_category_id',
        'products',
        'categories',
        ['category_id'],
        ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_table('categories')
    op.drop_column('products', 'category_id')
    op.drop_constraint('fk_products_category_id', 'products', type_='foreignkey')
