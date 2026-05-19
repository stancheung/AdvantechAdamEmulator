# AdvantechADAM Emulator

Python project emulating an ADVANTECH Adam-6050 I/O module over Modbus TCP.

## Run

| Component | Command |
|-----------|---------|
| Server only | `python server.py` (listens 0.0.0.0:502) |
| TUI + embedded server | `python tui.py` |
| Test client | `python client.py [host [port]]` |

- Python >=3.11, managed via `.venv` and `.python-version`. No declared dependencies in `pyproject.toml` yet (server uses stdlib socket; TUI uses `textual`).
- `start_server()` is a blocking call — the TUI spawns it as a thread (`tui.py:75`).

## Architecture

Three files, shared mutable state via module-level list:

| File | Role |
|------|------|
| `server.py` | Modbus TCP server. Handles function codes 01 (read coils), 05 (write single coil), 06 (write multiple coils). Exposes `adam6050_coils` (18-element list: 12 DI + 6 DO) and `start_server()`. |
| `tui.py` | Textual-based TUI. Binds checkbox changes to `adam6050_coils`. Reads CSS from `tui.tcss`. |
| `client.py` | Minimal Modbus client for testing (sends a single-coil write by default). |

The server runs as a simple blocking loop per-client (`server.py:11-44`). Keep-alive via periodic timeouts and per-connection timeout. No threading in the server itself.

## Gotchas

- `adam6050_coils` is shared mutable state between `server.py` and `tui.py`. TUI checkbox IDs are `DI{0-5}` and `DO{0-5}`, mapped to indices 0-5 and 12-17 respectively (`tui.py:69-71`).
- Function codes 03 (read holding registers) and 04 (read input registers) are stubs — they receive data but send no response.
- `construct_force_single_coil_status` only sets coil to `1`, never `0` (`server.py:101`).
- `construct_force_multi_coils_status` is a passthrough — it echoes back the request instead of applying coil values (`server.py:105-108`).
- TUI uses CSS from `tui.tcss` relative to working directory — ensure it exists when running.
