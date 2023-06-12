# coding = utf-8
from lib.Database import DB
from lib.ScanCode import SC

dBName = "test.db"
dBTable = "test_table"

db = DB(dBName)
db.create_table(dBTable)
db.create_item("testname", "testtype", 1, "td")
db.update_item("name", 1, "one")
db.delete_item(2)
db.show_data_all()
db.show_data_id(3)
sc = SC(dBName, dBTable)
sc.create_code(dBName, dBTable, 1)
