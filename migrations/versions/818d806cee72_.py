"""empty message

Revision ID: 818d806cee72
Revises: 02b1b74ed253
Create Date: 2023-06-02 09:45:45.023930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '818d806cee72'
down_revision = '02b1b74ed253'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.String(length=6), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('people')
    # ### end Alembic commands ###