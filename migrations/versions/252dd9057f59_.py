"""empty message

Revision ID: 252dd9057f59
Revises: f8c212160b6b
Create Date: 2023-06-03 13:24:36.818718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '252dd9057f59'
down_revision = 'f8c212160b6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fav_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fav_planets')
    # ### end Alembic commands ###