from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from lastfm import *
from spotify import *
from util import *


def get_tracks(type, amount):
    if type == 's':
        return get_spotify_tracks(amount)
    else:
        return get_lastfm_tracks(amount)


async def toggle_state(update: Update, to: str, text: str):
    p = Path(__file__).with_name('state')
    with p.open('r+') as file:
        prev = file.read()

        if prev == to:
            await update.message.reply_text(f'⚠️ Spotify-scrobble-watcher staat al {text}!')
        else:
            file.seek(0)
            file.write(to)
            file.truncate()
            await update.message.reply_text(f'🚀 Spotify-scrobble-watcher {text}gezet!')


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await toggle_state(update, '1', 'aan')


# /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await toggle_state(update, '0', 'uit')


# /getrecent lastfm 10
# /getrecent spotify 25
async def getrecent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text(f'⚠️ Invalid amount of arguments.')
        return

    type = args[0][0].lower()
    if type not in ['s', 'l']:
        await update.message.reply_text(f'⚠️ Cannot retrieve recent tracks for {args[0]}.')
        return

    try:
        amount = int(args[1])
    except (ValueError, TypeError):
        await update.message.reply_text(f'⚠️ {args[1]} is not a valid amount.')
        return

    tracks = '\n'.join(map(lambda track: create_track(track) + '\n', get_tracks(type, amount)))
    name = 'Spotify' if type == 's' else 'Last.fm'
    await update.message.reply_text(f'🎶 The latest {args[1]} tracks for {name}:\n\n{tracks}')


def main() -> None:
    application = Application.builder().token(telegramBot).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("getrecent", getrecent))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
