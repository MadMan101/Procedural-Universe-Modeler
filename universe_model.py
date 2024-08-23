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

sectors = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Xi", "Omicron", "Rho", "Sigma", "Tau", "Upsilon", "Psi", "Omega"]


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
            name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS factions (
            factionID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            relations INTEGER,
            rawMult REAL,
            energyMult REAL,
            industrialMult REAL,
            medicalMult REAL,
            weaponMult REAL,
            technologyMult REAL,
            foodMult REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS systems (
            systemID INTEGER PRIMARY KEY AUTOINCREMENT,
            sectorID INTEGER,
            factionID INTEGER,
            name TEXT,
            FOREIGN KEY (sectorID) REFERENCES sectors(sectorID),
            FOREIGN KEY (factionID) REFERENCES factions(factionID)
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
        self.con.commit()

    def fetch_all(self, query, params=None):
        self.execute_query(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.con.close()

class LoreGenerator:
    def __init__(self, db_handler):
        self.db = db_handler

    def generate_factions(self):
        culture = r.choice(cultures)
        factionName = r.choice(factions[culture]["prefixes"]) + r.choice(factions[culture]["suffixes"])
        existing_factions = [row[0] for row in self.db.fetch_all("SELECT name FROM factions")]
        while factionName in existing_factions:
            existing_factions = [row[0] for row in self.db.fetch_all("SELECT name FROM factions")]
            factionName = r.choice(factions[culture]["prefixes"]) + r.choice(factions[culture]["suffixes"])
        relations = r.randint(-100, 100)
        self.db.execute_query("INSERT INTO factions (name, relations, rawMult, energyMult, industrialMult, medicalMult, weaponMult, technologyMult, foodMult) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                              (factionName, relations, round(r.uniform(0.6, 1.9) * ((100+relations)/100), 2), round(r.uniform(0.6, 1.9) * ((100+relations)/100), 2), round(r.uniform(0.6, 1.9) * ((100+relations)/100), 2), round(r.uniform(0.6, 1.9) * ((100+relations)/100), 2), round(r.uniform(0.6, 1.9) * ((100+relations)/100), 2), round(r.uniform(0.6, 1.9) * ((100+relations)/100), 2), round(r.uniform(0.6, 1.9) * ((100+relations)/100), 2) ))
    
    def generate_sectors(self):
        sector = r.choice(sectors)
        existing_factions = [row[0] for row in self.db.fetch_all("SELECT name FROM sectors")]
        while sector in existing_factions:
            existing_factions = [row[0] for row in self.db.fetch_all("SELECT name FROM sectors")]
            sector = r.choice(sectors)
        self.db.execute_query("INSERT INTO sectors (name) VALUES (?)", (sector,))

    def generate_systems(self):
        sectors = [row[0] for row in self.db.fetch_all("SELECT sectorID FROM sectors")]
        for sector in sectors:
            numSystems = r.randint(13, 25)
            factions = [row[0] for row in self.db.fetch_all("SELECT factionID FROM factions")]
            for i in range(numSystems):
                self.db.execute_query("INSERT INTO systems (sectorID, factionID, name) VALUES (?, ?, ?)", (sector, r.choice(factions), "Sys"))

db = DatabaseHandler()

lg = LoreGenerator(db)
for i in range(30):
    lg.generate_factions()
    if i % 3 == 0:
        lg.generate_sectors()
lg.generate_systems()