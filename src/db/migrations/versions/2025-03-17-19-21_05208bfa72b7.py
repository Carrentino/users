"""empty message

Revision ID: 05208bfa72b7
Revises: 1261ca08d027
Create Date: 2025-03-17 19:21:49.960285

"""

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import ImageType


# revision identifiers, used by Alembic.
revision = '05208bfa72b7'
down_revision = '1261ca08d027'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('score', sa.Numeric(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'score')
    # ### end Alembic commands ###
