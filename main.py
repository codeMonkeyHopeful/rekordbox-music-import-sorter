import os
import shutil
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen import File as MutagenFile

CAMELOT_KEYS = {
    "C": "8B",
    "C#": "3B",
    "Db": "3B",
    "D": "10B",
    "D#": "5B",
    "Eb": "5B",
    "E": "12B",
    "F": "7B",
    "F#": "2B",
    "Gb": "2B",
    "G": "9B",
    "G#": "4B",
    "Ab": "4B",
    "A": "11B",
    "A#": "6B",
    "Bb": "6B",
    "B": "1B",
    "Cm": "5A",
    "C#m": "12A",
    "Dbm": "12A",
    "Dm": "7A",
    "D#m": "2A",
    "Ebm": "2A",
    "Em": "9A",
    "Fm": "4A",
    "F#m": "11A",
    "Gbm": "11A",
    "Gm": "6A",
    "G#m": "1A",
    "Abm": "1A",
    "Am": "8A",
    "A#m": "3A",
    "Bbm": "3A",
    "Bm": "10A",
}

SOURCE_FOLDER = "/Volumes/Rekordbox SSD/_Unsorted"
GENRE_FOLDER = "/Volumes/Rekordbox SSD/Organized"
ENERGY_FOLDER = "/Volumes/Rekordbox SSD/Energy"


def get_energy_level(bpm):
    if bpm == "???" or bpm is None:
        return "Unknown"
    try:
        bpm = int(bpm)
        if bpm < 95:
            return "Chill"
        elif bpm < 110:
            return "Warm Up"
        elif bpm <= 128:
            return "Peak Time"
        else:
            return "After Hours"
    except Exception as e:
        print(f"Error parsing BPM: {e}")
        return "Unknown"


def get_metadata(file_path):
    try:
        tags = EasyID3(file_path)
        artist = tags.get("artist", ["Unknown Artist"])[0]
        title = tags.get("title", ["Unknown Title"])[0]
        genre = tags.get("genre", ["Unknown"])[0]
    except Exception as e:
        artist, title, genre = "Unknown Artist", "Unknown Title", "Unknown"
        print(f"Error reading tags: {e}")

    # Key
    try:
        audio = MutagenFile(file_path)
        key_raw = audio.get("TKEY", [""])[0]
        key = key_raw.strip()
        camelot = CAMELOT_KEYS.get(key, key) if key else "UnknownKey"
    except Exception as e:

        camelot = "UnknownKey"
        print(f"Error reading key: {e}")

    # BPM
    try:
        bpm = int(MP3(file_path).info.bpm)
    except Exception as e:
        bpm = "???"
        print(f"Error reading BPM: {e}")

    return artist.strip(), title.strip(), genre.strip(), bpm, camelot


def organize_files():
    for root, dirs, files in os.walk(SOURCE_FOLDER):
        for file in files:
            if file.lower().endswith(".mp3"):
                full_path = os.path.join(root, file)
                artist, title, genre, bpm, key = get_metadata(full_path)

                filename = f"{artist} - {title} " f"[{bpm}BPM - {key}].mp3"
                filename = filename.replace("/", "-")

                # GENRE folder copy
                genre_path = os.path.join(GENRE_FOLDER, genre)
                os.makedirs(genre_path, exist_ok=True)
                genre_dest = os.path.join(genre_path, filename)
                if not os.path.exists(genre_dest):
                    print(f"Copying to genre: {genre_dest}")
                    shutil.copy2(full_path, genre_dest)

                # ENERGY folder copy
                energy_level = get_energy_level(bpm)
                energy_path = os.path.join(ENERGY_FOLDER, energy_level)
                os.makedirs(energy_path, exist_ok=True)
                energy_dest = os.path.join(energy_path, filename)
                if not os.path.exists(energy_dest):
                    print(f"Copying to energy: {energy_dest}")
                    shutil.copy2(full_path, energy_dest)


if __name__ == "__main__":
    organize_files()
