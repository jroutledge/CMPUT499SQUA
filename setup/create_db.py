import sqlite3
conn = sqlite3.connect('init.db')
c = conn.cursor()

c.execute('''
-- CREATE TABLE "StartWords" -----------------------------------
CREATE TABLE IF NOT EXISTS StartWords(
	word Text NOT NULL PRIMARY KEY,
    grade_level Integer NOT NULL
 );
-- -------------------------------------------------------------
''')
c.execute('''
-- CREATE TABLE "SynWords" -------------------------------------
CREATE TABLE IF NOT EXISTS SynWords(
	word Integer NOT NULL,
	syn Text NOT NULL,
    FOREIGN KEY ( word ) REFERENCES "StartWords"( word )
);
-- -------------------------------------------------------------
''')
c.execute('''
-- CREATE TABLE "AntWords" -------------------------------------
CREATE TABLE IF NOT EXISTS AntWords(
	word Integer NOT NULL,
	ant Text NOT NULL,
    FOREIGN KEY ( word ) REFERENCES "StartWords"( word )
);
-- -------------------------------------------------------------
''')
conn.commit()
conn.close()