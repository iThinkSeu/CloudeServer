"""init migration

Revision ID: 2c66cda35855
Revises: None
Create Date: 2017-03-15 14:24:06.522000

"""

# revision identifiers, used by Alembic.
revision = '2c66cda35855'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrumentID', sa.String(length=32), nullable=True),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('realvalue', sa.Float(), nullable=True),
    sa.Column('measurevalue', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('manageinstruments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('instrumentid', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['instrumentid'], ['instruments.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'userid', 'instrumentid')
    )
    op.create_table('messuredatas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrumentID', sa.String(length=32), nullable=True),
    sa.Column('datatype', sa.String(length=32), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('separation', sa.String(length=32), nullable=True),
    sa.Column('VWRTHD', sa.String(length=32), nullable=True),
    sa.Column('stand', sa.Float(), nullable=True),
    sa.Column('up', sa.Float(), nullable=True),
    sa.Column('down', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['instrumentID'], ['instruments.instrumentID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messuredatas')
    op.drop_table('manageinstruments')
    op.drop_table('users')
    op.drop_table('revises')
    ### end Alembic commands ###