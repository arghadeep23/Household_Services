"""Add service_id to Professional

Revision ID: 4cc5a88d1748
Revises: 
Create Date: 2024-11-26 02:49:58.915045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '4cc5a88d1748'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('professionals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_professional_service', 'services', ['service_id'], ['id'])

def downgrade():
    with op.batch_alter_table('professionals', schema=None) as batch_op:
        batch_op.drop_constraint('fk_professional_service', type_='foreignkey')
        batch_op.drop_column('service_id')