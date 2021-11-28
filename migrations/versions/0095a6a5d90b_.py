"""empty message

Revision ID: 0095a6a5d90b
Revises: 79d55e9d850c
Create Date: 2021-11-28 22:31:14.136502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0095a6a5d90b'
down_revision = '79d55e9d850c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genre_title'), 'genre', ['title'], unique=True)
    op.create_table('mood',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mood_title'), 'mood', ['title'], unique=True)
    op.create_table('playlist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uri', sa.String(length=64), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('genre', sa.Integer(), nullable=True),
    sa.Column('mood', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['genre'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['mood'], ['mood.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_playlist_title'), 'playlist', ['title'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('passwordHash', sa.String(length=128), nullable=False),
    sa.Column('preferredGenre', sa.Integer(), nullable=True),
    sa.Column('commonMood', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commonMood'], ['mood.id'], ),
    sa.ForeignKeyConstraint(['preferredGenre'], ['genre.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('scores',
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('playlistid', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('moodid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['moodid'], ['mood.id'], ),
    sa.ForeignKeyConstraint(['playlistid'], ['playlist.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('userid', 'playlistid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scores')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_playlist_title'), table_name='playlist')
    op.drop_table('playlist')
    op.drop_index(op.f('ix_mood_title'), table_name='mood')
    op.drop_table('mood')
    op.drop_index(op.f('ix_genre_title'), table_name='genre')
    op.drop_table('genre')
    # ### end Alembic commands ###
