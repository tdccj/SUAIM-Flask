# coding = utf-8
from lib.Database import DB


db = DB("test.db")
db.create_table("test_table")
db.create_item("testname","testtype",1)
db.show_data_all()
