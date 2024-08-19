"""Add last few columns to posts table

Revision ID: f630c8f1eb76
Revises: 34bc83858f28
Create Date: 2024-08-13 14:51:49.423465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f630c8f1eb76'
down_revision: Union[str, None] = '34bc83858f28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE")
    )
    op.add_column(
        "posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )


def downgrade() -> None:
    op.drop_column(
        "posts",
        "published"
    )
    op.drop_column(
        "posts",
        "created_at"
    )