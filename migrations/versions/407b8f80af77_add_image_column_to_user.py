"""Add image column to user

Revision ID: 407b8f80af77
Revises: a565ea52cf5e
Create Date: 2020-06-08 14:48:52.353404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '407b8f80af77'
down_revision = 'a565ea52cf5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_file', sa.String(length=20), nullable=True))
        batch_op.execute("UPDATE user SET image_file = 0")
        batch_op.alter_column('image_file', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('image_file')

    # ### end Alembic commands ###
