# Stdlib
import os
import time
from threading import Thread

# 3rd party
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Select, Header
from textual.containers import Horizontal, VerticalScroll

# Internal
from .client import SumoAPI
from .themes import THEMES
from .basho import BashoWidget
from .banzuke import BanzukeWidget
from .torikumi import TorikumiWidget


class Ozeki(App):

    CSS = """
#drop-down {
    height: 5;
    background: $surface;
    width: 100%;
}

#main-content {
    width: 100%;
    height: 1fr;
    background: $surface;
}

/* Widget */
#basho {
    padding-left: 1;
    width: auto;  /* Let content determine width */
    min-width: 100%;  /* Ensure it fills container */
    content-align: center top;
    background: $surface;
    height: auto;  /* Important for scrolling */
}
#banzuke {
    padding-left: 1;
    width: auto;  /* Let content determine width */
    min-width: 100%;  /* Ensure it fills container */
    content-align: center top;
    background: $surface;
    height: auto;  /* Important for scrolling */
}
#torikumi {
    padding-left: 1;
    width: auto;  /* Let content determine width */
    min-width: 100%;  /* Ensure it fills container */
    content-align: center top;
    background: $surface;
    height: auto;  /* Important for scrolling */
}
"""
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+t", "cycle_theme", "Cycle Theme"),
        ("ctrl+b", "background_updates", "Toggle Background Updates"),
    ]

    themes = THEMES
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
    _init = True
    _t_thread = False

    def action_cycle_theme(self) -> None:
        self.theme = next(self.themes)["theme"].name
        with open(f"{os.getenv('HOME', '~')}/.ozeki", "w+") as fp:
            fp.write(self.theme)

    def action_background_updates(self) -> None:
        if self._t_thread:
            self._t_thread = False
            return
        self._t_thread = True
        Thread(target=self._update_thread, daemon=True).start()

    def _update_thread(self) -> None:
        while self._t_thread:
            i_basho = self.query_one("#basho_s", Select).selection
            i_divis = self.query_one("#division_s", Select).selection
            i_torik = self.query_one("#torikumi_s", Select).selection
            d_banzu = self.query_one(BanzukeWidget)
            d_basho = self.query_one(BashoWidget)
            d_torik = self.query_one(TorikumiWidget)

            if i_torik is None:
                d_torik.tdata = {}
                d_banzu.init_d = ""
                d_basho.ydata = self.sumo.basho(i_basho, 1)
                d_banzu.data = self.sumo.banzuke(i_basho, i_divis, 1)
                d_basho.refresh(layout=True)
                d_banzu.refresh(layout=True)
                d_banzu.parent.refresh(layout=True)
            else:
                d_banzu.init_d = ""
                d_banzu.data = {}
                d_basho.ydata = {}
                d_torik.tdata = self.sumo.torikumi(i_basho, i_divis, i_torik, 1)
                d_torik.refresh(layout=True)
                d_torik.parent.refresh(layout=True)
            for _ in range(13):
                if not self._t_thread:
                    return
                time.sleep(5)

    def on_mount(self) -> None:
        self.__basho = ""
        self.__division = ""
        ftheme = next(self.themes)
        if os.path.exists(f"{os.getenv('HOME', '~')}/.ozeki"):
            with open(f"{os.getenv('HOME', '~')}/.ozeki", "r") as fp:
                theme_name = fp.read().strip()
                for theme in THEMES:
                    if theme["theme"].name == theme_name:
                        ftheme = theme
                        self.register_theme(ftheme["theme"])
                        break
        while True:
            ntheme = next(self.themes)
            if ntheme["theme"].name != ftheme["theme"].name:
                self.register_theme(ntheme["theme"])
            else:
                ftheme = ntheme
                break
        self.register_theme(ftheme["theme"])
        self.theme = ftheme["theme"].name

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

        yield Header(name="Ozeki", id="header", icon="🌸", show_clock=True)

        with Horizontal(id="drop-down"):
            years = list(self.bashos.keys())
            years.sort()
            years.reverse()
            yield Select(
                ((self.bashos[year], str(year)) for year in years),
                prompt="Select Basho",
                id="basho_s",
            )
            yield Select(
                ((div, div) for div in self.divisions),
                prompt="Select Division",
                id="division_s",
            )
            yield Select(
                ((f"Day #{day:02d}", str(day)) for day in range(1, 16)),
                prompt="Select Torikumi Day",
                id="torikumi_s",
            )

        with VerticalScroll(id="main-content"):
            yield BashoWidget(id="basho")
            yield BanzukeWidget(id="banzuke")
            yield TorikumiWidget(id="torikumi")
        yield Footer()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        d_banzu = self.query_one(BanzukeWidget)
        d_basho = self.query_one(BashoWidget)
        d_torik = self.query_one(TorikumiWidget)

        self._t_thread = False
        reset = False
        if event.select.id == "basho_s":
            self.__basho = event.value
            reset = True
        elif event.select.id == "division_s":
            self.__division = event.value
            reset = True

        if len(str(self.__basho)) < 1 or len(str(self.__division)) < 1:
            return

        if len(str(self.__basho)) > 0 and len(str(self.__division)) > 0 and reset:
            d_torik.tdata = {}
            d_banzu.init_d = ""
            d_basho.ydata = self.sumo.basho(self.__basho)
            d_banzu.data = self.sumo.banzuke(self.__basho, self.__division)
            reset = False
        elif len(str(self.__basho)) > 0 and len(str(self.__division)) > 0 and not reset:
            d_banzu.init_d = ""
            d_banzu.data = {}
            d_basho.ydata = {}
            d_torik.tdata = self.sumo.torikumi(
                self.__basho, self.__division, event.value
            )
            reset = True
