"""Initial migration

Revision ID: 9adaf9016776
Revises: 
Create Date: 2024-07-29 16:42:37.096962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9adaf9016776'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Check if index exists before dropping it
    conn = op.get_bind()
    if conn.dialect.has_table(conn, 'articles'):
        existing_indexes = conn.execute(
            "SELECT indexname FROM pg_indexes WHERE tablename = 'articles'"
        ).fetchall()
        index_names = [index[0] for index in existing_indexes]
        if 'ix_articles_id' in index_names:
            op.drop_index('ix_articles_id', table_name='articles')

    op.add_column('users', sa.Column('disabled', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('users', 'disabled')
    # Recreate the index if needed
    op.create_index('ix_articles_id', 'articles', ['id'])
