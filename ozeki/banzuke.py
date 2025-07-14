from rich.table import Table
from textual.widget import Widget
from textual.widgets import Footer
from textual.app import ComposeResult, App
from textual.reactive import reactive

from ozeki.client import SumoAPI


class BanzukeWidget(Widget):

    data = reactive({})
    DEFAULT_CSS = "Table { border: none; height: auto; }"

    def _record(self, d=[]):
        record = {"win": 0, "loss": 0}
        for n in d:
            result = n.get("result", "")
            if result == "win":
                record["win"] += 1
            elif result == "loss":
                record["loss"] += 1
        col = ""
        if record["win"] > record["loss"]:
            col = "bold green"
        elif record["win"] > 0 and record["win"] == record["loss"]:
            col = "bold yellow"
        elif record["win"] < record["loss"]:
            col = "bold red"
        beg = f"[{col}]" if len(col) > 0 else ""
        end = f"[/{col}]" if len(col) > 0 else ""
        return f'{beg}{record["win"]} / {record["loss"]}{end}'

    def render(self) -> None:
        self.table = Table(title="Banzuke", box=None, show_header=True)
        idx = 0
        for c in (
            "East",
            "Shikona (EN)",
            "Shikona (JP)",
            "Rank",
            " ",
            "Rank",
            "Shikona (JP)",
            "Shikona (EN)",
            "West",
        ):
            if idx < 3:
                just = "left"
            elif idx == 3:
                just = "center"
            elif idx > 3:
                just = "right"
            self.table.add_column(c, justify=just)
            idx += 1

        for n in range(0, len(self.data.get("east", []))):
            edata = self.data.get("east", [])[n]
            if len(self.data.get("west", [])) > n:
                wdata = self.data.get("west", [])[n]
                west = {
                    "en": wdata.get("shikonaEn", " "),
                    "jp": wdata.get("shikonaJp", " "),
                    "rank": wdata.get("rank", " "),
                }
            else:
                wdata = {}
                west = {
                    "en": wdata.get("shikonaEn", " "),
                    "jp": wdata.get("shikonaJp", " "),
                    "rank": wdata.get("rank", " "),
                }
            east = {
                "en": edata.get("shikonaEn", " "),
                "jp": edata.get("shikonaJp", " "),
                "rank": edata.get("rank", " "),
            }
            self.table.add_row(
                self._record(edata.get("record", [])),
                east["en"],
                east["jp"],
                " ".join(east["rank"].split()[0:2]),
                " ",
                " ".join(west["rank"].split()[0:2]),
                west["jp"],
                west["en"],
                self._record(wdata.get("record", [])),
            )
        return self.table


class TestBanzukeWidgetApp(App):

    banzuke = BanzukeWidget()
    sumo = SumoAPI()
    BINDINGS = [("ctrl+q", "quit", "Quit"), ("ctrl+d", "change_data", "Change data")]

    def compose(self) -> ComposeResult:
        yield self.banzuke
        yield Footer()

    def on_mount(self):
        self.banzuke.data = self.sumo.banzuke("202507", "Makuuchi")

    def action_change_data(self):
        self.banzuke.data = self.sumo.banzuke("202505", "Makuuchi")


if __name__ == "__main__":
    obj = TestBanzukeWidgetApp()
    obj.run()
