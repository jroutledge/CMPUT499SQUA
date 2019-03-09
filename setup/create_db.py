import sqlite3
import os


class Creator:
    """
    Class responsible for the creation and population of
    the database being used for the game
    """

    def __init__(self, path):
        self.conn = sqlite3.connect('init.db')
        self.c = self.conn.cursor()
        self.path = path

    def end(self):
        self.conn.close()

    def create_tables(self):
        """
        If the tables do not exist already, creates the needed tables.
        """

        # drop all the tables needed so we don't have any issues
        self.c.execute("DROP TABLE IF EXISTS 'StartWords';")
        self.c.execute("DROP TABLE IF EXISTS 'SynWords';")
        self.c.execute("DROP TABLE IF EXISTS 'AntWords';")

        # create the tables
        self.c.execute('''
        -- CREATE TABLE "StartWords" -----------------------------------
        CREATE TABLE IF NOT EXISTS StartWords(
            word Text NOT NULL,
            grade_level Text NOT NULL,
            PRIMARY KEY (word, grade_level)
         );
        -- -------------------------------------------------------------
        ''')
        self.c.execute('''
        -- CREATE TABLE "SynWords" -------------------------------------
        CREATE TABLE IF NOT EXISTS SynWords(
            word Text NOT NULL,
            syn Text NOT NULL,
            FOREIGN KEY ( word ) REFERENCES "StartWords"( word )
        );
        -- -------------------------------------------------------------
        ''')
        self.c.execute('''
        -- CREATE TABLE "AntWords" -------------------------------------
        CREATE TABLE IF NOT EXISTS AntWords(
            word Text NOT NULL,
            ant Text NOT NULL,
            FOREIGN KEY ( word ) REFERENCES "StartWords"( word ) 
        );
        -- -------------------------------------------------------------
        ''')

        # create indexes on things to speed up queries
        self.c.execute("CREATE INDEX IF NOT EXISTS StartWords_grades ON StartWords (grade_level);")
        self.c.execute("CREATE INDEX IF NOT EXISTS StartWords_words ON StartWords (word);")
        self.c.execute("CREATE INDEX IF NOT EXISTS SynWords_words ON SynWords (word);")
        self.c.execute("CREATE INDEX IF NOT EXISTS SynWords_syns ON SynWords (syn);")
        self.c.execute("CREATE INDEX IF NOT EXISTS SynWords_words ON AntWords (word);")
        self.c.execute("CREATE INDEX IF NOT EXISTS SynWords_ants ON AntWords (ant);")

        self.conn.commit()

    def populate(self):
        """
        Populates the created tables with the data generated in
        in the table text files
        """
        fileNames = ["table_StartWords.txt", "table_SynWords.txt", "table_AntWords.txt"]
        tableNames = ["StartWords", "SynWords", "AntWords"]

        for i in range(0, 3):
            f = open(fileNames[i], "r")
            table = tableNames[i]
            for l in f:
                line = l.rstrip()
                line = line.split()

                statement = "INSERT INTO \"" + table + "\" VALUES (\"" + \
                            line[0] + "\", \"" + line[1] + "\");"
                self.c.execute(statement)

        self.conn.commit()


def test():
    """ testing the above class """
    current_path, filename = os.path.split(os.path.abspath(__file__))
    c = Creator(current_path)
    print("Creating tables...")
    c.create_tables()
    print("Populating tables...")
    c.populate()
    c.end()
    print("Done!")


if __name__ == "__main__":
    test()
