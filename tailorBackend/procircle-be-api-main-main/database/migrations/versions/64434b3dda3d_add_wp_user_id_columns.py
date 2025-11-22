"""add wp_user_id columns

Revision ID: 64434b3dda3d
Revises: 57a18c491093
Create Date: 2025-07-24 14:08:10.016693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64434b3dda3d'
down_revision: Union[str, None] = '57a18c491093'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "linkedin_profiles",
        sa.Column("wp_user_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "linkedin_match_analysis",
        sa.Column("wp_user_id", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("linkedin_match_analysis", "wp_user_id")
    op.drop_column("linkedin_profiles", "wp_user_id")
