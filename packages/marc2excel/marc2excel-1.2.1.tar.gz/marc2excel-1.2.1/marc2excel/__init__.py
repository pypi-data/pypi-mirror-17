# -*- coding: utf8 -*-
"""Main package for marc2excel.

Exports the following convenience functions:
    * marc2excel: convert MARC to Excel
    * excel2marc: convert Excel to MARC
"""

from .main import Converter

__author__ = "Alexander Mendes"
__license__ = "BSD License"
__version__ = "1.2.1"


def marc2excel(path, out_path, silent=True, force_utf8=False):
    """Convert MARC to Excel.

    :param path: Path to the MARC file.
    :param out_path: Path to save the Excel spreadsheet.
    :param silent: Don't display CLI progress.
    :param force_utf8: Force UTF8 encoding.
    """
    converter = Converter(silent)
    converter.marc2excel(path, out_path, force_utf8=force_utf8)


def excel2marc(path, out_path, sheet=0, silent=True, force_utf8=False):
    """Convert Excel to MARC.

    :param path: Path to the Excel spreadsheet.
    :param out_path: Path to save the MARC file.
    :param sheet: The index of the sheet from which to extract data.
    :param silent: Don't display CLI progress.
    :param force_utf8: Force UTF8 encoding.
    """
    converter = Converter(silent)
    converter.excel2marc(path, out_path, sheet=sheet, force_utf8=force_utf8)
