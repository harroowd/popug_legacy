"""001_added_users

Revision ID: ece12439f1f2
Revises:
Create Date: 2023-09-20 00:40:14.216162

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ece12439f1f2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "CUSTOMER", "MARKET", "COURIER", "ADMIN", name="userroles"
            ),
            server_default=sa.text("'CUSTOMER'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###