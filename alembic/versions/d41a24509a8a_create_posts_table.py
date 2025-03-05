"""create posts table

Revision ID: d41a24509a8a
Revises:
Create Date: 2025-03-04 15:04:56.993775

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d41a24509a8a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("posts")
