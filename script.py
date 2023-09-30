import asyncio
from pathlib import Path

import telegram

from lastfm import *
from spotify import *
from util import *


# def mdEscape(text):
#     return re.sub(r"([_*\[\]\(\)~`>#\+-=\|{}\.!])", r'\<1>', text)


async def send_sms(lfm, spotify, missing):
    bot = telegram.Bot(telegramBot)
    async with bot:
        await bot.send_message(text=f'Hoi, de lastfm scrobbler lijkt weer krak te zijn. Er mistte {missing} nummers.\n'
                                    f'Laatste last-fm: {lfm}\n'
                                    f'Laatste spotify: {spotify}\n\n'
                                    f'https://www.last.fm/settings/applications',
                               chat_id=telegramChat)


def count_missing(lfm, spotify):
    lfm_s = map(lambda track: create_track(track).lower(), lfm)
    spotify_s = map(lambda track: create_track(track).lower(), spotify)
    return len(list(filter(lambda track: track not in spotify_s, lfm_s)))


def run():
    p = Path(__file__).with_name('state')
    with p.open('r+') as file:
        prev = file.read()
        if prev != '1':
            print('Watcher is turned off.')
            return

    lfm = get_lastfm_tracks(trackCount)
    spotify = get_spotify_tracks(trackCount)
    missing = count_missing(lfm, spotify)

    if missing >= threshold:
        print('Last.fm and spotify out of sync')
        asyncio.run(send_sms(create_track(lfm[0]), create_track(spotify[0]), missing))


run()
