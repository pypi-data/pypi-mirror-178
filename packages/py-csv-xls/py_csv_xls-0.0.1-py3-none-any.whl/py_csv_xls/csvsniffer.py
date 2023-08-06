import csv
import os
import typing
from pathlib import Path

from .exception import PyCsvXlsException


class CSVSniffer:
    def __init__(self, file_startswith: str, main_path: str, fields: typing.List):
        self.__is_file: bool = os.path.isfile(main_path)
        self.__start_row_flag: bool = False
        self.__file_startswith: str = file_startswith
        self.__main_path: str = (
            Path(main_path).parent.absolute() if self.__is_file else main_path
        )
        self.__fields: typing.List = fields

    def get_files_with_lines_for_set_dir(self) -> typing.List:
        try:
            return list(self.__main_dir_sniffer())
        except Exception as e:
            raise PyCsvXlsException(msg=f"{self.__class__.__name__} error", exc=e)

    @property
    def is_file(self) -> bool:
        return self.__is_file

    def __main_dir_sniffer(self) -> typing.Generator:
        if not os.path.exists(self.__main_path) or not self.__is_file:
            raise NotADirectoryError
        for dir_path, _, files_list in os.walk(self.__main_path):
            yield from self.__files_sniffer_by_pattern(dir_path, files_list)

    def __files_sniffer_by_pattern(
        self, curr_dir_path: str, files_list: typing.List[str]
    ) -> typing.Generator:
        for file_name in files_list:
            if file_name.startswith(self.__file_startswith) and file_name.endswith(
                ".csv"
            ):
                self.__start_row_flag = False
                lines = self.__csv_file_parser(os.path.join(curr_dir_path, file_name))
                yield {file_name: list(lines)}

    def __csv_file_parser(self, abs_file_path: str) -> typing.Generator:
        with open(abs_file_path, "r", encoding="utf-8") as csv_file:
            for csv_line in csv.reader(csv_file):
                if csv_line == self.__fields:
                    self.__start_row_flag = True
                if self.__start_row_flag is True:
                    yield csv_line
