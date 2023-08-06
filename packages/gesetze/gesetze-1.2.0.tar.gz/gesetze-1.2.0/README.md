# py-gesetze
[![License](https://badgen.net/badge/license/GPL/blue)](https://codeberg.org/S1SYPHOS/py-gesetze/src/branch/main/LICENSE) [![PyPI](https://badgen.net/pypi/v/gesetze)](https://pypi.org/project/gesetze) [![Build](https://ci.codeberg.org/api/badges/S1SYPHOS/py-gesetze/status.svg)](https://codeberg.org/S1SYPHOS/py-gesetze/issues)

Linking german legal norms, dependency-free & GDPR-friendly. `py-gesetze` automatically transforms legal references into `a` tags - batteries included.

This project is a Python port of the PHP library [`php-gesetze`](https://github.com/S1SYPHOS/php-gesetze).


## Installation

It's available from [PyPi](https://pypi.org/project/gesetze) using `pip`:

```text
pip install gesetze
```


## Getting started

Using this library is straightforward.


### Commandline

Pretty much self-explanatory - otherwise, `--help` is your friend:

```text
$ gesetze --help
Usage: gesetze [OPTIONS] COMMAND [ARGS]...

  Utilities for indexing & analyzing german legal norms

Options:
  -v, --verbose  Enable verbose mode.
  --version      Show the version and exit.
  --help         Show this message and exit.

Commands:
  analyze  Analyzes legal norm
  build    Builds index
  clear    Clears download cache
```


### Package

The underlying module may also be used directly:

```python
from gesetze import Gesetz, analyze

# Initialize it
obj = Gesetz()

# Configure it
obj.title = 'normal'

# Convert legal references
print(obj.gesetzify('This text references Art. 1 GG.'))

# "This text references <a class="hover:underline" href="https://www.gesetze-im-internet.de/gg/art_1.html" title="Grundgesetz für die Bundesrepublik Deutschland">Art. 1 GG</a>."

print(analyze('§ 433 Abs. 2 BGB'))

# {'norm': '433', 'absatz': '2', 'gesetz': 'BGB'}
```


## Usage

### Class `Gesetz`

#### `__init__(drivers: typing.Union[str, list])`

`drivers` controls the providers (and their respective order) to be used, either `str` or `list`.

**Note:** This defaults to all available drivers, which is a good overall choice, simply because of the vast array of supported laws. However, possible values are `gesetze`, `'dejure'`, `'buzer'` and `'lexparency'`.


#### `gesetzify(string: str, callback: typing.Callable) -> str`

Transforms legal references into HTML link tags

**Note:** For more flexibility, you may use your own `callback` method as second parameter of `gesetzify`. Callbacks are being passed the [`re.Match`](https://docs.python.org/3/library/re.html#match-objects) object representing matched legal norms. This way, you could highlight them using `<strong>` tags instead of converting them into `a` tags. Default: `obj.linkify`

Example: Inside the callback function, the `match` for '§ 433 Abs. 2 BGB' (`match.group(0)`) would give a dictionary like `{'norm': '433', 'absatz': '2', 'satz': None, 'nr': None, 'lit': None, 'gesetz': 'BGB'}` (eg using `match.groupdict()`).

**Note:** For convenience, a [Markdown](https://en.wikipedia.org/wiki/Markdown) callback is included and may be used like this: `obj.gesetzify('your-text', obj.markdownify)`


### Helpers

#### `analyze(string: str) -> dict`

Analyzes a single legal norm


#### `extract(string: str) -> list`

Extracts legal norms as list of strings


#### `roman2arabic(string: str)`

Converts roman numerals to arabic numerals (static method)


## Configuration

The `gesetzify` command may be configured through the following options:


### `obj.attributes (dict)`

Defines HTML attribute defaults. Default: `{'target': '_blank'}`


### `obj.title (False|str)`

Controls `title` attribute. Default: `False`

Possible values:

- `light`: abbreviated law (eg 'GG')
- `normal`: complete law (eg 'Grundgesetz')
- `full`: official heading (eg 'Art 45d Parlamentarisches Kontrollgremium')


## Contributing

If you want to get your hands dirty, this will download the repository and install `py-gesetze` along its dependencies inside a virtual environment, ready for action:

```bash
# Clone repository & change directory
git clone https://codeberg.org/S1SYPHOS/py-gesetze && cd py-gesetze

# Set up & activate virtualenv
poetry shell

# Install dependencies
poetry install
```


## Credits

This library is based on ..

- .. an adapted (and somewhat improved) version of the [`jura_regex`](https://github.com/kiersch/jura_regex) regex package by Philipp Kiersch.
- .. an adapted (and somewhat modified) version of the [`gesetze`](https://github.com/matejgrahovac/gesetze) crawler package by Matej Grahovac.


## Special Thanks

I'd like to thank everybody that's making free & open source software - you people are awesome. Also I'm always thankful for feedback and bug reports :)
