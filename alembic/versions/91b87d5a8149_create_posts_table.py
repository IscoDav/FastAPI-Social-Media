"""create posts table

Revision ID: 91b87d5a8149
Revises: 
Create Date: 2023-02-13 18:57:34.668087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91b87d5a8149'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable =False,
                    primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
