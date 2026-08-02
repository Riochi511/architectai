"""add discovery memory to projects

Revision ID: b9ee32e26bf5
Revises: ef9bcbac58f6
Create Date: 2026-08-01 19:19:04.203656
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9ee32e26bf5"
down_revision: Union[str, Sequence[str], None] = "ef9bcbac58f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "projects",
        sa.Column(
            "discovery_stage",
            sa.String(length=50),
            nullable=False,
            server_default="vision",
        ),
    )

    op.add_column(
        "projects",
        sa.Column(
            "discovery_memory",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'"),
        ),
    )

    op.add_column(
        "projects",
        sa.Column(
            "discovery_confidence",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade() -> None:
    op.drop_column("projects", "discovery_confidence")
    op.drop_column("projects", "discovery_memory")
    op.drop_column("projects", "discovery_stage")