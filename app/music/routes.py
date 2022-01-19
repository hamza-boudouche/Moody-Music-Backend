from app.music import bp
from flask import request
from app import db
from app.models import Genre, Mood, Playlist, User, Score
from app.utils import auth, validate, COOKIE_NAME, DEFAULT_COUNT, moodToNum
from app.utils import mail
import logging


@bp.route("/<uri>", methods=["GET"])
def getMusicByUri(uri):
    # tested
    # added to api documentation
    logging.info(f"request: GET /music/{uri}")
    playlist = Playlist.query.filter_by(uri=uri).first()
    if playlist is None:
        return {"success": False, "message": "playlist not found"}, 404
    return {"success": True, "playlist": playlist.toDict()}


@bp.route("/rec/<moodid>", methods=["GET"])
def getMusic(moodid: str):
    logging.info(f"request: GET /music/rec/{moodid}")
    moodid = moodToNum(moodid)
    # TODO: implement this
    mood = Mood.query.filter_by(id=moodid).first()
    if mood is None:
        return {"success": False, "message": "mood not found (invalid moodid)"}, 404
    playlists = Playlist.query.filter_by(mood=mood).limit(DEFAULT_COUNT).all()
    token = request.cookies.get(COOKIE_NAME)
    user = auth.Token.verify(token)
    if user is None:
        playlistDict = [playlist.toDict() for playlist in playlists]
        return {"success": True, "playlists": playlistDict}
    if not auth.Token.verify_blacklist(token):
        user = User.query.filter_by(username=user.get("username")).first()
        num_of_owned_by = 0
        for idx, playlist in enumerate(playlists):
            if playlist.owner is not None and playlist.user == user:
                num_of_owned_by += 1
                for i in range(idx):
                    playlists[i + 1] = playlists[i]
                playlists.insert(0, playlist)
        for idx, playlist in enumerate(playlists):
            score = Score.query.filter_by(
                uri=playlist.uri, user=playlist.user
            ).first()  # does this work ?!
            if score is None:
                continue
            if score.score == 1:
                for i in range(num_of_owned_by, idx):
                    playlists[i + 1] = playlists[i]
                playlists.insert(num_of_owned_by, playlist)
            if score.score == -1:
                for i in range(idx + 1, len(playlists)):
                    playlists[i - 1] = playlists[i]
                playlists.append(playlist)
        playlistDict = [playlist.toDict() for playlist in playlists]
        return {"success": True, "playlists": playlistDict}


@bp.route("/genre", methods=["GET"])
def getGenres():
    # TODO: implement This
    logging.info(f"request: GET /music/genre")
    genres = Genre.query.all()
    return {"success": True, "genres": genres}


@bp.route("/mood", methods=["GET"])
def getMoods():
    # TODO: implement This
    logging.info(f"request: GET /music/mood")
    moods = Mood.query.all()
    return {"success": True, "moods": moods}


@bp.route("/add", methods=["POST"])
def addMusic():
    # tested
    logging.info(f"request: POST /music/add - {request.get_json()}")
    # FIXME: verify if uri is already in database or not (http code 409)
    # added to api documentation
    # authentication
    token = request.cookies.get(COOKIE_NAME)
    if not auth.Token.verify_blacklist(token):
        return {"success": False, "message": "invalid authorization cookie"}, 403
    user = auth.Token.verify(token)
    if user is None:
        return {"success": False, "message": "invalid authorization cookie"}, 403
    # authorization
    content = request.get_json()
    if content.get("username") is None:
        return {"success": False, "message": "missing username"}, 422
    if content.get("username") != user.get("username"):
        # unauthorized operation
        return {"success": False, "message": "invalid authorization cookie"}, 403
    # processing request
    content = request.get_json()
    if (
        content.get("uri") is None
        or content.get("title") is None
        or content.get("genreid") is None
        or content.get("moodid") is None
    ):
        return {
            "success": False,
            "message": "missing uri, title, genreid, and/or moodid",
        }, 422
    if not validate.validate_link(
        "https://open.spotify.com/" + content.get("uri").strip()
    ):
        return {"success": False, "message": "invalid uri"}, 400
    genre = Genre.query.filter_by(id=content.get("genreid")).first()
    if Playlist.query.filter_by(uri=content.get("uri")).count() != 0:
        return {
            "success": False,
            "message": "invalid uri (already bound to another playlist instance)",
        }, 409
    if genre is None:
        return {"success": False, "message": "genre not found (invalid genreid)"}, 404
    mood = Mood.query.filter_by(id=content.get("moodid")).first()
    if mood is None:
        return {"success": False, "message": "mood not found (invalid moodid)"}, 404
    user = User.query.filter_by(username=content.get("username")).first()
    return user.add(
        uri=content.get("uri"), title=content.get("title"), genre=genre, mood=mood
    )


@bp.route("/vote", methods=["PUT"])
def vote():
    # tested
    logging.info(f"request: PUT /music/vote - {request.get_json()}")
    # authentication
    # added to api documentation
    token = request.cookies.get(COOKIE_NAME)
    if not auth.Token.verify_blacklist(token):
        return {"success": False, "message": "invalid authorization cookie"}, 403
    user = auth.Token.verify(token)
    if user is None:
        return {"success": False, "message": "invalid authorization cookie"}, 403
    # authorization
    content = request.get_json()
    if content.get("username") is None:
        return {"success": False, "message": "missing username"}, 422
    user = User.query.filter_by(username=user.get("username")).first()
    if content.get("username") != user.username:
        # unauthorized operation
        return {"success": False, "message": "invalid authorization cookie"}, 403
    # processing request
    content = request.get_json()
    # content contains uri of playlist, and vote (which can be equal to: 1 (to upvote), -1 (to downvote) or 0 (to clear vote))
    if (
        content.get("uri") is None
        or content.get("vote") is None
        or content.get("moodid") is None
    ):
        return {"success": False, "message": "missing uri and/or vote"}, 422
    if content.get("vote") not in (-1, 0, 1):
        return {
            "success": False,
            "message": "invalid vote, should be either -1, 0, 1",
        }, 422
    mood = Mood.query.filter_by(id=content.get("moodid")).first()
    if mood is None:
        return {"success": False, "message": "invalid mood id"}, 422
    return user.vote(uri=content.get("uri"), vote=content.get("vote"), mood=mood)


@bp.route("/update/<uri>", methods=["PUT"])
def update(uri):
    # tested
    logging.info(f"request: PUT /music/update - {request.get_json()}")
    tokenString = request.cookies.get(COOKIE_NAME)
    if not auth.Token.verify_blacklist(tokenString):
        return {"success": False, "message": "invalid authorization cookie"}, 403
    user = auth.Token.verify(tokenString)
    if user is None:
        return {"success": False, "message": "invalid authorization cookie"}, 403
    content = request.get_json()
    if content.get("username") is None:
        return {"success": False, "message": "missing username"}, 422
    if content.get("username") != user.get("username"):
        # unauthorized operation
        return {"success": False, "message": "invalid authorization cookie"}, 403
    user = User.query.filter_by(username=content.get("username")).first()
    if user is None:
        return {"success": False, "message": "account not found"}, 404
    playlist = Playlist.query.filter_by(uri=uri, owner=user).first()
    if playlist is None:
        return {
            "success": False,
            "message": "playlist not found or user not authorized to update it",
        }, 404
    content = request.get_json()
    success, message = playlist.update(content)
    return {"success": success, "message": message or f"update successful - {playlist}"}


@bp.route("/delete/<uri>", methods=["DELETE"])
def delete(uri):
    # tested
    logging.info(f"request: DELETE /music/delete/{uri}")
    # added to api documentation
    tokenString = request.cookies.get(COOKIE_NAME)
    if not auth.Token.verify_blacklist(tokenString):
        return {"success": False, "message": "invalid authorization cookie"}, 403
    user = auth.Token.verify(tokenString)
    if user is None:
        return {"success": False, "message": "invalid authorization cookie"}, 403
    content = request.get_json()
    if content.get("username") is None:
        return {"success": False, "message": "missing username"}, 422
    if content.get("username") != user.get("username"):
        # unauthorized operation
        return {"success": False, "message": "invalid authorization cookie"}, 403
    user = User.query.filter_by(username=content.get("username")).first()
    if user is None:
        return {"success": False, "message": "account not found"}, 404
    playlist = Playlist.query.filter_by(uri=uri, owner=user).first()
    if playlist is None:
        return {"success": False, "message": "playlist not found"}, 404
    return playlist.delete(user)


@bp.after_request  # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response
