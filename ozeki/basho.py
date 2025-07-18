# 3rd party
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.console import Group

from textual.widget import Widget
from textual.reactive import reactive


class BashoWidget(Widget):

    ydata = reactive({})

    def get_content_height(self, container, viewport, console) -> int:
        retv = 0
        if self.ydata != {}:
            retv += 4

        xdata = len(self.ydata.get("yusho", [])) + len(
            self.ydata.get("specialPrizes", [])
        )
        if xdata > 0:
            retv += xdata + 5

        return retv

    def render(self) -> None:
        widgets = []
        if self.ydata != {}:
            widgets.append(
                Panel(
                    Group(
                        f"[yellow]Start Date[/yellow] [bold]{self.ydata.get('startDate', 'Unknown')}[/bold]",
                        f"[yellow]End Date[/yellow]   [bold]{self.ydata.get('endDate', 'Unknown')}[/bold]",
                    ),
                    box=box.SIMPLE,
                    expand=True,
                )
            )
        if len(self.ydata.get("yusho", [])) > 0:
            tbl = Table(
                title="Yusho and Special Prizes",
                box=box.SIMPLE,
                expand=True,
                title_justify="full",
                show_header=True,
            )
            for c in ("Shikona (EN)", "Shikona (JP)", "Yusho", "Special Prizes"):
                tbl.add_column(c, justify="left")
            for y in self.ydata.get("yusho", []):
                tbl.add_row(
                    y.get("shikonaEn", "UNKNOWN"),
                    y.get("shikonaJp", "UNKNOWN"),
                    "[green]" + y.get("type", "UNKNOWN") + "[/green]",
                    "",
                )
            for p in self.ydata.get("specialPrizes", []):
                tbl.add_row(
                    p.get("shikonaEn", "UNKNOWN"),
                    p.get("shikonaJp", "UNKNOWN"),
                    "",
                    "[cyan]" + p.get("type", "UNKNOWN") + "[/cyan]",
                )
            widgets.append(tbl)
        return Group(*widgets)
