"""initial schema

Revision ID: 5800d2420705
Revises: 
Create Date: 2017-01-19 20:54:03.697751

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5800d2420705'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qb_id', sa.String(), nullable=True),
    sa.Column('topic', sa.String(), nullable=False),
    sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('qb_id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
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
    op.create_table('user_subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('external_id', sa.String(length=128), nullable=True),
    sa.Column('mturk_worker_id', sa.String(length=128), nullable=False),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.Column('experiment_group', sa.String(length=128), nullable=True),
    sa.Column('data_string', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject_assignments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('mturk_assignment_id', sa.String(length=128), nullable=False),
    sa.Column('hit_id', sa.String(length=128), nullable=False),
    sa.Column('assignment_phase', sa.String(length=50), nullable=True),
    sa.Column('ua_raw', sa.String(length=255), nullable=True),
    sa.Column('ua_browser', sa.String(length=128), nullable=True),
    sa.Column('ua_browser_version', sa.String(length=128), nullable=True),
    sa.Column('ua_os', sa.String(length=128), nullable=True),
    sa.Column('ua_os_version', sa.String(length=128), nullable=True),
    sa.Column('ua_device', sa.String(length=128), nullable=True),
    sa.Column('skill_level', sa.String(length=50), nullable=True),
    sa.Column('education', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=50), nullable=True),
    sa.Column('english_level', sa.String(length=50), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('did_cheat', sa.Boolean(), nullable=True),
    sa.Column('did_timeout', sa.Boolean(), nullable=False),
    sa.Column('is_complete', sa.Boolean(), nullable=False),
    sa.Column('mturk_completion_code', sa.String(length=255), nullable=True),
    sa.Column('mturk_assignment_status', sa.String(length=100), nullable=True),
    sa.Column('mturk_assignment_status_date', sa.DateTime(), nullable=True),
    sa.Column('assignment_results', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('assignment_predictions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['user_subjects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assignment_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.Column('selection', sa.Integer(), nullable=False),
    sa.Column('credit', sa.Float(), nullable=False),
    sa.Column('user_response_time', sa.Float(), nullable=False),
    sa.Column('started_on', sa.DateTime(), nullable=False),
    sa.Column('completed_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['assignment_id'], ['subject_assignments.id'], ),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assignment_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['assignment_id'], ['subject_assignments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('assignment_sessions')
    op.drop_table('assignment_responses')
    op.drop_table('subject_assignments')
    op.drop_table('user_subjects')
    op.drop_table('roles_users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('exercises')
