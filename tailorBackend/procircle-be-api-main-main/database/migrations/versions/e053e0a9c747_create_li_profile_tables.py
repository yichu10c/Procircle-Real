"""add linkedin profile tables

Revision ID: 57a18c491093
Revises: 0048dbb62b9c
Create Date: 2025-07-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57a18c491093'
down_revision = '0048dbb62b9c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "linkedin_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("profile_data", sa.Text, nullable=False),
        sa.Column("job_types", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "linkedin_match_analysis",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "profile_id",
            sa.Integer,
            sa.ForeignKey("linkedin_profiles.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("result_asset_id", sa.Integer, nullable=True),
        sa.Column("status_code", sa.Integer, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("linkedin_match_analysis")
    op.drop_table("linkedin_profiles")
