import sqlite3

def insert_user(personne, ville, decalage):
    con = sqlite3.connect('./bd/bd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO prayer_time (personne, ville, decalage) VALUES (?, ?, ?)", (personne, ville, decalage))
    con.commit()
    cur.close()
    con.close()
    return "Insertion reussie"

def update_ville(pesonne, new_ville):
    con = sqlite3.connect('./bd/bd.db')
    cur = con.cursor()
    cur.execute("UPDATE prayer_time SET ville = ? WHERE personne = ?", (new_ville, pesonne))
    con.commit()
    cur.close()
    con.close()
    return "Mise a jour reussie"

def update_decalage(personne, new_decalage):
    con = sqlite3.connect('./bd/bd.db')
    cur = con.cursor()
    cur.execute("UPDATE prayer_time SET decalage = ? WHERE personne = ?", (new_decalage, personne))
    con.commit()
    cur.close()
    con.close()
    return "Mise a jour reussie"

def select_all():
    con = sqlite3.connect('./bd/bd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM prayer_time")
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows