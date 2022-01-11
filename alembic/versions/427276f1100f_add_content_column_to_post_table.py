"""add content column to post table

Revision ID: 427276f1100f
Revises: 17b3c946ee66
Create Date: 2022-01-11 13:44:23.738773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '427276f1100f'
down_revision = '17b3c946ee66'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
