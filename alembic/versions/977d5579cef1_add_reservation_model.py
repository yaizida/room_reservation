"""Add Reservation model

Revision ID: 977d5579cef1
Revises: 8c70a7a9db44
Create Date: 2024-02-20 12:39:14.353306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '977d5579cef1'
down_revision = '8c70a7a9db44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_reserve', sa.DateTime(), nullable=True),
    sa.Column('to_reserve', sa.DateTime(), nullable=True),
    sa.Column('meeting_room_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meeting_room_id'], ['meetingroom.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    # ### end Alembic commands ###
