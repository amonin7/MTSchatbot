import shelve
class SaveToFile:
    file = shelve.open("ourDB.db")