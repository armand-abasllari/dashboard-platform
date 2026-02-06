from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "2db35658ab43"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "snapshots",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("service", sa.Text(), nullable=False),
        sa.Column("metric", sa.Text(), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column(
            "collected_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_snapshots_service_metric_time",
        "snapshots",
        ["service", "metric", "collected_at"],
    )


def downgrade():
    op.drop_index("ix_snapshots_service_metric_time", table_name="snapshots")
    op.drop_table("snapshots")
