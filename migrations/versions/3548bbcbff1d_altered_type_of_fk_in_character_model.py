"""altered type of fk in character model

Revision ID: 3548bbcbff1d
Revises: 8d3678976a5b
Create Date: 2023-10-22 17:38:20.621148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3548bbcbff1d'
down_revision = '8d3678976a5b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character', sa.Column('room_fk', sa.Integer(), nullable=False))
    op.drop_constraint('fk_character_room_id_room', 'character', type_='foreignkey')
    op.create_foreign_key(op.f('fk_character_room_fk_room'), 'character', 'room', ['room_fk'], ['id'])
    op.drop_column('character', 'room_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character', sa.Column('room_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk_character_room_fk_room'), 'character', type_='foreignkey')
    op.create_foreign_key('fk_character_room_id_room', 'character', 'room', ['room_id'], ['id'], ondelete='CASCADE')
    op.drop_column('character', 'room_fk')
    # ### end Alembic commands ###
