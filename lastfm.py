from zoneinfo import ZoneInfo
from datetime import timezone, datetime

from requests import get

from conf import *


def get_lastfm_tracks(amount):
    response = get(
        f'https://ws.audioscrobbler.com/2.0/?'
        f'method=user.getrecenttracks&'
        f'user={lfmUsername}&'
        f'api_key={lfmApiKey}&'
        f'format=json&limit={amount}')
    tracks = response.json().get('recenttracks').get('track')
    finished = list(filter(lambda x: '@attr' not in x or x.get('@attr').get('nowplaying') != 'true', tracks))
    return list(map(lambda track: (
        track.get('artist').get('#text'),
        track.get('name'),
        datetime.fromtimestamp(int(track.get('date').get('uts')), tz=timezone.utc).astimezone(tz=ZoneInfo("Europe/Amsterdam"))
    ), finished))
