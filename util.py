def create_track(track):
    return f'{track[0]} - {track[1]}'


def create_track_with_ts(track):
    return f'{track[2].strftime("%d-%m-%Y %H:%M")}: {create_track(track)}'
