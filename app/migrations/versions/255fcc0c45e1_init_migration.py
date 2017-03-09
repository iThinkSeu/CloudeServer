"""init migration

Revision ID: 255fcc0c45e1
Revises: 246ff8d13f22
Create Date: 2017-03-09 22:24:35.960000

"""

# revision identifiers, used by Alembic.
revision = '255fcc0c45e1'
down_revision = '246ff8d13f22'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messuredatas', sa.Column('separation', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messuredatas', 'separation')
    ### end Alembic commands ###
