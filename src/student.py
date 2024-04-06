import os
from dataclasses import dataclass
from typing import final
from pandas import Series


@final
@dataclass
class Student:
    first_name: str
    last_name: str
    asurite: str
    github_username: str
    homework_directory: str
    javascripts: list[str]


    def __init__(self, row: Series, homework_directory: str) -> None:
        self.first_name = row['first_name']
        self.last_name = row['last_name']
        self.asurite = row['asurite']
        self.github_username = row['github_username']
        self.homework_directory = homework_directory
        self.javascripts = self.__filter_files__(homework_directory, 'js', ['.git', 'node_modules'])


    def __filter_files__(self, homework_directory: str, extension: str, exclude_subfolders: list[str]) -> list[str]:
        filtered_files: list[str] = []
        for path, subfolders, files in os.walk(homework_directory):
            for exclude_subfolder in exclude_subfolders:
                if exclude_subfolder in subfolders:
                    subfolders.remove(exclude_subfolder)
            for name in files:
                if name.endswith(extension):
                    filtered_files.append(os.path.join(path, name))
        return filtered_files    


    def __hash__(self) -> int:
        return self.asurite.__hash__()
