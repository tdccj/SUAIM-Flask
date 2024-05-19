# coding = utf-8
class ReturnError(Exception):
    def __str__(self):
        return "Invalid return value"
