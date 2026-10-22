"""add payment fields to booking_requests

Revision ID: a1c4e7b92d10
Revises: 386925d4e7fc
Create Date: 2026-10-22 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1c4e7b92d10'
down_revision = '386925d4e7fc'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('booking_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.add_column(sa.Column('currency', sa.String(length=8), nullable=True))
        batch_op.add_column(sa.Column('tx_ref', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('payment_status', sa.String(length=16), nullable=True))
        batch_op.add_column(sa.Column('flw_transaction_id', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('paid_at', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_booking_requests_tx_ref'), ['tx_ref'], unique=True)
        batch_op.create_index(batch_op.f('ix_booking_requests_payment_status'), ['payment_status'], unique=False)

    op.execute("UPDATE booking_requests SET payment_status = 'unpaid' WHERE payment_status IS NULL")


def downgrade():
    with op.batch_alter_table('booking_requests', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_booking_requests_payment_status'))
        batch_op.drop_index(batch_op.f('ix_booking_requests_tx_ref'))
        batch_op.drop_column('paid_at')
        batch_op.drop_column('flw_transaction_id')
        batch_op.drop_column('payment_status')
        batch_op.drop_column('tx_ref')
        batch_op.drop_column('currency')
        batch_op.drop_column('amount')
