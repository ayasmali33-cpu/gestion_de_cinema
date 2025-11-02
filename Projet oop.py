import tkinter as tk
from tkinter import messagebox 
import sqlite3

#---BASE DE DONNÉES---
Database="cinema.db"

def creer_tab():
    db=sqlite3.connect(Database)
    cursor=db.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS film (
            id_film INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            genre TEXT,
            duree INTEGER,
            annee INTEGER
        );
        CREATE TABLE IF NOT EXISTS client (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_client TEXT NOT NULL,
            numero_telephone TEXT,
            email TEXT
        );
        CREATE TABLE IF NOT EXISTS reservation (
            id_res INTEGER PRIMARY KEY AUTOINCREMENT,
            id_client INTEGER,
            id_film INTEGER,
            nom_salle TEXT,
            type_de_projection TEXT,
            date_res TEXT,
            prix REAL,
            FOREIGN KEY (id_film) REFERENCES film(id_film),
            FOREIGN KEY (id_client) REFERENCES client(id_client)
        );
    """)
    db.commit()
    db.close()

#---FONCTIONS DE GESTION---
def inser_film(titre, genre, duree, annee):
    db = sqlite3.connect(Database)
    db.execute("INSERT INTO film (titre, genre, duree, annee) VALUES (?, ?, ?, ?)", (titre, genre, duree, annee))
    db.commit()
    db.close()

def inser_client(nom, tel, email):
    db = sqlite3.connect(Database)
    db.execute("INSERT INTO client (nom_client, numero_telephone, email) VALUES (?, ?, ?)", (nom, tel, email))
    db.commit()
    db.close()

def inser_reservation(id_client, id_film, salle, type_proj, date_res, prix):
    db = sqlite3.connect(Database)
    db.execute("""
        INSERT INTO reservation (id_client, id_film, nom_salle, type_de_projection, date_res, prix)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_client, id_film, salle, type_proj, date_res, prix))
    db.commit()
    db.close()

def supp(nom_table, nom_id, valeur_id):
    db=sqlite3.connect(Database)
    cursor=db.cursor()
    cursor.execute(f"DELETE FROM {nom_table} WHERE {nom_id} = ?",(valeur_id,))
    cursor.execute(f"SELECT {nom_id} FROM {nom_table} ORDER BY {nom_id}")
    ids=cursor.fetchall()
    new_id = 1
    for (old_id,) in ids:
        if old_id != new_id:
            cursor.execute(f"UPDATE {nom_table} SET {nom_id} = ? WHERE {nom_id} = ?", (new_id, old_id))
        new_id += 1
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{nom_table}'")
    db.commit()
    db.close()

# --- THÈME ---
FOND= "#0D0D0D"
TEXTE= "#F5F5F5"
BOUTON = "#D4AF37"
BOUTON_TEXTE = "#0D0D0D"
FONT_LABEL =("Arial", 14, "bold")
FONT_BTN =("Arial", 12, "bold")
GRID_BG = "#FFFFFF"
GRID_TEXT = "#000000"

#---windows---
def window_films():
    fen=tk.Toplevel()
    fen.title("Gestion des films")
    fen.configure(bg=FOND)

    titre_var=tk.StringVar()
    genre_var=tk.StringVar()
    duree_var=tk.StringVar()
    annee_var=tk.StringVar()
    id_sup_var=tk.StringVar()

   
    tk.Label(fen, text="Titre:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=0, column=0, sticky='w')
    tk.Entry(fen, textvariable=titre_var, width=30).grid(row=0, column=1)
    
    tk.Label(fen, text="Genre:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=1, column=0, sticky='w')
    tk.Entry(fen, textvariable=genre_var, width=30).grid(row=1, column=1)
    
    tk.Label(fen, text="Durée:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=2, column=0, sticky='w')
    tk.Entry(fen, textvariable=duree_var, width=30).grid(row=2, column=1)
    
    tk.Label(fen, text="Année:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=3, column=0, sticky='w')
    tk.Entry(fen, textvariable=annee_var, width=30).grid(row=3, column=1)

    tk.Label(fen, text="ID à supprimer:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=4, column=0, sticky='w')
    tk.Entry(fen, textvariable=id_sup_var, width=30).grid(row=4, column=1)

    frame_affichage=tk.Frame(fen, bg=GRID_BG)
    frame_affichage.grid(row=6, column=0, columnspan=2, pady=20)

    def afficher_films():
        for widget in frame_affichage.winfo_children():
            widget.destroy()
        db = sqlite3.connect(Database)
        db.row_factory = sqlite3.Row
        cursor = db.execute("SELECT * FROM film")
        # En-tête
        tk.Label(frame_affichage, text="ID", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=0)
        tk.Label(frame_affichage, text="Titre", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=1)
        tk.Label(frame_affichage, text="Genre", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=2)
        tk.Label(frame_affichage, text="Durée", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=3)
        tk.Label(frame_affichage, text="Année", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=4)
        ligne = 1
        for row in cursor:
            tk.Label(frame_affichage, text=row['id_film'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=0)
            tk.Label(frame_affichage, text=row['titre'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=1)
            tk.Label(frame_affichage, text=row['genre'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=2)
            tk.Label(frame_affichage, text=row['duree'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=3)
            tk.Label(frame_affichage, text=row['annee'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=4)
            ligne+=1
        db.close()

    def ajouter_film():
        if not titre_var.get() or not genre_var.get() or not duree_var.get() or not annee_var.get():
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs !")
            return
        inser_film(titre_var.get(),genre_var.get(),duree_var.get(),annee_var.get())
        afficher_films()
        messagebox.showinfo("Succès", "Film ajouté avec succès !")

    def supprimer_film():
        if not id_sup_var.get():
            messagebox.showwarning("Attention", "Veuillez entrer l'ID à supprimer !")
            return
        supp("film", "id_film", id_sup_var.get())
        afficher_films()

    tk.Button(fen, text="Ajouter", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, command=ajouter_film).grid(row=5, column=0, pady=5)
    tk.Button(fen, text="Supprimer", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, command=supprimer_film).grid(row=5, column=1, pady=5)

    afficher_films()


def window_clients():
    fen=tk.Toplevel()
    fen.title("Gestion des clients")
    fen.configure(bg=FOND)

    nom_var=tk.StringVar()
    tel_var=tk.StringVar()
    email_var=tk.StringVar()
    id_sup_var=tk.StringVar()

    tk.Label(fen,text="Nom:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=0, column=0, sticky='w')
    tk.Entry(fen,textvariable=nom_var, width=30).grid(row=0, column=1)
    tk.Label(fen,text="Téléphone:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=1, column=0, sticky='w')
    tk.Entry(fen,textvariable=tel_var, width=30).grid(row=1, column=1)
    tk.Label(fen,text="Email:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=2, column=0, sticky='w')
    tk.Entry(fen,textvariable=email_var, width=30).grid(row=2, column=1)

    tk.Label(fen, text="ID à supprimer:", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=3, column=0, sticky='w')
    tk.Entry(fen, textvariable=id_sup_var, width=30).grid(row=3, column=1)

    frame_affichage = tk.Frame(fen, bg=GRID_BG)
    frame_affichage.grid(row=5, column=0, columnspan=2, pady=20)

    def afficher_clients():
        for widget in frame_affichage.winfo_children():
            widget.destroy()
        db = sqlite3.connect(Database)
        db.row_factory = sqlite3.Row
        cursor = db.execute("SELECT * FROM client")
        tk.Label(frame_affichage, text="ID", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=0)
        tk.Label(frame_affichage, text="Nom", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=1)
        tk.Label(frame_affichage, text="Téléphone", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=2)
        tk.Label(frame_affichage, text="Email", bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=3)
        ligne = 1
        for row in cursor:
            tk.Label(frame_affichage, text=row['id_client'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=0)
            tk.Label(frame_affichage, text=row['nom_client'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=1)
            tk.Label(frame_affichage, text=row['numero_telephone'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=2)
            tk.Label(frame_affichage, text=row['email'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=3)
            ligne += 1
        db.close()

    def ajouter_client():
        if not nom_var.get() or not tel_var.get() or not email_var.get():
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs !")
            return
        inser_client(nom_var.get(), tel_var.get(), email_var.get())
        afficher_clients()
        messagebox.showinfo("Succès", "Client ajouté avec succès !")

    def supprimer_client():
        if not id_sup_var.get():
            messagebox.showwarning("Attention", "Veuillez entrer l'ID à supprimer !")
            return
        supp("client", "id_client", id_sup_var.get())
        afficher_clients()

    tk.Button(fen, text="Ajouter", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, command=ajouter_client).grid(row=4, column=0, pady=5)
    tk.Button(fen, text="Supprimer", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, command=supprimer_client).grid(row=4, column=1, pady=5)

    afficher_clients()

# --- Réservations ---
def window_reservations():
    fen = tk.Toplevel()
    fen.title("Gestion des réservations")
    fen.configure(bg=FOND)

    id_client_var=tk.StringVar()
    id_film_var=tk.StringVar()
    salle_var=tk.StringVar()
    type_var=tk.StringVar()
    date_var=tk.StringVar()
    prix_var=tk.StringVar()
    id_sup_var=tk.StringVar()

    labels = ["ID Client", "ID Film", "Salle", "Type", "Date", "Prix", "ID à supprimer"]
    vars_list = [id_client_var, id_film_var, salle_var, type_var, date_var, prix_var, id_sup_var]

    tk.Label(fen, text=labels[0] + ":", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=0, column=0, sticky='w')
    tk.Entry(fen, textvariable=vars_list[0], width=30).grid(row=0, column=1)

    tk.Label(fen, text=labels[1] + ":", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=1, column=0, sticky='w')
    tk.Entry(fen, textvariable=vars_list[1], width=30).grid(row=1, column=1)

    tk.Label(fen, text=labels[2] + ":", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=2, column=0, sticky='w')
    tk.Entry(fen, textvariable=vars_list[2], width=30).grid(row=2, column=1)

    tk.Label(fen, text=labels[3] + ":", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=3, column=0, sticky='w')
    tk.Entry(fen, textvariable=vars_list[3], width=30).grid(row=3, column=1)

    tk.Label(fen, text=labels[4] + ":", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=4, column=0, sticky='w')
    tk.Entry(fen, textvariable=vars_list[4], width=30).grid(row=4, column=1)

    tk.Label(fen, text=labels[5] + ":", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=5, column=0, sticky='w')
    tk.Entry(fen, textvariable=vars_list[5], width=30).grid(row=5, column=1)

    tk.Label(fen, text=labels[6] + ":", bg=FOND, fg=TEXTE, font=FONT_LABEL).grid(row=6, column=0, sticky='w')
    tk.Entry(fen, textvariable=vars_list[6], width=30).grid(row=6, column=1)


    frame_affichage=tk.Frame(fen, bg=GRID_BG)
    frame_affichage.grid(row=8, column=0, columnspan=2, pady=20)

    def afficher_reservations():
        for widget in frame_affichage.winfo_children():
            widget.destroy()
        db = sqlite3.connect(Database)
        db.row_factory = sqlite3.Row
        cursor = db.execute("SELECT * FROM reservation")
        headers = ["ID", "ID Client", "ID Film", "Salle", "Type", "Date", "Prix"]
        for col, h in enumerate(headers):
            tk.Label(frame_affichage, text=h, bg=GRID_BG, fg=GRID_TEXT, font=FONT_LABEL).grid(row=0, column=col)
        ligne = 1
        for row in cursor:
            tk.Label(frame_affichage, text=row['id_res'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=0)
            tk.Label(frame_affichage, text=row['id_client'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=1)
            tk.Label(frame_affichage, text=row['id_film'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=2)
            tk.Label(frame_affichage, text=row['nom_salle'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=3)
            tk.Label(frame_affichage, text=row['type_de_projection'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=4)
            tk.Label(frame_affichage, text=row['date_res'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=5)
            tk.Label(frame_affichage, text=row['prix'], bg=GRID_BG, fg=GRID_TEXT).grid(row=ligne, column=6)
            ligne += 1
        db.close()

    def ajouter_reservation():
        if not all([v.get() for v in vars_list[:-1]]):
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs !")
            return
        inser_reservation(id_client_var.get(), id_film_var.get(), salle_var.get(), type_var.get(), date_var.get(), prix_var.get())
        afficher_reservations()
        messagebox.showinfo("Succès", "Réservation ajoutée avec succès !")

    def supprimer_reservation():
        if not id_sup_var.get():
            messagebox.showwarning("Attention", "Veuillez entrer l'ID à supprimer !")
            return
        supp("reservation", "id_res", id_sup_var.get())
        afficher_reservations()

    tk.Button(fen, text="Ajouter", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, command=ajouter_reservation).grid(row=7, column=0, pady=5)
    tk.Button(fen, text="Supprimer", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, command=supprimer_reservation).grid(row=7, column=1, pady=5)

    afficher_reservations()

# --- FENÊTRE PRINCIPALE ---
creer_tab()
window=tk.Tk()
window.title("Gestion de cinéma")
window.geometry("900x700")
window.configure(bg=FOND)

tk.Label(window,text="🎞 Gestion de Cinéma 🎞", bg=FOND, fg=BOUTON, font=("Arial", 24, "bold")).pack(pady=20)
tk.Button(window,text="🎞 Films", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, width=30, command=window_films).pack(pady=10)
tk.Button(window,text="👥 Clients", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, width=30, command=window_clients).pack(pady=10)
tk.Button(window,text="🎟 Réservations", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, width=30, command=window_reservations).pack(pady=10)
tk.Button(window,text="❌ Quitter", bg=BOUTON, fg=BOUTON_TEXTE, font=FONT_BTN, width=30, command=window.destroy).pack(pady=10)

window.mainloop()
