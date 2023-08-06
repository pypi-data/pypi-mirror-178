# picsexl

<p align="center">
    <a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Converter from ics format to xls

### Installation
[PYPI](https://pypi.org/project/picsexl/)
```shell script
pip install picsexl
```

### Example
```python
    from datetime import datetime
    from picsexl import PIcsExl

    start = datetime.today()

    p = PIcsExl(
        file_path="/path/to/your/file.ics",
        mail_to="some.email@gmail.com",
        start_date=datetime(start.year, start.month, start.day, 0, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(start.year, start.month, start.day + 15, 23, 59, 59, tzinfo=timezone.utc),
    )
    p.run_sniff_and_write_ics_lines()
```