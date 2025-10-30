import sqlite3
#---GESTION_DE_BASE_DE_DONEE_CINEMA---

#-FCT_CREATION_DB

def creer_tab():
    db= sqlite3.connect("cinema.db")
    cursor= db.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS FILM (
        Id_film INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        genre TEXT,
        duree INTEGER
    );

    CREATE TABLE IF NOT EXISTS SALLE (
        Id_salle INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_salle TEXT NOT NULL,
        capacite INTEGER,
        type_projection TEXT
    );

    CREATE TABLE IF NOT EXISTS RESERVATION (
        Id_res INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_cli TEXT NOT NULL,
        Id_film INTEGER,
        Id_salle INTEGER,
        date_res TEXT,
        prix REAL,
        FOREIGN KEY (Id_film) REFERENCES FILM(Id_film),
        FOREIGN KEY (Id_salle) REFERENCES SALLE(Id_salle)
    );
    """)
    db.commit()
    db.close()


