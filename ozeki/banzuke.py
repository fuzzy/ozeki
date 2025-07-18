# stdlib
import os

# 3rd party imports
from rich.table import Table
from rich.panel import Panel
from rich.console import Group, Console
from rich import box
from textual.widget import Widget
from textual.reactive import reactive
from textual.geometry import Size


class BanzukeWidget(Widget):

    init_d = reactive(
        """
[yellow]Ozeki[/yellow] - [bold]A data browser for sumo-api.com[/bold]
        
[bold]1.[/bold] Select the basho date at the top left
[bold]2.[/bold] Select the division at the bottom left
[bold]3.[/bold] Browse and enjoy

[yellow]Support[/yellow] ozeki by supporting [cyan][link=https://ko-fi.com/sumoapi]sumo-api.com (click here to open)[/link][/cyan].
They provide this data anonymously, and [bold]free[/bold] of charge to you
and I. Supporting them is to support Ozeki.
"""
    )
    data = reactive({})
    ydata = reactive({})
    tdata = reactive([])
    can_focus = True

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

    def get_content_height(
        self, container: Size, viewport: Size, console: Console
    ) -> int:
        retv = self.init_d.count("\n") + 2  # Count lines in initial message

        if self.data.get("east", []):
            retv += 5
            retv += len(self.data["east"])

        for n in self.tdata:
            if len(n.get("torikumi", [])) > 0 and n["torikumi"][0].get("day", 0) > 0:
                retv += 5
                for x in n.get("torikumi", []):
                    if x.get("day", 0) > 0 and x.get("winnerId", 0) != 0:
                        retv += 1

        return retv

    def render(self) -> None:
        widgets = []

        # Our default display / splash screen
        if len(self.init_d) > 0 and len(self.data.get("east", [])) == 0:
            widgets.append(Panel(self.init_d, box=box.SIMPLE, expand=False, padding=1))

        # Primary banzuke display
        if len(self.data.get("east", [])) > 0:
            self.table = Table(
                title="Banzuke",
                expand=True,
                title_justify="full",
                box=box.SIMPLE,
                show_header=True,
            )
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
                if idx < 4:
                    just = "left"
                elif idx == 4:
                    just = "center"
                elif idx > 4:
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
            widgets.append(self.table)

        # torikumi displays
        if len(self.tdata) > 0:
            for tdatum in self.tdata:
                if (
                    len(tdatum.get("torikumi", [])) > 0
                    and tdatum["torikumi"][0].get("winnerId", 0) != 0
                ):
                    day = Table(
                        title=f"Day #{tdatum['torikumi'][0]['day']:02d}",
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

                    for n in tdatum.get("torikumi", []):
                        eflag = wflag = ""
                        if n.get("winnerId", True) == n.get("eastId", False):
                            east = f"[green]{n.get('eastShikona', 'UNKNOWN')}[/green]"
                            west = f"[red]{n.get('westShikona', 'UNKNOWN')}[/red]"
                            eflag = "🏅"
                        else:
                            east = f"[red]{n.get('eastShikona', 'UNKNONW')}[/red]"
                            west = f"[green]{n.get('westShikona', 'UNKNOWN')}[/green]"
                            wflag = "🏅"

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

        self.refresh(layout=True)
        return Group(*widgets)
