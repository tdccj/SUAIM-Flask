# coding = utf-8

from src.Execute import Execute, Ignore, IgnoreList


class Item:

    def __init__(self, columns: list, execute: Execute, db_name: str):
        self.columns = columns
        self.Execute = execute
        self.db_name = db_name






