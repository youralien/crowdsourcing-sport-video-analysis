"""
sample data stream of crowd annotations for
first stage of pipeline found in

sequence_annotation.txt

time (s)    label
1   serve
2   hit
3   hit
4   win
8   serve
9   hit
10  hit
11  hit
12  loose
14  serve
15  hit
17  loose
"""
import sqlite3


def create_table():
    conn = sqlite3.connect('nu_tt.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE sequences
                 (sequence integer,
                  outcome text)""")

    c.execute("""CREATE TABLE events
                 (time integer,
                  ball integer,
                  sequence integer,
                  passive_aggressive text,
                  fh_bh text
                  placement_left_middle_right text,
                  placement_fh_middle_bh text)""")

    conn.commit()
    conn.close()


def save_to_db():

    conn = sqlite3.connect('nu_tt.db')
    c = conn.cursor()

    with open('sequence_annotation.txt', 'r') as f:
        lines = f.readlines()
        lines = lines[1:]  # remove header

        seqIter = 0
        ballNumber = 0
        for line in lines:
            time, label = line.strip("\n").split('\t')  # tab separated

            if label == "serve":
                ballNumber = 1
                c.execute("""INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)""",
                          (time, ballNumber, seqIter, "", "", ""))
                conn.commit()

            if label == "win" or label == "loose":
                c.execute("""INSERT INTO sequences VALUES (?, ?)""",
                          (seqIter, label))
                conn.commit()
                ballNumber = 0
                seqIter += 1

            else:
                ballNumber += 2
                c.execute("""INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)""",
                          (time, ballNumber, seqIter, "", "", ""))

                conn.commit()

    conn.close()


def table_col_info(c, table_name, print_out=False):
    """ Returns a list of tuples with column informations:
        (id, name, type, notnull, default_value, primary_key)
    """
    c.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = c.fetchall()

    if print_out:
        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)
    return info


def read_db():
    conn = sqlite3.connect('nu_tt.db')
    c = conn.cursor()

    table_col_info(c, "events", True)
    c.execute("SELECT * FROM events")
    for line in c:
        print line

    table_col_info(c, "sequences", True)
    c.execute("SELECT * FROM sequences")
    for line in c:
        print line


if __name__ == '__main__':
    create_table()
    save_to_db()
    read_db()
