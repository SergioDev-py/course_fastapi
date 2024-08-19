"""add content column to posts table

Revision ID: ef5bc443f776
Revises: e1d8a8c6464a
Create Date: 2024-08-13 14:32:36.037259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef5bc443f776'
down_revision: Union[str, None] = 'e1d8a8c6464a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String, nullable=False)
    )


def downgrade() -> None:
    op.drop_column(
        "posts",
        "content"
    )
