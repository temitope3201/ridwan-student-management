"""Added email to the User table

Revision ID: 8df275bff343
Revises: 
Create Date: 2023-03-12 12:14:00.514657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8df275bff343'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=30), nullable=False))
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_code', sa.String(), nullable=False))
        batch_op.create_unique_constraint(None, ['course_code'])

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=30), nullable=False))
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('email')

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('course_code')

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
