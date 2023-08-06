import csv
import os
import typing
from pathlib import Path

from .exception import PyCsvXlsException


class CSVSniffer:
    def __init__(
        self,
        main_path: str,
        file_startswith: str = "",
        fields: typing.List = [],
    ):
        self.__is_file: bool = os.path.isfile(main_path)
        self.__file_startswith: str = file_startswith
        self.__main_path = main_path
        self.__main_dir_path: Path = (
            Path(self.__main_path).parent.absolute()
            if self.__is_file
            else self.__main_path
        )
        self.__fields: typing.List = fields
        self.__start_row_flag: bool = not self.__fields

    def get_dir_files_with_lines(self) -> typing.List:
        try:
            return list(self.__main_dir_sniffer())
        except Exception as e:
            raise PyCsvXlsException(msg=f"{self.__class__.__name__} error", exc=e)

    @property
    def is_file(self) -> bool:
        return self.__is_file

    @property
    def is_csv_file(self) -> bool:
        return self.__is_csv_file(file_name=self.__main_path, only_ext=True)

    def __main_dir_sniffer(self) -> typing.Generator:
        if not os.path.exists(self.__main_dir_path) or (
            not os.path.isdir(self.__main_dir_path) and not self.__is_file
        ):
            raise FileNotFoundError
        if self.__is_csv_file(file_name=self.__main_path, only_ext=True):
            yield {
                self.__main_path.split("/")[-1].rstrip(".csv"): list(
                    self.__csv_file_parser(self.__main_path)
                )
            }
        else:
            for dir_path, _, files_list in os.walk(self.__main_dir_path):
                yield from self.__files_sniffer_by_pattern(dir_path, files_list)

    def __is_csv_file(self, file_name: str, only_ext: bool = False) -> bool:
        if only_ext:
            return str(file_name).endswith(".csv")
        return str(file_name).startswith(self.__file_startswith) and file_name.endswith(
            ".csv"
        )

    def __files_sniffer_by_pattern(
        self, curr_dir_path: str, files_list: typing.List[str]
    ) -> typing.Generator:
        for file_name in files_list:
            if self.__is_csv_file(file_name=file_name):
                self.__start_row_flag = not self.__fields
                lines = self.__csv_file_parser(os.path.join(curr_dir_path, file_name))
                yield {file_name: list(lines)}

    def __csv_file_parser(self, abs_file_path: str) -> typing.Generator:
        with open(abs_file_path, "r", encoding="utf-8") as csv_file:
            for csv_line in csv.reader(csv_file):
                if not self.__start_row_flag and csv_line == self.__fields:
                    self.__start_row_flag = True
                if self.__start_row_flag is True:
                    yield csv_line
