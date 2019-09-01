"""invert the function of track_data_conflicts to untrack_data_conflicts

Revision ID: 29d545c18474
Revises: 62783e6332b6
Create Date: 2019-09-01 18:35:41.012986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d545c18474'
down_revision = '62783e6332b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('form', sa.Column('untrack_data_conflicts', sa.Boolean(), nullable=False, server_default='f'))

    # ----- data migration -----
    connection = op.get_bind()
    q = sa.sql.text('''
        UPDATE form SET untrack_data_conflicts = NOT track_data_conflicts;
    ''')
    connection.execute(q)
    # ----- data migration -----

    op.drop_column('form', 'track_data_conflicts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('form', sa.Column('track_data_conflicts', sa.BOOLEAN(), nullable=False, server_default='t'))

    # ----- data migration -----
    connection = op.get_bind()
    q = sa.sql.text('''
        UPDATE form SET track_data_conflicts = NOT untrack_data_conflicts;
    ''')
    connection.execute(q)
    # ----- data migration -----

    op.drop_column('form', 'untrack_data_conflicts')
    # ### end Alembic commands ###
