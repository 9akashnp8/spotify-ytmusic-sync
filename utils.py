from typing import List

from logger import logger
from models import YTMusicSearchPayload
from services import yt_music_like_wrapper, yt_music_search_wrapper

MOCK_SPOTIFY_PLAYLIST_SONGS = [
    {
        "song_id": "4a49PDoDgb7IiQtoxjuUXK",
        "name": "Tokyo",
        "artist": "Timecop1983"
    },
    {
        "song_id": "2nMeu6UenVvwUktBCpLMK9",
        "name": "Young And Beautiful",
        "artist": "Lana Del Rey"
    },
    {
        "song_id": "6P30NMoLLzWTuue4faRjsd",
        "name": "Bright Blue Berlin Sky",
        "artist": "The Shutes"
    },
    {
        "song_id": "1GxNPd5r7D1zChEMuMhue0",
        "name": "Only",
        "artist": "RY X"
    },
    {
        "song_id": "3AqPL1n1wKc5DVFFnYuJhp",
        "name": "To Build A Home",
        "artist": "The Cinematic Orchestra"
    },
    {
        "song_id": "1aEsTgCsv8nOjEgyEoRCpS",
        "name": "this is how you fall in love",
        "artist": "Jeremy Zucker"
    },
    {
        "song_id": "0ZAbupc7jAQpG9IxojQ3s3",
        "name": "Cocaine Jesus",
        "artist": "Rainbow Kitten Surprise"
    },
    {
        "song_id": "4w4tdTFijVgVvT3kujszX6",
        "name": "Deep Blue - Droid Bishop Remix",
        "artist": "The Midnight"
    },
    {
        "song_id": "0DlrV801mOlq3zZijliOqB",
        "name": "Ghost Story (with All Time Low)",
        "artist": "Cheat Codes"
    },
    {
        "song_id": "5GQyYSGz8bymILpekzEy7L",
        "name": "Bad Dream Baby",
        "artist": "September 87"
    },
    {
        "song_id": "0DmDj6uDZIKcnhFjqytqNs",
        "name": "Hangin' On",
        "artist": "LeBrock"
    },
    {
        "song_id": "0TxPln0uhql4ucFGk1XISM",
        "name": "Wrong Time",
        "artist": "Hippie Sabotage"
    },
    {
        "song_id": "6JdU7eaEl9fPAq0sEVNzGc",
        "name": "say goodbye",
        "artist": "Sarcastic Sounds"
    },
    {
        "song_id": "1jUkHIMc7UaJQuzWe5Iop2",
        "name": "Sweet Disposition",
        "artist": "The Temper Trap"
    },
    {
        "song_id": "2Ahtup0oSl1OZVl4325JGU",
        "name": "Next To You",
        "artist": "New West"
    },
    {
        "song_id": "2FTTz19ql2XzrwnCBM0dP7",
        "name": "10K Summer Nights",
        "artist": "Eighty Ninety"
    },
    {
        "song_id": "4eDtZP99H6xfasP4Tku9Ee",
        "name": "Fairytale",
        "artist": "Livingston"
    },
    {
        "song_id": "6OnfBiiSc9RGKiBKKtZXgQ",
        "name": "We Built This City",
        "artist": "Starship"
    },
    {
        "song_id": "4gvea7UlDkAvsJBPZAd4oB",
        "name": "The Boys Of Summer",
        "artist": "Don Henley"
    },
    {
        "song_id": "5O4NFbDqJ8SOfbjnIhdPDt",
        "name": "The Safety Dance",
        "artist": "Men Without Hats"
    },
    {
        "song_id": "7L3b6iaVhDVjfo52Hbvh9Z",
        "name": "Edge of Seventeen - 2016 Remaster",
        "artist": "Stevie Nicks"
    }
]

MOCK_YTMUSIC_SEARCH_RESULT = [
    {
        "source_song_id": "4a49PDoDgb7IiQtoxjuUXK",
        "ytmusic_song_id": "jtsAV736A2k",
        "name": "Tokyo",
        "artist": "Timecop1983"
    },
    {
        "source_song_id": "2nMeu6UenVvwUktBCpLMK9",
        "ytmusic_song_id": "mjcX-5lKdeg",
        "name": "Young And Beautiful",
        "artist": "Lana Del Rey"
    },
    {
        "source_song_id": "6P30NMoLLzWTuue4faRjsd",
        "ytmusic_song_id": "yNl5zpEmwVI",
        "name": "Bright Blue Berlin Sky",
        "artist": "The Shutes"
    },
    {
        "source_song_id": "1GxNPd5r7D1zChEMuMhue0",
        "ytmusic_song_id": "vRMD_9g33Ww",
        "name": "Only",
        "artist": "RY X"
    },
    {
        "source_song_id": "3AqPL1n1wKc5DVFFnYuJhp",
        "ytmusic_song_id": "OAYuMygPkbI",
        "name": "To Build A Home (feat. Patrick Watson)",
        "artist": "The Cinematic Orchestra"
    },
    {
        "source_song_id": "1aEsTgCsv8nOjEgyEoRCpS",
        "ytmusic_song_id": "kkdYpecD2pw",
        "name": "this is how you fall in love",
        "artist": "Jeremy Zucker,Chelsea Cutler"
    },
    {
        "source_song_id": "0ZAbupc7jAQpG9IxojQ3s3",
        "ytmusic_song_id": "CPXkZcGOKhI",
        "name": "Cocaine Jesus",
        "artist": "Rainbow Kitten Surprise"
    },
    {
        "source_song_id": "4w4tdTFijVgVvT3kujszX6",
        "ytmusic_song_id": "dGvGaE23bKg",
        "name": "Deep Blue (Droid Bishop Remix)",
        "artist": "The Midnight"
    },
    {
        "source_song_id": "0DlrV801mOlq3zZijliOqB",
        "ytmusic_song_id": "GQzXSbEMWeM",
        "name": "Ghost Story",
        "artist": "Cheat Codes,All Time Low"
    },
    {
        "source_song_id": "5GQyYSGz8bymILpekzEy7L",
        "ytmusic_song_id": "s7buOVqE55c",
        "name": "Bad Dream Baby",
        "artist": "September 87"
    },
    {
        "source_song_id": "0DmDj6uDZIKcnhFjqytqNs",
        "ytmusic_song_id": "nsR5b8KTDSY",
        "name": "Hangin' On",
        "artist": "LeBrock"
    },
    {
        "source_song_id": "0TxPln0uhql4ucFGk1XISM",
        "ytmusic_song_id": "Qw1kIMy2Q_s",
        "name": "Wrong Time",
        "artist": "Hippie Sabotage"
    },
    {
        "source_song_id": "6JdU7eaEl9fPAq0sEVNzGc",
        "ytmusic_song_id": "Tt2GjQwS7dg",
        "name": "say goodbye",
        "artist": "Sarcastic Sounds"
    },
    {
        "source_song_id": "1jUkHIMc7UaJQuzWe5Iop2",
        "ytmusic_song_id": "EDpXR2_-WSY",
        "name": "Sweet Disposition",
        "artist": "The Temper Trap"
    },
    {
        "source_song_id": "2Ahtup0oSl1OZVl4325JGU",
        "ytmusic_song_id": "qSqFW2vuD9w",
        "name": "Next To You",
        "artist": "New West"
    },
    {
        "source_song_id": "2FTTz19ql2XzrwnCBM0dP7",
        "ytmusic_song_id": "ySl3IbOAWdc",
        "name": "10K Summer Nights",
        "artist": "Eighty Ninety"
    },
    {
        "source_song_id": "4eDtZP99H6xfasP4Tku9Ee",
        "ytmusic_song_id": "y57nt6WhKTM",
        "name": "Fairytale",
        "artist": "Livingston"
    },
    {
        "source_song_id": "6OnfBiiSc9RGKiBKKtZXgQ",
        "ytmusic_song_id": "BsCBGsKSW4g",
        "name": "We Built This City",
        "artist": "Starship"
    },
    {
        "source_song_id": "4gvea7UlDkAvsJBPZAd4oB",
        "ytmusic_song_id": "P8Jw5FbKbK0",
        "name": "The Boys Of Summer",
        "artist": "Don Henley"
    },
    {
        "source_song_id": "5O4NFbDqJ8SOfbjnIhdPDt",
        "ytmusic_song_id": "M-FlrqHE5MY",
        "name": "The Safety Dance",
        "artist": "Men Without Hats"
    },
    {
        "source_song_id": "7L3b6iaVhDVjfo52Hbvh9Z",
        "ytmusic_song_id": "b5bgQjTmm3g",
        "name": "Edge of Seventeen",
        "artist": "Stevie Nicks"
    }
]


def sync_ytmusic_spotify(song: YTMusicSearchPayload):
    """
    Search YTMusic for given <song name> - <artist> combo
    """
    logger.info("search_and_like Triggered")
    yt_music_song = yt_music_search_wrapper(song.song_id, song.name, song.artist)
    if yt_music_song:
        yt_music_like_wrapper(yt_music_song.ytmusic_song_id)
        logger.info(f"Found and liked: {song.name} by {song.artist}")
    else:
        logger.error(f"Song {song.name} not found on YTMusic")


def sync_ytmusic_spotify(songs: List[YTMusicSearchPayload]):
    """
    Main function used as background task that syncs Spotify
    songs to YTMusics

    Iterates over `YTMusicSearchPayload` objects to search and
    like given songs
    """
    logger.info("Sync Started")
    for song in songs:
        sync_ytmusic_spotify(song)
    logger.info("Sync Complete")
