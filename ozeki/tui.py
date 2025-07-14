# Stdlib
import time

# 3rd party
from rich.markdown import Markdown
from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label
from textual.widgets import MarkdownViewer, Header, Footer
from textual.containers import Horizontal

# Internal
from .client import SumoAPI

class SumoApp(App):

    CSS = """
Horizontal { height: 1fr; }
Vertical { width: 1fr; }
Markdown { text-align: center; }
MarkdownViewer { height: 5fr; }
ListView { border: tab white; }
"""
    BINDINGS = [('ctrl+q', 'quit', 'Quit')]
    bashos = {}
    months = (
        None,
        "January",
        None,
        "March",
        None,
        "May",
        None,
        "July",
        None,
        "September",
        None,
        "November",
        None,
    )
    divisions = ("Makuuchi", "Juryo", "Makushita", "Sandanme", "Jonidan", "Jonokuchi")
    init_data = """
# Ozeki (Sumo Stats Viewer)

Select a basho from the top left list, and a category from the top right. Browse the banzuke and get day by day breakdowns.
    """
    sumo = SumoAPI()

    def data_setup(self):
        self.bashos = {}
        for year in range(1960, 2026):
            for month in (1, 3, 5, 7, 9, 11):
                if year < time.gmtime().tm_year:
                    self.bashos[f"{year}{month:02d}"] = f"{self.months[month]} {year}"
                elif year == time.gmtime().tm_year and month <= time.gmtime().tm_mon:
                    self.bashos[f"{year}{month:02d}"] = f"{self.months[month]} {year}"

    def compose(self) -> ComposeResult:
        if len(self.bashos.keys()) == 0:
            self.data_setup()

        yield Header(id="header")
        with Horizontal(id="leftbar"):
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
        yield MarkdownViewer(
            self.init_data, show_table_of_contents=False, id="markdownviewer"
        )
        yield Footer(id="footer")

    def _entry(self, sumo, n):
        e_rec = {'win': 0, 'lose': 0}
        w_rec = {'win': 0, 'lose': 0}

        e_half = '| | | |'
        e_shi = {'en': '', 'jp': ''}
        
        if len(sumo['east'])-1 >= n:
            e_shi = {'en': sumo['east'][n].get('shikonaEn', ''), 'jp': sumo['east'][n].get('shikonaJp', '')}
            e_rnk = sumo['east'][n].get('rank', '')
            for x in sumo['east'][n].get('record', []):
                if x.get('result', '') == 'win':
                    e_rec['win'] += 1
                elif x.get('result', '').startswith('los'):
                    e_rec['lose'] += 1
            e_half = f"{e_shi['en']} - {e_shi['jp']} | **{e_rnk}**"

        w_half = ' | | |'
        w_shi = {'en': '', 'jp': ''}

        if len(sumo['west'])-1 >= n:
            w_shi = {'en': sumo['west'][n].get('shikonaEn', ''), 'jp': sumo['west'][n].get('shikonaJp', '')}
            w_rnk = sumo['west'][n].get('rank', '')
            for x in sumo['west'][n].get('record', []):
                if x.get('result', '') == 'win':
                    w_rec['win'] += 1
                elif x.get('result', '').startswith('los'):
                    w_rec['lose'] += 1
            w_half = f" {w_shi['en']} - {w_shi['jp']} | **{w_rnk}**"
        return f'| {e_half} | **{e_rec["win"]}** / `{e_rec["lose"]}` | {w_half} | **{w_rec["win"]}** / `{w_rec["lose"]}` |'

    def _day(self, basho, div, day):
        retv = [f'# Day {day}',
                '| Shikona | Rank |    | Rank | Shikona |',
                '| :------ | :--- | -- | ---: | ------: |']
        for tori in self.sumo.torikumi(basho, div, day).get('torikumi', []):
            if tori != {}:
                east = '|'
                west = ''
                if tori.get('eastShikona', '') == tori.get('winnerEn', ''):
                    east += f' (W) **{tori.get("eastShikona", "")}** | {tori.get("eastRank", "")} |'
                else:
                    east += f' {tori.get("eastShikona", "")} | {tori.get("eastRank", "")} |'
                east += f' {tori.get("kimarite", "")} |'
                if tori.get('westShikona', '') == tori.get('winnerEn', ''):
                    west += f' (W) **{tori.get("westShikona", "")}** | {tori.get("westRank", "")} |'
                else:
                    west += f' {tori.get("westShikona", "")} | {tori.get("westRank", "")} |'
                retv.append(f"{east}{west}")
        return retv
    
    def on_list_view_selected(self, event: ListView.Selected):
        w_basho = self.query_one("#bashos")
        w_divi = self.query_one("#divisions")

        basho = w_basho.children[w_basho.index].id.split("_")[1]
        divi = w_divi.children[w_divi.index].id

        data = ['# Banzuke',
                '| Shikona | Rank | Record | Shikona | Rank | Record |',
                '| :---- | -- | -- | ----: | -- | -- |']
        sumo = self.sumo.banzuke(basho, divi)
        for n in range(0, len(sumo['east'])):
            data.append(self._entry(sumo, n))
        for n in range(0, 15):
            for x in self._day(basho, divi, n+1):
                data.append(x)
        self.query_one(Markdown).update(f"{'\n'.join(data)}")
