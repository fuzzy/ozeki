# -*- coding: utf-8 -*-
import dateutil
import calendar
from datetime import datetime

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input
from textual.widgets import Rule, DataTable
from textual.containers import Vertical, Horizontal
from textual.containers import VerticalScroll

from .client import SumoAPI


class RikishiScreen(ModalScreen):

    api = SumoAPI()
    DEFAULT_CSS = """
    RikishiScreen {
        align: center middle;
        layer: overlay;
    }

    RikishiScreen > Vertical {
        width: 70%;
        height: 80%;
        border: thick $foreground 80%;
        background: $surface;
        align: center middle;
    }

    RikishiScreen > Vertical > Label {
        width: 100%;
        content-align-horizontal: center;
        margin-top: 1;
        margin-bottom: 1;
    }

    RikishiScreen > Vertical > Horizontal {
        width: 100%;
        height: auto;
        padding-left: 1;
        padding-right: 2;
    }

    RikishiScreen > Vertical > Horizontal > Rule {
        width: 100%;
        padding-bottom: 1;
        color: $primary;
    }

    RikishiScreen > Vertical > Horizontal > Input {
        width: 1fr;
    }

    RikishiScreen > Vertical > Horizontal > Button { }

    RikishiScreen > Vertical > VerticalScroll {
        width: 100%;
        height: 1fr;
    }
    
    RikishiScreen > Vertical > VerticalScroll > DataTable {
        width: 1fr;
        padding-right: 2;
        padding-left: 2;
        padding-bottom: 1;
    }

    .twenty_five_lines {
        height: 25;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Input(
                    placeholder="Enter Rikishi Name and hit <ENTER>", id="rikishi_name"
                )
                yield Button("Exit", id="no", variant="error")
            yield Rule(line_style="double")
            yield VerticalScroll(id="data_box")
            # yield DataTable(id="rank_history", show_header=False, zebra_stripes=True)

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def rikishi_lookup(self, event: Input.Submitted) -> None:
        rikishi_name = event.value.strip()
        data = self.api.rikishi_by_name(rikishi_name)
        # tble.clear(columns=True)
        idx = 0
        parent = self.query_one("#data_box", VerticalScroll)
        parent.remove_children()
        for records in data.get("records", []):
            if records.get("shikonaEn").lower() == rikishi_name.lower():
                if idx > 0:
                    parent.mount(Rule())
                # details
                birth = dateutil.parser.isoparse(records.get("birthDate", ""))
                age = (datetime.now().year - birth.year) if birth else "Unknown"
                debut = datetime.strptime(records.get("debut", ""), "%Y%m")
                intai = (
                    dateutil.parser.isoparse(records["intai"])
                    if records.get("intai", False)
                    else None
                )
                hometown = records.get("shusshin", "Unknown")
                heya = records.get("heya", "Unknown")
                shikonas = {
                    "en": records.get("shikonaEn", "Unknown"),
                    "jp": records.get("shikonaJp", "Unknown"),
                }
                rank = records.get("currentRank", "Retired")
                height = records.get("height", "Unknown")
                weight = records.get("weight", "Unknown")

                table_a = DataTable(
                    id=f"{rikishi_name.lower()}_details_{idx}",
                    show_header=False,
                    show_cursor=False,
                    zebra_stripes=False,
                )
                table_a.add_columns("Attribute", "Value")
                table_a.add_rows(
                    (
                        ("Current Rank", rank),
                        (
                            "Height",
                            f"{height}cm / {int((height * 0.3937) // 12)}'{int((height * 0.3937) % 12)}\"",
                        ),
                        ("Weight", f"{weight}kg / {int(weight * 2.20462)}lb"),
                        (
                            "Birth Date",
                            f'{birth.strftime("%Y-%m-%d") if birth else "Unknown"} (Age: {age})',
                        ),
                        ("Debut", debut.strftime("%Y-%m") if debut else "Unknown"),
                        (
                            "Retired",
                            intai.strftime("%Y-%m-%d") if intai else "*still active*",
                        ),
                        ("Hometown", hometown),
                        ("Heya", heya),
                        ("Shikona (EN)", shikonas["en"]),
                        ("Shikona (JA)", shikonas["jp"]),
                    )
                )
                parent.mount(Label("Rikishi Detail"))
                parent.mount(Label(""))
                parent.mount(table_a)
                parent.mount(Label("Measurement History"))
                parent.mount(Label(""))

                table_b = DataTable(
                    id=f"{rikishi_name.lower()}_measurement_history_{idx}",
                    show_header=False,
                    show_cursor=False,
                    zebra_stripes=False,
                )
                table_b.add_columns(*("Basho", "Height", "Weight"))
                recs = [
                    (
                        f'{calendar.month_name[datetime.strptime(datum.get("bashoId", "Unknown"), "%Y%m").month][0:3]} {datetime.strptime(datum.get("bashoId", "Unknown"), "%Y%m").year}',
                        f"{datum.get('height', 0)}cm / {int(datum.get('height', 0) * 0.3937) // 12}'{int(datum.get('height', 0) * 0.3937) % 12}\"",
                        f"{datum.get('weight', 0)}kg / {int(datum.get('weight', 0) * 2.20462)}lb",
                    )
                    for datum in records.get("measurementHistory", [])
                ]
                recs.reverse()
                table_b.add_rows(recs)

                parent.mount(table_b)

                parent.mount(Label("Rank History"))
                parent.mount(Label(""))
                # table widget
                table_c = DataTable(
                    id=f"{rikishi_name.lower()}_rank_history_{idx}",
                    show_header=False,
                    show_cursor=False,
                    zebra_stripes=False,
                )
                table_c.add_columns(*("Basho", "Rank", "Age"))
                parent.mount(table_c)
                recs = [
                    (
                        f'{calendar.month_name[datetime.strptime(datum.get("bashoId", "Unknown"), "%Y%m").month][0:3]} {datetime.strptime(datum.get("bashoId", "Unknown"), "%Y%m").year}',
                        datum.get("rank", "Unknown"),
                        f'Age: {datetime.strptime(datum.get("bashoId", ""), "%Y%m").year - birth.year}',
                    )
                    for datum in records.get("rankHistory", [])
                ]
                recs.reverse()
                table_c.add_rows(recs)
                parent.mount(Label(""))

            idx += 1

    @on(Button.Pressed, "#no")
    def back_to_app(self) -> None:
        self.app.pop_screen()
