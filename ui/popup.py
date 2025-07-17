import customtkinter as ctk

class TraktPopup(ctk.CTkToplevel):
    def __init__(self, master, results, on_select):
        super().__init__(master)
        self.title("Choose a Trakt Match")
        self.geometry("400x400")
        self.on_select = on_select
        self.focus()

        for r in results:
            type = r.get("type")
            item = r.get(type)

            ctk.CTkButton(
                self,
                text=item["title"],
                command=lambda i=r: self.select(i)
            ).pack(pady=5)

        ctk.CTkButton(self, text="Cancel", command=self.destroy).pack(pady=10)

    def select(self, item):
        self.on_select(item)
        self.destroy()
