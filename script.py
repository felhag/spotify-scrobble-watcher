import asyncio
from pathlib import Path

import spotipy
import telegram
from requests import get
from spotipy.oauth2 import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

from conf import *


# def mdEscape(text):
#     return re.sub(r"([_*\[\]\(\)~`>#\+-=\|{}\.!])", r'\<1>', text)


async def send_sms(lfm, spotify):
    bot = telegram.Bot(telegramBot)
    async with bot:
        await bot.send_message(text=f'Hoi, de lastfm scrobbler lijkt weer krak te zijn.\n'
                                    f'Laatste last-fm: {lfm}\n'
                                    f'Laatste spotify: {spotify}\n\n'
                                    f'https://www.last.fm/settings/applications',
                               chat_id=telegramChat)


def get_api(username):
    handler = CacheFileHandler(cache_path='./.cache/' + username, username=username)
    auth_manager = SpotifyOAuth(client_id=spotifyClientId,
                                client_secret=spotifyClientSecret,
                                redirect_uri=spotifyRedirectUrl,
                                cache_handler=handler,
                                open_browser=False,
                                scope="user-read-recently-played")
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


def get_lastfm_tracks():
    response = get(
        f'https://ws.audioscrobbler.com/2.0/?'
        f'method=user.getrecenttracks&'
        f'user={lfmUsername}&'
        f'api_key={lfmApiKey}&'
        f'format=json&limit={trackCount}')
    tracks = response.json().get('recenttracks').get('track')
    finished = list(filter(lambda x: '@attr' not in x or x.get('@attr').get('nowplaying') != 'true', tracks))
    return list(map(lambda track: (
        track.get('artist').get('#text').lower(),
        track.get('name').lower(),
        # datetime.utcfromtimestamp(int(track.get('date').get('uts')))
    ), finished))


def get_spotify_tracks():
    playlists = get_api(spotifyUsername).current_user_recently_played(limit=trackCount)['items']
    return list(map(lambda track: (
        track.get('track').get('artists')[0].get('name').lower(),
        track.get('track').get('name').lower(),
        # datetime.fromisoformat(track.get('played_at')[:-1])
    ), playlists))


def create_track(track):
    return f'{track[0]} - {track[1]}'


def run():
    p = Path(__file__).with_name('state')
    with p.open('r+') as file:
        prev = file.read()
        if prev != '1':
            print('Watcher is turned off.')
            return

    lfm = get_lastfm_tracks()
    spotify = get_spotify_tracks()
    missing = list(filter(lambda track: track not in spotify, lfm))

    if len(missing) >= threshold:
        print('Last.fm and spotify out of sync')
        asyncio.run(send_sms(create_track(lfm[0]), create_track(spotify[0])))


run()
