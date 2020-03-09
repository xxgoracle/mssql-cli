# macOS Installation

## Compatibility

### Supported OS Versions:
mssql-cli supports macOS (x64) 10.12 and up.

### Python Installation
Although Python 2.7 is bundled with macOS, it is recommended to install Python 3, as version 2.7 has been officially deprecated by Python.

The latest Python installation may be downloaded from [Python's website](https://www.python.org/downloads/).

## Official mssql-cli Installation
> Note: your path to Python may be different from the listed command. For example, instead of `python` you may need to call `python3`.

mssql-cli is installed using `pip`. Use the instructions below if Python 3 is installed, or jump to the [next section](#python-27-installation) for Python 2.7:
```sh
# Install pip
sudo easy_install pip

# Update pip
python -m pip install --upgrade pip

# Install mssql-cli
sudo pip install mssql-cli

# Run mssql-cli
mssql-cli
```

## Installing with Direct Link
Alternatively, mssql-cli may be installed by pointing directly to the wheel file:

```sh
sudo pip install --pre --no-cache https://files.pythonhosted.org/packages/43/5d/c9af6aec5b491e7b0c5ccf00b4b8062282d6c4cfb4c0417891bd6013e299/mssql_cli-0.15.0-py2.py3-none-macosx_10_11_intel.whl
```

## Uninstall mssql-cli
Use `pip` to remove mssql-cli:
```sh
sudo pip uninstall mssql-cli
```
