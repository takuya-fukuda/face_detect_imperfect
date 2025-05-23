"""add new column

Revision ID: 22f30b71072b
Revises: b7c99dc4259f
Create Date: 2025-05-18 19:31:32.708614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '22f30b71072b'
down_revision = 'b7c99dc4259f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
