"""Dropped confidence column

Revision ID: b4a1109001bd
Revises: 440ada6979b9
Create Date: 2018-12-20 19:28:25.759022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4a1109001bd'
down_revision = '440ada6979b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("staff") as batch_op:
        batch_op.drop_column('confidence')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff', sa.Column('confidence', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
