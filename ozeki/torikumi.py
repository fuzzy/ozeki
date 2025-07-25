# 3rd party
from rich import box
from rich.table import Table
from rich.console import Group

from textual.widget import Widget
from textual.reactive import reactive


class TorikumiWidget(Widget):

    tdata = reactive({})
    DEFAULT_CSS = "Table { border: none; height: 1fr; width: 1fr; }"

    def get_content_height(self, container, viewport, console) -> int:
        retv = 0
        if (
            len(self.tdata.get("torikumi", [])) > 0
            and self.tdata["torikumi"][0].get("day", 0) > 0
        ):
            retv += 5
        for x in self.tdata.get("torikumi", []):
            if x.get("day", 0) > 0 and x.get("winnerId", 0) != 0:
                retv += 1
        return retv

    def render(self) -> None:
        widgets = []
        if (
            len(self.tdata.get("torikumi", [])) > 0
            and self.tdata["torikumi"][0].get("winnerId", 0) != 0
        ):
            day = Table(
                title=f"Day #{self.tdata['torikumi'][0]['day']:02d}",
                expand=True,
                title_justify="full",
                box=box.SIMPLE,
                show_header=True,
            )
            idx = 0

            for n in (
                "East",
                "Shikona",
                "Rank",
                "Kimarite",
                "Rank",
                "Shikona",
                "West",
            ):
                if idx < 3:
                    just = "left"
                elif idx == 3:
                    just = "center"
                elif idx > 3:
                    just = "right"
                day.add_column(n, justify=just)
                idx += 1

            for n in self.tdata.get("torikumi", []):
                eflag = wflag = ""
                if n.get("winnerId", True) == n.get("eastId", False):
                    east = f"[green]{n.get('eastShikona', 'UNKNOWN')}[/green]"
                    west = f"[red]{n.get('westShikona', 'UNKNOWN')}[/red]"
                    eflag = "🏅"
                elif n.get("winnerId", True) == n.get("westId", True):
                    east = f"[red]{n.get('eastShikona', 'UNKNONW')}[/red]"
                    west = f"[green]{n.get('westShikona', 'UNKNOWN')}[/green]"
                    wflag = "🏅"
                else:
                    east = f"[yellow]{n.get('eastShikona', 'UNKNONW')}[/yellow]"
                    west = f"[yellow]{n.get('westShikona', 'UNKNOWN')}[/yellow]"

                day.add_row(
                    eflag,
                    east,
                    " ".join(n.get("eastRank", "UNKNOWN").split()[0:2]),
                    n.get("kimarite", "UNKNOWN"),
                    " ".join(n.get("westRank", "UNKNOWN").split()[0:2]),
                    west,
                    wflag,
                )

            widgets.append(day)

        return Group(*widgets)
