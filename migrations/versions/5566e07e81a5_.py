"""empty message

Revision ID: 5566e07e81a5
Revises: 3e6ebdc2b619
Create Date: 2022-09-20 02:49:32.568750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5566e07e81a5'
down_revision = '3e6ebdc2b619'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('hair_color', sa.String(length=120), nullable=False),
    sa.Column('eye_color', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('eye_color'),
    sa.UniqueConstraint('eye_color'),
    sa.UniqueConstraint('hair_color'),
    sa.UniqueConstraint('hair_color'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.add_column('favorites', sa.Column('people_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'favorites', 'people', ['people_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'favorites', type_='foreignkey')
    op.drop_column('favorites', 'people_id')
    op.drop_table('people')
    # ### end Alembic commands ###
