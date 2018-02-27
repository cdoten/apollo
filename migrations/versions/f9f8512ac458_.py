"""empty message

Revision ID: f9f8512ac458
Revises: cee9b42e2c0a
Create Date: 2018-02-22 14:30:18.615986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9f8512ac458'
down_revision = 'cee9b42e2c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant', sa.Column('location_id', sa.Integer(), nullable=True))
    op.add_column('participant', sa.Column('participant_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'participant', 'location', ['location_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'participant', type_='foreignkey')
    op.drop_column('participant', 'participant_id')
    op.drop_column('participant', 'location_id')
    # ### end Alembic commands ###