"""empty message

Revision ID: b527cd9542af
Revises: d816f7eb47d1
Create Date: 2021-11-30 11:23:45.221041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b527cd9542af'
down_revision = 'd816f7eb47d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('playlistid', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('moodid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['moodid'], ['mood.id'], ),
    sa.ForeignKeyConstraint(['playlistid'], ['playlist.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('userid', 'playlistid')
    )
    op.drop_table('scores')
    op.add_column('playlist', sa.Column('genreid', sa.Integer(), nullable=True))
    op.add_column('playlist', sa.Column('moodid', sa.Integer(), nullable=True))
    op.drop_constraint('playlist_genre_fkey', 'playlist', type_='foreignkey')
    op.drop_constraint('playlist_mood_fkey', 'playlist', type_='foreignkey')
    op.create_foreign_key(None, 'playlist', 'genre', ['genreid'], ['id'])
    op.create_foreign_key(None, 'playlist', 'mood', ['moodid'], ['id'])
    op.drop_column('playlist', 'mood')
    op.drop_column('playlist', 'genre')
    op.add_column('user', sa.Column('preferredGenreid', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('commonMoodid', sa.Integer(), nullable=True))
    op.drop_constraint('user_commonMood_fkey', 'user', type_='foreignkey')
    op.drop_constraint('user_preferredGenre_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'mood', ['commonMoodid'], ['id'])
    op.create_foreign_key(None, 'user', 'genre', ['preferredGenreid'], ['id'])
    op.drop_column('user', 'commonMood')
    op.drop_column('user', 'preferredGenre')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('preferredGenre', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('commonMood', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_preferredGenre_fkey', 'user', 'genre', ['preferredGenre'], ['id'])
    op.create_foreign_key('user_commonMood_fkey', 'user', 'mood', ['commonMood'], ['id'])
    op.drop_column('user', 'commonMoodid')
    op.drop_column('user', 'preferredGenreid')
    op.add_column('playlist', sa.Column('genre', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('playlist', sa.Column('mood', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'playlist', type_='foreignkey')
    op.drop_constraint(None, 'playlist', type_='foreignkey')
    op.create_foreign_key('playlist_mood_fkey', 'playlist', 'mood', ['mood'], ['id'])
    op.create_foreign_key('playlist_genre_fkey', 'playlist', 'genre', ['genre'], ['id'])
    op.drop_column('playlist', 'moodid')
    op.drop_column('playlist', 'genreid')
    op.create_table('scores',
    sa.Column('userid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('playlistid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('moodid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['moodid'], ['mood.id'], name='scores_moodid_fkey'),
    sa.ForeignKeyConstraint(['playlistid'], ['playlist.id'], name='scores_playlistid_fkey'),
    sa.ForeignKeyConstraint(['userid'], ['user.id'], name='scores_userid_fkey'),
    sa.PrimaryKeyConstraint('userid', 'playlistid', name='scores_pkey')
    )
    op.drop_table('score')
    # ### end Alembic commands ###
