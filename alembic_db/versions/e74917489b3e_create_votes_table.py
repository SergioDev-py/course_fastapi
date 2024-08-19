"""create votes table

Revision ID: e74917489b3e
Revises: f630c8f1eb76
Create Date: 2024-08-13 15:14:41.988850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e74917489b3e'
down_revision: Union[str, None] = 'f630c8f1eb76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("post_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id")
    )


def downgrade() -> None:
    op.drop_table(
        "votes"
    )
