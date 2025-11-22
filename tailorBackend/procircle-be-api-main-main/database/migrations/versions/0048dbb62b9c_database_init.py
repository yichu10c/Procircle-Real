
"""database init"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0048dbb62b9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "linkedin_jobs",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("job_id", sa.Text),
        sa.Column("job_title", sa.Text),
        sa.Column("job_linkedin_url", sa.Text),
        sa.Column("company_name", sa.Text),
        sa.Column("company_link", sa.Text),
        sa.Column("date_of_listing", sa.Text),
        sa.Column("job_description", sa.Text),
        sa.Column("seniority_level", sa.Text),
        sa.Column("employment_type", sa.Text),
        sa.Column("job_function", sa.Text),
        sa.Column("industries", sa.Text),
        sa.Column("location", sa.Text),
        sa.Column("logo", sa.Text),
    )

    op.create_table(
        "guest_user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(256), nullable=True),
        sa.Column("resume_id", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "asset",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("url", sa.String(2048), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "user_asset",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("guest_user.id")),
        sa.Column("asset_id", sa.Integer, sa.ForeignKey("asset.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "job_worker_task",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("task_type", sa.String(100), nullable=False),
        sa.Column("status", sa.String(100), nullable=False),
        sa.Column("metadata", sa.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "job_match",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("guest_user.id")),
        sa.Column("job_id", sa.BigInteger, sa.ForeignKey("linkedin_jobs.id")),
        sa.Column("resume_id", sa.Integer, sa.ForeignKey("asset.id")),
        sa.Column("job_desc_id", sa.Integer, sa.ForeignKey("asset.id")),
        sa.Column("job_title", sa.String(256), nullable=True),
        sa.Column("job_desc_text", sa.Text, nullable=True),
        sa.Column("score", sa.Float, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "job_match_analysis",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("guest_user.id")),
        sa.Column("job_id", sa.BigInteger, sa.ForeignKey("linkedin_jobs.id")),
        sa.Column("job_title", sa.String(256), nullable=True),
        sa.Column("resume_id", sa.Integer, sa.ForeignKey("asset.id")),
        sa.Column("job_desc_id", sa.Integer, sa.ForeignKey("asset.id")),
        sa.Column("result", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

def downgrade():

    op.drop_table("job_match_analysis")
    op.drop_table("job_match")
    op.drop_table("job_worker_task")
    op.drop_table("logs")
    op.drop_table("user_asset")
    op.drop_table("asset")
    op.drop_table("guest_user")
    op.drop_table("linkedin_jobs")