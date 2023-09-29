from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from conf import *


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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await toggle_state(update, '1', 'aan')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await toggle_state(update, '0', 'uit')


def main() -> None:
    application = Application.builder().token(telegramBot).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
