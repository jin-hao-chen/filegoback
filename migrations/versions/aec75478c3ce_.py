"""empty message

Revision ID: aec75478c3ce
Revises: 
Create Date: 2019-10-08 17:31:35.108425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aec75478c3ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('is_current', sa.Boolean(), nullable=True),
    sa.Column('expire_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sid', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sid')
    )
    op.create_table('file',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(length=80), nullable=False),
    sa.Column('upload_time', sa.DateTime(), nullable=True),
    sa.Column('size', sa.Float(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('sid', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['sid'], ['student.sid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    op.drop_table('student')
    op.drop_table('category')
    # ### end Alembic commands ###