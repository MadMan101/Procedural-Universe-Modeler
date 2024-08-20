import sqlite3
import os
import random as r

if os.path.isfile("universe.db"):
    os.remove("universe.db")
con = sqlite3.connect("universe.db")
cur = con.cursor()

