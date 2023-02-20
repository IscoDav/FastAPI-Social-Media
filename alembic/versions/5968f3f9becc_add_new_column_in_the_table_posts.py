"""add new column in the table posts

Revision ID: 5968f3f9becc
Revises: 91b87d5a8149
Create Date: 2023-02-20 11:10:04.539378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5968f3f9becc'
down_revision = '91b87d5a8149'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
