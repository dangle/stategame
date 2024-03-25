from __future__ import annotations

import tkinter as tk

from PIL import ImageTk

from state import State
from state_machine import StateMachine


class TkStateMachine(StateMachine):

    WINDOW_TITLE: str = "State Game"
    IMAGE_HEIGHT: int = 1024
    IMAGE_WIDTH: int = 1024

    def __init__(self, start_state: State):
        super().__init__(start_state)
        self._window = tk.Tk()
        self._window.title(self.WINDOW_TITLE)
        self._window.resizable(False, False)
        self._window.after(100, self._on_tick)

        self._image = None

        self._image_frame = tk.Frame(
            self._window,
            height=self.IMAGE_HEIGHT,
            width=self.IMAGE_WIDTH,
        )
        self._image_frame.pack()

        self._image_label = tk.Label(
            self._image_frame,
            text="Loading...",
            font=("Sans", 16),
        )
        self._image_label.pack(fill=tk.BOTH, expand=tk.YES)
        self._image_label.lower()

        self._description_frame = tk.Frame(
            self._image_frame,
        )
        self._description_frame.place(
            relx=0.5,
            rely=0.1,
            anchor=tk.CENTER,
        )

        self._prompt_frame = tk.Frame(
            self._image_frame,
        )
        self._prompt_frame.place(
            relx=0.5,
            rely=0.95,
            anchor=tk.CENTER,
        )

        self._prompt = tk.Entry(self._window, font=("Sans", 16))
        self._prompt.pack(expand=True, fill=tk.BOTH)
        self._prompt.focus()
        self._prompt.bind("<Return>", self._on_return)

    def _update(self):
        if self._state.is_terminal:
            self._window.quit()
            return

        self.display_state()

    def _on_tick(self):
        new_state = self._state.transition()

        if new_state != self._state:
            self._state = new_state
            self._update()

        self._window.after(100, self._on_tick)

    def _on_return(self, _):
        transition = self.get_transition()
        new_state = self._state.transition(transition)

        if new_state != self._state:
            self._state = new_state
            self._update()

    def display_state(self):
        if self._state.is_terminal:
            return

        if self._state.image:
            self._image = ImageTk.PhotoImage(self._state.image)
            self._image_label.config(image=self._image)

        for widgets in self._description_frame.winfo_children():
            widgets.destroy()

        self._description_frame.place_forget()

        if self._state.description:
            self._description_frame.place(
                relx=0.5,
                rely=0.1,
                anchor=tk.CENTER,
            )
            tk.Label(
                self._description_frame,
                text=self._state.description,
                font=("Sans", 10),
                wraplength=int(self.IMAGE_WIDTH),
                background="black",
                foreground="white",
            ).pack(fill=tk.X, expand=True)

        for widgets in self._prompt_frame.winfo_children():
            widgets.destroy()

        self._prompt_frame.place_forget()

        if self._state.prompt:
            self._prompt_frame.place(
                relx=0.5,
                rely=0.95,
                anchor=tk.CENTER,
            )
            tk.Label(
                self._prompt_frame,
                text=self._state.prompt,
                font=("Sans", 10),
                wraplength=int(self.IMAGE_WIDTH),
                background="black",
                foreground="white",
            ).pack(fill=tk.X, expand=True)

    def get_transition(self) -> str:
        input_: str = self._prompt.get()
        self._prompt.delete(0, tk.END)
        self._prompt.focus()
        return input_

    def _generate_images(self):
        print("Generating state images...", end="", flush=True)

        for state in State.__subclasses__():
            state().image

        print(" done", flush=True)

    def run(self):
        self._generate_images()

        self.display_state()

        self._window.mainloop()
