"""add new column

Revision ID: 0391fa619e59
Revises: 9942db353e76
Create Date: 2025-05-18 18:46:22.225862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0391fa619e59'
down_revision = '9942db353e76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
