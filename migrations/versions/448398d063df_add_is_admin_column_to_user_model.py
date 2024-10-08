"""Add is_admin column to User model

Revision ID: 448398d063df
Revises: aa73d302fca5
Create Date: 2024-08-02 09:47:35.698986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '448398d063df'
down_revision = 'aa73d302fca5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
