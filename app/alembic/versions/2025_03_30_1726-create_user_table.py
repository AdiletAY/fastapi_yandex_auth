"""create_user_table

Revision ID: d3b918c9779e
Revises:
Create Date: 2025-03-30 17:26:05.346863

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "d3b918c9779e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("yandex_id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("yandex_id", name=op.f("uq_users_yandex_id")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
