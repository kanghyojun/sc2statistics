"""Add replay

Revision ID: 2545500d4934
Revises: None
Create Date: 2014-02-06 01:57:17.070198

"""
from alembic.op import create_table, drop_table
from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Unicode, UnicodeText

# revision identifiers, used by Alembic.
revision = '2545500d4934'
down_revision = None


def upgrade():
    create_table(
        'replays',
        Column('id', Unicode(), nullable=False),
        Column('build', UnicodeText(), nullable=False),
        Column('unit', UnicodeText(), nullable=False),
        Column('player', UnicodeText(), nullable=False),
        PrimaryKeyConstraint('id')
    )


def downgrade():
    drop_table('replays')
