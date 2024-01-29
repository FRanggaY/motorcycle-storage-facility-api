"""create table customer

Revision ID: dd0b347f8395
Revises: 8ea76a6c6e80
Create Date: 2024-01-29 20:04:02.709850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd0b347f8395'
down_revision: Union[str, None] = '8ea76a6c6e80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(256), unique=True, nullable=False),
        sa.Column('no_hp', sa.String(256), unique=False, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('customers')
