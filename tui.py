import threading
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.containers import Horizontal, HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, Checkbox, Digits, Footer, Header, Label
from server import adam6050_coils, start_server


class CustomCheckbox(Checkbox):
    BUTTON_LEFT = ""
    BUTTON_INNER = ""
    BUTTON_RIGHT = ""
    def toggle(self) -> None:
        super().toggle()

class InputsLeftColumn(VerticalGroup):
    def compose(self) -> ComposeResult:
        for i in range(6):
            yield InputRow(i)

class InputsRightColumn(VerticalGroup):
    def compose(self) -> ComposeResult:
        for i in range(6, 12):
            yield InputRow(i)

class OutputsColumn(VerticalGroup):
    def compose(self) -> ComposeResult:
        for i in range(6):
            yield OutputRow(i)

class InputRow(HorizontalGroup):
    def __init__(self, number: int):
        super().__init__()
        self.number = number
    def compose(self) -> ComposeResult:
        yield CustomCheckbox(f"DI {self.number}", True, id=f"DI{self.number}")

class OutputRow(HorizontalGroup):
    def __init__(self, number: int):
        super().__init__()
        self.number = number
    def compose(self) -> ComposeResult:
        yield CustomCheckbox(f"DO {self.number}", False, id=f"DO{self.number}")

class Adam6050Emulator(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "tui.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Horizontal(
            InputsLeftColumn(),
            InputsRightColumn(),
            OutputsColumn(),
            id="IOColumns"
        )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def on_checkbox_changed(self, event: CustomCheckbox.Changed) -> None:
        checkbox = event.checkbox
        if checkbox.id[1] == "I":
            adam6050_coils[int(checkbox.id[2])] = 1 if checkbox.value else 0
        elif checkbox.id[1] == "O":
            adam6050_coils[int(checkbox.id[2]) + 12] = 1 if checkbox.value else 0
        print(adam6050_coils)

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    app = Adam6050Emulator()
    app.run()
