"""add other participant names

Revision ID: 17e9d721d8cc
Revises: d29306ab0e6a
Create Date: 2019-08-19 18:10:27.739621

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '17e9d721d8cc'
down_revision = 'd29306ab0e6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('participant', 'name_translations', new_column_name='full_name_translations')
    op.add_column('participant', sa.Column('first_name_translations', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('participant', sa.Column('last_name_translations', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('participant', sa.Column('other_names_translations', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('participant', 'full_name_translations', new_column_name='name_translations')
    op.drop_column('participant', 'other_names_translations')
    op.drop_column('participant', 'last_name_translations')
    op.drop_column('participant', 'first_name_translations')
    # ### end Alembic commands ###