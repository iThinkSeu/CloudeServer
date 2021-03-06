"""init migration

Revision ID: 2f645788654
Revises: None
Create Date: 2016-06-16 14:01:58.495000

"""

# revision identifiers, used by Alembic.
revision = '2f645788654'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('messuredatas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrumentid', sa.Integer(), nullable=True),
    sa.Column('datatype', sa.String(length=32), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['instrumentid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=32), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8mb4',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('messuredatas')
    op.drop_table('users')
    ### end Alembic commands ###
