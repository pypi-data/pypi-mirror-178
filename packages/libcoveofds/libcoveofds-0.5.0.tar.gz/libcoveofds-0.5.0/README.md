# Lib Cove OFDS

See https://libcoveofds.readthedocs.io/en/latest/ for docs.

## Command line

### Installation

Installation from this git repo:

```bash
git clone https://github.com/Open-Telecoms-Data/lib-cove-ofds.git
cd lib-cove-ofds
python3 -m venv .ve
source .ve/bin/activate
pip install -e .
```

### Running the command line tool

Call `libcoveofds` and pass --help to see options.

```bash
libcoveofds --help 
libcoveofds jsontogeojson --help
```
    
### Running tests

```bash
python -m pytest
```

For writing tests, look in `make_expected_test_data.sh` for a helper script.

### Code linting

Make sure dev dependencies are installed in your virtual environment:

```bash
pip install -e .[dev]
```

Then run:

```bash
isort libcoveofds/ libcove2/ tests/ setup.py
black libcoveofds/ libcove2/ tests/ setup.py
flake8 libcoveofds/ libcove2/ tests/ setup.py
mypy --install-types --non-interactive -p  libcoveofds
```
