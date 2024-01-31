"""create table transaction

Revision ID: e4b9ae4ced91
Revises: dd0b347f8395
Create Date: 2024-01-29 20:05:50.820118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4b9ae4ced91'
down_revision: Union[str, None] = 'dd0b347f8395'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('item_id', sa.Integer, nullable=False),
        sa.Column('customer_id', sa.Integer, nullable=False),

        sa.Column('date_come', sa.DateTime, nullable=False),
        sa.Column('date_out', sa.DateTime, nullable=True),
        sa.Column('cost_hourly', sa.Integer, nullable=False, default=0),
        sa.Column('cost_daily', sa.Integer, nullable=False, default=0),
        sa.Column('cost_final', sa.Integer, nullable=False, default=0),
        sa.Column('notes', sa.String(1024), nullable=True),
        sa.Column('plat_number', sa.String(512), nullable=True),
        sa.Column('status', sa.Enum("reserved", "taken"), nullable=False, default="reserved"),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.NOW(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.NOW(), onupdate=sa.func.NOW(), nullable=False),
    )

    op.create_foreign_key("fk_transaction_customer_id", 'transactions', 'customers',
                        ["customer_id"], ["id"], ondelete='CASCADE', onupdate='CASCADE')
    op.create_foreign_key("fk_transaction_item_id", 'transactions', 'items',
                        ["item_id"], ["id"], ondelete='CASCADE', onupdate='CASCADE')


def downgrade() -> None:
    op.drop_table('transactions')
