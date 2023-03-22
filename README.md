# Keep Windows Alive

Simple python GUI app to prevent windows from entering sleep mode. it does so by increase and decrease the system volume every 5 minutes.

## Features

- Trick windows to never sleep.
- UI interface using PyQt5 package.
- Windows volume control using PyWin32 package.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyQt5 and PyWin32 packages.

```bash
pip install PyQt5, PyWin32
```

## Demo

to create demo app install PyInstaller package.

```bash
pip install PyInstaller
```

and run the following command:

```bash
pyinstaller --noconsole --onefile ./KeepAlive/__init__.py --demo
```

## Tests

run tests using:

```bash
python -m unittest tests
```

## License

This project is licensed under the MIT License.