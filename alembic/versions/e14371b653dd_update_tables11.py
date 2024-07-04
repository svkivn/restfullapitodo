"""update tables11

Revision ID: e14371b653dd
Revises: 56a5d8c3fcfb
Create Date: 2024-07-04 13:52:19.106299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e14371b653dd'
down_revision: Union[str, None] = '56a5d8c3fcfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'complete2')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'complete2')
    # ### end Alembic commands ###
