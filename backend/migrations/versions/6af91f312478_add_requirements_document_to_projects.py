"""add requirements document to projects

Revision ID: 6af91f312478
Revises: b9ee32e26bf5
Create Date: 2026-08-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6af91f312478"
down_revision: Union[str, Sequence[str], None] = "b9ee32e26bf5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "projects",
        sa.Column(
            "requirements_document",
            sa.JSON(),
            nullable=True,
        ),
    )

    # Initialize the new field for all existing projects.
    op.execute(
        """
        UPDATE projects
        SET requirements_document = '{}'::json
        WHERE requirements_document IS NULL
        """
    )

    # Make the field required after existing rows have been initialized.
    op.alter_column(
        "projects",
        "requirements_document",
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column(
        "projects",
        "requirements_document",
    )