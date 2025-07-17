from mpv.instance import MPVInstance

from util import clean_file_name

MPV = MPVInstance()

def handle_new_file(path):
    cleaned_name = clean_file_name(path)
    print(cleaned_name)

def handle_play_pause(paused):
    print("Paused" if paused else "Resumed")

def main():
    MPV.on_file_change(handle_new_file)
    MPV.on_playback_change(handle_play_pause)
    MPV.run()

if __name__ == "__main__":
    main()
