"""empty message

Revision ID: 1261ca08d027
Revises: 443a3c4c7e08
Create Date: 2025-03-06 14:14:18.683278

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '1261ca08d027'
down_revision = '443a3c4c7e08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_favorites',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('car_id', sa.Uuid(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_favorites_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_user_favorites')),
    )
    op.create_index(op.f('ix_user_favorites_id'), 'user_favorites', ['id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_favorites_id'), table_name='user_favorites')
    op.drop_table('user_favorites')
