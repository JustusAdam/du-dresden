import sqlite3 as db


with db.connect('data.db') as con:
    with con.cursor() as cur:
        cur.execute('CREATE TABLE "Twitter" ('
                    '"id" INTEGER NOT NULL ON CONFLICT FAIL PRIMARY KEY UNIQUE ON CONFLICT FAIL,'
                    '"status" TEXT NOT NULL'
                    ');')
