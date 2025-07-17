import customtkinter as ctk
import queue

class UIManager:
    _root: ctk.CTk | None = None
    _queue = queue.Queue()

    @classmethod
    def start_ui(cls):
        cls._root = ctk.CTk()
        cls._root.withdraw()  # Hide window
        cls._root.after(100, cls._process_queue)
        cls._root.mainloop()

    @classmethod
    def _process_queue(cls):
        while not cls._queue.empty():
            func, args = cls._queue.get()
            func(*args)
        if cls._root is not None:
            cls._root.after(100, cls._process_queue)

    @classmethod
    def show_trakt_popup(cls, results, on_select):
        def show():
            popup = TraktPopup(cls._root, results, on_select)
            popup.grab_set()  # Modal behavior
        cls._queue.put((show, []))

from ui.popup import TraktPopup  # At the bottom to avoid circular import
