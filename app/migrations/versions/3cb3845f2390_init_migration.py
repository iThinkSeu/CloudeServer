"""init migration

Revision ID: 3cb3845f2390
Revises: 50686f5a051a
Create Date: 2017-03-16 14:11:22.684000

"""

# revision identifiers, used by Alembic.
revision = '3cb3845f2390'
down_revision = '50686f5a051a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
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
    sa.Column('fre', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['instrumentID'], ['instruments.instrumentID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messuredatas')
    ### end Alembic commands ###