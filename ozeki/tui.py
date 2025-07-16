# Stdlib
import time

# 3rd party
from textual.theme import Theme
from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label
from textual.widgets import Footer
from textual.containers import Horizontal, Vertical, VerticalScroll

# Internal
from .client import SumoAPI
from .banzuke import BanzukeWidget


class SumoApp(App):

    CSS = """
Horizontal { background: $surface; }
Vertical { background: $surface; width: 20; }
ListView { padding: 1; }
/* Container */
VerticalScroll { 
    width: 5fr; 
    overflow: auto;
    background: $surface; 
    overflow: auto;  /* Better than separate x/y */
}

/* Widget */
#banzuke {
    width: auto;  /* Let content determine width */
    min-width: 100%;  /* Ensure it fills container */
    content-align: center middle;
    background: $surface;
    height: auto;  /* Important for scrolling */
}
"""
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+t", "toggle_theme", "Toggle light/dark mode"),
    ]

    themes = {
        "current": "kakejiku-light",
        "light": Theme(
            name="kakejiku-light",
            primary="#1a1a1a",  # Sumi black (main text)
            secondary="#8b0000",  # Vermilion ink (accents, stamps)
            accent="#c19a6b",  # Muted gold (highlight or focal elements)
            foreground="#1a1a1a",  # Deep ink tone
            background="#f8f4e3",  # Washi paper base
            success="#6b8e23",  # Olive green (natural, understated)
            warning="#b5651d",  # Earthy orange (subtle contrast)
            error="#990000",  # Dark red (without overwhelming)
            surface="#ede6d0",  # Scroll body (slightly off-washi)
            panel="#dcd2b2",  # Borders or side panels (gold-tan trim)
            dark=False,
            variables={
                "block-cursor-text-style": "none",
                "footer-key-foreground": "#8b0000",  # Red accent
                "input-selection-background": "#c19a6b 35%",
                "highlight-foreground": "#c19a6b",
                "highlight-background": "#f0e8cc",
            },
        ),
        "dark": Theme(
            name="kakejiku-dark",
            primary="#e0c07d",  # Gold script ink (primary accent)
            secondary="#a93f2e",  # Deep vermilion (seals, alerts)
            accent="#82664a",  # Aged bronze (secondary highlight)
            foreground="#e8e6dc",  # Pale ink on dark scroll
            background="#1a1a1a",  # Lacquer-black base
            success="#6f9f6a",  # Subtle green (nature balance)
            warning="#d19a66",  # Burnt orange
            error="#a93434",  # Dried crimson ink
            surface="#2a2a2a",  # Scroll body
            panel="#33302a",  # Faintly warm dark background
            dark=True,
            variables={
                "block-cursor-text-style": "bold",
                "footer-key-foreground": "#e0c07d",
                "input-selection-background": "#a93f2e 30%",
                "highlight-foreground": "#e0c07d",
                "highlight-background": "#2f2c26",
            },
        ),
    }

    bashos = {}
    months = {
        1: "January",
        3: "March",
        5: "May",
        7: "July",
        9: "September",
        11: "November",
    }
    divisions = ("Makuuchi", "Juryo", "Makushita", "Sandanme", "Jonidan", "Jonokuchi")
    sumo = SumoAPI()

    def action_toggle_theme(self) -> None:
        if self.themes["current"] == "kakejiku-light":
            self.themes["current"] = "kakejiku-dark"
        elif self.themes["current"] == "kakejiku-dark":
            self.themes["current"] = "kakejiku-light"
        else:
            self.themes["current"] = "kakejiku-light"
        self.theme = self.themes["current"]

    def on_mount(self) -> None:
        self.register_theme(self.themes["light"])
        self.register_theme(self.themes["dark"])
        self.action_toggle_theme()

    def data_setup(self) -> None:
        self.bashos = {}
        for year in range(1960, 2026):
            for month in (1, 3, 5, 7, 9, 11):
                if year < time.gmtime().tm_year:
                    self.bashos[f"{year}{month:02d}"] = (
                        f"{self.months[month]:10s} {year}"
                    )
                elif year == time.gmtime().tm_year and month <= time.gmtime().tm_mon:
                    self.bashos[f"{year}{month:02d}"] = (
                        f"{self.months[month]:10s} {year}"
                    )

    def compose(self) -> ComposeResult:
        if len(self.bashos.keys()) == 0:
            self.data_setup()

        with Horizontal(id="main-horiz"):
            with Vertical(id="side-bar"):
                keys = list(self.bashos.keys())
                keys.sort()
                keys.reverse()
                yield ListView(
                    *[ListItem(Label(self.bashos[k]), id=f"n_{k}") for k in keys],
                    id="bashos",
                )
                yield ListView(
                    *[ListItem(Label(n), id=n) for n in self.divisions], id="divisions"
                )
            yield VerticalScroll(BanzukeWidget(id="banzuke"))
            yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        w_basho = self.query_one("#bashos")
        w_divi = self.query_one("#divisions")
        basho = w_basho.children[w_basho.index].id.split("_")[1]
        divi = w_divi.children[w_divi.index].id
        banzuke = self.query_one(BanzukeWidget)

        banzuke.init_d = ""
        banzuke.ydata = self.sumo.basho(basho)
        banzuke.data = self.sumo.banzuke(basho, divi)
        torikumi = []
        for n in range(1, 16):
            torikumi.append(self.sumo.torikumi(basho, divi, n))
        banzuke.tdata = torikumi
