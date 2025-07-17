from mpv.instance import MPVInstance
from trakt.client import TraktClient
from ui.manager import UIManager
from ui.session import SESSION
from util import clean_file_name

MPV = MPVInstance()
TRAKT = TraktClient()

def handle_new_file(path):
    if not path:
        return
    cleaned_name = clean_file_name(path)
    data = TRAKT.search(cleaned_name)
    if data and len(data) > 0:
        UIManager.show_trakt_popup(data, on_trakt_selection)

def handle_play_pause(paused):
    print("Paused" if paused else "Resumed")

def on_trakt_selection(item):
    SESSION.start(item)
    print(f"Chosen {item}")

def main():
    MPV.on_file_change(handle_new_file)
    MPV.on_playback_change(handle_play_pause)
    import threading
    threading.Thread(target=MPV.run, daemon=True).start()

    # Start the CustomTkinter root once
    UIManager.start_ui()

if __name__ == "__main__":
    main()
