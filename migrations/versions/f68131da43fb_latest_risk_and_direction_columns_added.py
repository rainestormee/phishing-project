"""latest_risk and direction columns added

Revision ID: f68131da43fb
Revises: 715d63f3b96c
Create Date: 2018-12-24 17:46:10.537344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f68131da43fb'
down_revision = '715d63f3b96c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff', sa.Column('direction', sa.Boolean(), nullable=True))
    op.add_column('staff', sa.Column('latest_risk', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staff', 'latest_risk')
    op.drop_column('staff', 'direction')
    # ### end Alembic commands ###
