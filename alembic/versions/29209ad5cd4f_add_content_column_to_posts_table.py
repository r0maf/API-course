"""add content column to posts table

Revision ID: 29209ad5cd4f
Revises: d41a24509a8a
Create Date: 2025-03-04 15:15:52.252013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29209ad5cd4f'
down_revision: Union[str, None] = 'd41a24509a8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
