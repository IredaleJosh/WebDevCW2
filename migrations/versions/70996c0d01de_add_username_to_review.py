"""add username to Review

Revision ID: 70996c0d01de
Revises: 4207f6714223
Create Date: 2024-12-09 23:32:24.035372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70996c0d01de'
down_revision = '4207f6714223'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=15), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Review', schema=None) as batch_op:
        batch_op.drop_column('username')

    # ### end Alembic commands ###
