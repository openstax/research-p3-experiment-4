"""added completed_on to assignment table

Revision ID: 1cead0dd8c2b
Revises: e39a9595a3fb
Create Date: 2017-07-24 16:00:19.423645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cead0dd8c2b'
down_revision = 'e39a9595a3fb'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subject_assignments', sa.Column('completed_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subject_assignments', 'completed_on')
    # ### end Alembic commands ###
