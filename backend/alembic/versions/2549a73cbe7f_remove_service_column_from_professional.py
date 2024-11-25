"""Remove service column from Professional

Revision ID: 2549a73cbe7f
Revises: 4cc5a88d1748
Create Date: 2024-11-26 03:12:39.198014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '2549a73cbe7f'
down_revision: Union[str, None] = '4cc5a88d1748'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('professionals', schema=None) as batch_op:
        batch_op.drop_column('service')

def downgrade():
    with op.batch_alter_table('professionals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service', sa.String(), nullable=False))
    # ### end Alembic commands ###
