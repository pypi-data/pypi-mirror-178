# py-csv-xls

<p align="center">
<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Converter from csv format to xls

### Installation
[PYPI](https://pypi.org/project/py-csv-xls/)
```shell script
pip install py-csv-xls
```

### Example
```python
from py_csv_xls import CSVSniffer, ExcelWorker, PyCsvXlsException

file_lines = CSVSniffer(
    main_path="/abs/path/to/ur/csv/or/dir",
).get_dir_files_with_lines()

ExcelWorker(
    workbook_name="/abs/path/to/ur/xl/without/extension",
    workbook_extension=".xls",
    want_cleared=True,
).fill_workbook(all_data=file_lines)
```