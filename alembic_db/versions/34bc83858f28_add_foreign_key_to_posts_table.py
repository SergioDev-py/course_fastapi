"""Add foreign key to posts table

Revision ID: 34bc83858f28
Revises: 6a75cecd2109
Create Date: 2024-08-13 14:45:02.773532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34bc83858f28'
down_revision: Union[str, None] = '6a75cecd2109'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer, nullable=False)
    )
    op.create_foreign_key(
        "posts_users_key",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_key", table_name="posts")
    op.drop_column("posts", "owner_id")
