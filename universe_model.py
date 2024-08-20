import sqlite3
import os
import random as r

factions = {
    "Chinese": {
        "prefixes": ["Qing", "Han", "Shan", "Jin", "Wei", "Tai"],
        "suffixes": [" Dao", " Guo", " Zhu", " Ming", " Shen", " Lu"]
    },
    "Arab": {
        "prefixes": ["Al ", "Nur", "Qadir", "Rasha", "Zahir", "Faran"],
        "suffixes": ["shahr", "khalif", "marr", "dari", "zuri"]
    },
    "Roman": {
        "prefixes": ["Imperia", "Nova", "Aeternus", "Magnus", "Victor", "Aurelia"],
        "suffixes": [" Dominium", " Rex", " Civitas", " Legio", " Aetern", " Nova"]
    },
    "Norse": {
        "prefixes": ["Val", "Ragn", "Thor", "Ulf", "Ygg", "Fenr"],
        "suffixes": ["heim", "fjall", "gard", "skald", "drakkar", "skorn"]
    },
    "Indian": {
        "prefixes": ["Raj", "Chandra ", "Veda", "Ashoka ", "Soma", "Agni"],
        "suffixes": ["maya", "jaya", "loka", "varsha", "asura", "putra"]
    },
    "African": {
        "prefixes": ["Kongo", "Zulu", "Mali", "Nkrum", "Ashan", "Nyasa"],
        "suffixes": ["bara", "mara", "lamba", "sawa", "ganda", "ngala"]
    }
}
cultures = ["Chinese", "Arab", "Roman", "Norse", "Indian", "African"]

if os.path.isfile("universe.db"):
    os.remove("universe.db")

class DatabaseHandler:
    def __init__(self, db_name="universe.db"):
        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sectors (
            sectorID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            faction TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS systems (
            systemID INTEGER PRIMARY KEY AUTOINCREMENT,
            sectorID INTEGER,
            name TEXT,
            faction TEXT,
            rawMult REAL,
            energyMult REAL,
            industrialMult REAL,
            medicalMult REAL,
            weaponMult REAL,
            technologyMult REAL,
            foodMult REAL,
            FOREIGN KEY (sectorID) REFERENCES sectors(sectorID)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
            tradeID INTEGER PRIMARY KEY AUTOINCREMENT,
            price INTEGER,
            category TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bodies (
            bodyID INTEGER PRIMARY KEY AUTOINCREMENT,
            systemID INTEGER,
            name TEXT,
            station INTEGER,
            rings INTEGER,
            type TEXT,
            FOREIGN KEY (systemID) REFERENCES systems(systemID)
            )
        ''')

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self, query, params=None):
        self.execute_query(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

class LoreGenerator:
    def generate_factions(self):
        culture = r.choice(cultures)
        print(r.choice(factions[culture]["prefixes"]) + r.choice(factions[culture]["suffixes"]))

db = DatabaseHandler()

lg = LoreGenerator()
for i in range(30):
    lg.generate_factions()