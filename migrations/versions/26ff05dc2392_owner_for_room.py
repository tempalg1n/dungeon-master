"""owner for room

Revision ID: 26ff05dc2392
Revises: c17cf896091a
Create Date: 2023-10-21 22:35:28.869182

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '26ff05dc2392'
down_revision = 'c17cf896091a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('character', 'adventure')
    op.add_column('room', sa.Column('owner', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_room_owner_user'), 'room', 'user', ['owner'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_room_owner_user'), 'room', type_='foreignkey')
    op.drop_column('room', 'owner')
    op.add_column('character', sa.Column('adventure', postgresql.ENUM('AI', 'EGW', 'ERLW', 'EEPC', 'GGR', 'LR', 'MOT', 'MTF', 'OGA', 'PHB', 'SCAG', 'VGM', 'TCE', 'TTP', name='adventure'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
