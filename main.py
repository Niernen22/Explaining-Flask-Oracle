#importálni mindent amit használsz, idővel több mindent hozzá fogsz adni
from flask import Flask, render_template, request, redirect, url_for
import oracledb
import config

# Flask alkalmazás inicializálása
app = Flask(__name__)

#config fájlból beolvasni az oracle-höz tartozó adatokat
username = config.username
password = config.password
dsn = config.dsn

# A csatlakozási pool (kapcsolatkezelő) létrehozása az adatbázis és az alkalmazás között. (oracledb-t használva)
pool = oracledb.create_pool(user=username, password=password, dsn=dsn, min=1, max=5, increment=1)

#index oldalad
@app.route('/')
def index():
    #session nyitás
    try:
        # Kapcsolat lekérése a csatlakozási pool-ból
        connection = pool.acquire()
        cursor = connection.cursor()

        # SQL lekérdezés létrehozása az 'TESTS' táblából, a nevek alapján rendezve
        query = "SELECT * FROM TESTS ORDER BY NAME"
        cursor.execute(query)

        # Az eredmény formázása egy lista-dict listává
        tests = []
        column_names = [col[0] for col in cursor.description]  # Az oszlopnevek lekérése a kurzor leírásából
        for row in cursor.fetchall():
            tests.append(dict(zip(column_names, row)))  # A táblázat adatok feltöltése egy tests nevű listába

        # Az adatbázis kapcsolat lezárása és a kurzor bezárása
        cursor.close()
        connection.close()

        # HTML sablon renderelése az index oldalhoz, átadva az adatokat (tests) a sablonnak
        return render_template('index.html', tests=tests)

    #error handling
    except oracledb.Error as error:
        # Hiba esetén a megfelelő hibaüzenet visszaadása
        return f"Error connecting to Oracle DB: {error}"


#app futtatása
if __name__ == '__main__':
    # Az alkalmazás indítása, debug mód engedélyezve a hibakereséshez
    app.run(debug=True)
