"""last columns for posts

Revision ID: 378ba336b297
Revises: 45420b23392c
Create Date: 2023-02-20 12:14:02.958520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '378ba336b297'
down_revision = '45420b23392c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        "published", sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False,
        server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
