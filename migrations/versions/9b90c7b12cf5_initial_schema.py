"""initial schema

Revision ID: 9b90c7b12cf5
Revises: 
Create Date: 2016-10-05 14:15:38.915653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b90c7b12cf5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.String(length=128), nullable=True),
    sa.Column('assignment_id', sa.String(length=128), nullable=False),
    sa.Column('worker_id', sa.String(length=128), nullable=False),
    sa.Column('hit_id', sa.String(length=128), nullable=False),
    sa.Column('ua_raw', sa.String(length=128), nullable=True),
    sa.Column('ua_browser', sa.String(length=128), nullable=True),
    sa.Column('ua_browser_version', sa.String(length=128), nullable=True),
    sa.Column('ua_os', sa.String(length=128), nullable=True),
    sa.Column('ua_os_version', sa.String(length=128), nullable=True),
    sa.Column('ua_device', sa.String(length=128), nullable=True),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.Column('experiment_group', sa.String(length=128), nullable=True),
    sa.Column('data_string', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('completion_code', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('assignment_id', 'worker_id', name='worker_id_assignment_id_uix')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=100), nullable=True),
    sa.Column('current_login_ip', sa.String(length=100), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )


def downgrade():
    op.drop_table('roles_users')
    op.drop_table('users')
    op.drop_table('subjects')
    op.drop_table('roles')
