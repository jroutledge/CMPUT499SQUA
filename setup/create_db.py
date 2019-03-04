import sqlite3
conn = sqlite3.connect('init.db')
c = conn.cursor()

c.execute('''
-- CREATE TABLE "StartWords" -----------------------------------
CREATE TABLE IF NOT EXISTS StartWords(
	id Integer NOT NULL PRIMARY KEY,
	word Text NOT NULL,
    grade_level Integer NOT NULL
 );
-- -------------------------------------------------------------
''')
c.execute('''
-- CREATE TABLE "SynWords" -------------------------------------
CREATE TABLE IF NOT EXISTS SynWords(
	id Integer NOT NULL,
	syn Text NOT NULL,
    FOREIGN KEY ( id ) REFERENCES "StartWords"( id )
);
-- -------------------------------------------------------------
''')
c.execute('''
-- CREATE TABLE "AntWords" -------------------------------------
CREATE TABLE IF NOT EXISTS AntWords(
	id Integer NOT NULL,
	ant Text NOT NULL,
    FOREIGN KEY ( id ) REFERENCES "StartWords"( id )
);
-- -------------------------------------------------------------
''')
conn.commit()
conn.close()