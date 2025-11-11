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

def select_user_vd(ville, decalage):
    con = sqlite3.connect('./bd/bd.db')
    cur = con.cursor()
    cur.execute("SELECT personne FROM prayer_time WHERE ville = ? AND decalage = ?", (ville, decalage))
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows

def insert_time(time,user):
    con = sqlite3.connect('./bd/time.db')
    cur = con.cursor()
    cur.execute("INSERT INTO timings_connex (time, user) VALUES (?, ?)", (time,user))
    con.commit()
    cur.close()
    con.close()
    return "Insertion reussie"

def get_all_time():
    con = sqlite3.connect('./bd/time.db')
    cur = con.cursor()
    cur.execute("SELECT time FROM timings_connex")
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows

def delete_time(user):
    con = sqlite3.connect('./bd/time.db')
    cur = con.cursor()
    cur.execute("DELETE FROM timings_connex WHERE user = ?", (user,))
    con.commit()
    cur.close()
    con.close()
    return "Suppression reussie"

def get_users(time):
    con = sqlite3.connect('./bd/time.db')
    cur = con.cursor()
    cur.execute("SELECT user FROM timings_connex WHERE time = ?", (time,))
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows