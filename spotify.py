from zoneinfo import ZoneInfo
from datetime import datetime, timezone

import spotipy
from spotipy import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

from conf import *


def get_api(username):
    handler = CacheFileHandler(cache_path='./.cache/' + username, username=username)
    auth_manager = SpotifyOAuth(client_id=spotifyClientId,
                                client_secret=spotifyClientSecret,
                                redirect_uri=spotifyRedirectUrl,
                                cache_handler=handler,
                                open_browser=False,
                                scope="user-read-recently-played")
    return spotipy.Spotify(auth_manager=auth_manager)


def get_spotify_tracks(amount):
    tracks = get_api(spotifyUsername).current_user_recently_played(limit=amount)['items']
    return list(map(lambda track: (
        track.get('track').get('artists')[0].get('name'),
        track.get('track').get('name'),
        datetime.fromisoformat(track.get('played_at')[:-1])
        .replace(tzinfo=timezone.utc)
        .astimezone(ZoneInfo("Europe/Amsterdam"))
    ), tracks))
