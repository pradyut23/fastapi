"""add foreign key to posts table

Revision ID: f78287e91fd7
Revises: ae6b56778ec7
Create Date: 2022-01-11 13:56:02.783019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic. 
revision = 'f78287e91fd7'
down_revision = 'ae6b56778ec7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', 
        local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
