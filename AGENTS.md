# MCEdit-Unified

Minecraft world editor. Single-package Python app, no monorepo.

## Entrypoints

- **GUI**: `python mcedit.py` (or `./mcedit.sh` on Linux). `mcedit.py:main()`.
- **CLI**: `python mce.py` for headless world editing commands.

## Key directories

| Path | Purpose |
|---|---|
| `albow/` | Custom GUI widget toolkit (forked Albow, pygame-based) |
| `pymclevel/` | Minecraft world I/O library (NBT, Anvil, Pocket, schematics) |
| `viewports/` | 3D camera and chunk view renderers (`camera.py`) |
| `editortools/` | Tool implementations: select, clone, brush, fill, filter, player, nbt |
| `panels/` | UI panels for editor tools |
| `pymclevel/test/` | pytest-based tests (library only, no GUI tests) |
| `lang/` | Translation files (`.trn` format, see `albow/README.txt`) |

## Dependencies

Python 3.12, pygame ≥2.5, PyOpenGL ≥3.1.7, numpy ≥1.26, Pillow ≥10.3, Cython ≥3.0.
See `requirements.txt`. Optional: ftputil, pyclark.

## Testing

```sh
cd pymclevel && python -m pytest test/
```

Or to test NBT specifically (with and without C extension):
```sh
cd pymclevel && bash run_nbt_tests.sh
```

Tests exist only for `pymclevel/`. No tests for the GUI.

## Cython extensions

Build with `python setup.py nbt` (for `pymclevel/_nbt`) or `python setup.py png` (for `cpngfilters`), or `python setup.py all` for both. Verify with `python setuptest.py`.

## Pygame 2 / SDL2 quirks

- `pygame.key.get_pressed()` returns a `ScancodeWrapper` indexed by **scancodes** (0-511), not keycodes.
- SDL2 key constants like `K_LCTRL`, `K_LSHIFT` are large ints (1073742048+) that **cannot** safely index the 512-element array.
- Use `key.get_mods() & KMOD_LCTRL` instead of `allKeys[K_LCTRL]`.
- `key.name(scancode)` returns empty strings for most scancodes. Convert names to keycodes with `key.key_code(name)`, then check `allKeys[keycode]`.
- See `albow/root.py:137-164` (`getKeycode`) for the pattern.

## Python 3 `map()` pitfalls

`map()` returns an iterator, not a list. This crashes when the result is:
- concatenated with `+` (list + map)
- passed to `numpy.sum()`
- indexed or sliced

Fix: wrap in `list(map(...))` where the result is used as a sequence.

## Config

- File: `~/.mcedit/MCEdit/mcedit.ini`
- Loaded by `config.py` using RawConfigParser.
- Key bindings stored under `[Keys]` section, names like `W`, `Shift`, `Lshift`, `Space`.
- `pygame.key.key_code()` doesn't accept strings like `"Shift"`, `"Lshift"`, `"Ctrl"` directly — these need mapping (see `getKeycode`).

## Code style

- BSD-3-Clause license (David Rio Vierra).
- Translation support: text strings use `from albow.translate import _` for `.trn` file lookups.
- Logging via `logging.getLogger(__name__)`.
- No type hints, no linter config, no formatter config.
