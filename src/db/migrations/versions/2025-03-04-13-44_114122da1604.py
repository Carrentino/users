"""empty message

Revision ID: 114122da1604
Revises:
Create Date: 2025-03-04 13:44:57.112977

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '114122da1604'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column(
            'status',
            sa.Enum('NOT_REGISTERED', 'NOT_VERIFIED', 'VERIFIED', 'SUSPECTED', 'BANNED', name='userstatus'),
            nullable=False,
        ),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('email', name=op.f('uq_users_email')),
        sa.UniqueConstraint('phone_number', name=op.f('uq_users_phone_number')),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
