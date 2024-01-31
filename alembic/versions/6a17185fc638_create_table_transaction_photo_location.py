"""create table transaction_photo_location

Revision ID: 6a17185fc638
Revises: e4b9ae4ced91
Create Date: 2024-01-29 20:15:33.501505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a17185fc638'
down_revision: Union[str, None] = 'e4b9ae4ced91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'transaction_photo_locations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('transaction_id', sa.Integer, nullable=False),

        sa.Column('title', sa.String(1024), nullable=False),
        sa.Column('url_photo', sa.String(1024), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )

    op.create_foreign_key("fk_transaction_photo_locations_customer_id", 'transaction_photo_locations', 'transactions',
                        ["transaction_id"], ["id"], ondelete='CASCADE', onupdate='CASCADE')


def downgrade() -> None:
    op.drop_table('transaction_photo_locations')
