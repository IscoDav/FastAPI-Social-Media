"""add user table

Revision ID: 08a0e2fdedfb
Revises: 5968f3f9becc
Create Date: 2023-02-20 11:37:18.433148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08a0e2fdedfb'
down_revision = '5968f3f9becc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
