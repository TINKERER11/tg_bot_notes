import psycopg2


def get_books_from_db(note_id: int) -> list:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="yfhmzy03",
        dbname="mydb"
    )
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM notes WHERE user_id = (%s);", (note_id, ))
        result = cursor.fetchall()
        print(result)
    conn.commit()
    conn.close()
    return result


def create_databases() -> None:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="yfhmzy03",
        dbname="mydb"
    )


    with conn.cursor() as cursor:
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
    	    user_id integer NOT NULL,
    	    note_id serial,
    	    note varchar(20000) NOT NULL
        );""")
    conn.commit()
    conn.close()


def save_data(id: int, s: str):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="yfhmzy03",
        dbname="mydb"
    )
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO notes (user_id, note) VALUES ((%s), (%s));", (id, s))
    conn.commit()
    conn.close()


def delete_data(note_id: int, user_id):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="yfhmzy03",
        dbname="mydb"
    )
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM notes WHERE note_id = (%s) AND user_id = (%s);", (note_id, user_id))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    pass
    #get_books_from_db()
