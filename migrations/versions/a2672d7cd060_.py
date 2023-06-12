"""empty message

Revision ID: a2672d7cd060
Revises: 
Create Date: 2023-06-12 14:45:10.390841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2672d7cd060'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Todos', schema=None) as batch_op:
        batch_op.alter_column('completed',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Todos', schema=None) as batch_op:
        batch_op.alter_column('completed',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###