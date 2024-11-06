"""Added average_speed to ACTIVITIES table

Revision ID: f6100d1dcb4b
Revises: 
Create Date: 2024-11-06 13:30:43.755889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6100d1dcb4b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('average_speed', sa.Float()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activity', 'average_speed')
    # ### end Alembic commands ###
