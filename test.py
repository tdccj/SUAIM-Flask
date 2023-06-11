# coding = utf-8
from lib.Database import DB


db = DB("test.db")
db.create("test_table")