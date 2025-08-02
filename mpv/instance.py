import os
import socket
import json
import time

from config import MPV_SOCKET, MPV_POLL_INTERVAL

class MPVInstance:
    def __init__(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._file_cb = None
        self._playback_cb = None
        self._quit_cb = None

    def on_file_change(self, callback):
        self._file_cb = callback

    def on_playback_change(self, callback):
        self._playback_cb = callback

    def on_quit(self, callback):
        self._quit_cb = callback

    def run(self):
        while True:
            if not os.path.exists(MPV_SOCKET):
                print("Waiting for MPV...")
                time.sleep(MPV_POLL_INTERVAL)
                continue

            try:
                self._connect_and_listen()
            except Exception:
                print("Stale socket found. Removing...")
                os.remove(MPV_SOCKET)
                time.sleep(MPV_POLL_INTERVAL)

    def pause(self):
        self._send_command({"command": ["set_property", "pause", True]})

    def play(self):
        self._send_command({"command": ["set_property", "pause", False]})

    def _connect_and_listen(self):
        self.socket.connect(MPV_SOCKET)

        self._send_command({"command": ["observe_property", 0, "path"]})
        self._send_command({"command": ["observe_property", 1, "pause"]})
        buffer = b""
        while True:
            chunk = self.socket.recv(4096)
            if not chunk:
                break
            buffer += chunk

            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                try:
                    event = json.loads(line.decode("utf-8"))
                    if event.get("event") == "property-change":
                        name = event.get("name")
                        data = event.get("data")
                        if name == "path" and self._file_cb:
                            self._file_cb(data)
                        elif name == "pause" and self._playback_cb:
                            self._playback_cb(data)
                    elif event.get("event") == "end-file":
                        if self._quit_cb:
                            self._quit_cb()
                    elif event.get("event") == "shutdown":
                        if self._quit_cb:
                            self._quit_cb()
                except Exception as e:
                    print(f"Error processing event: {e}")

    def _send_command(self, command):
        self.socket.sendall(json.dumps(command).encode("utf-8") + b"\n")
