# © 2022 Dmitrii Shcherbakov. All rights reserved.

from servmoncode import dbsqlalch
from sqlalchemy import text

def first_init_db():
    with open('schema.sql', 'r', encoding='utf-8') as f:
        t = text(f.read())
        with dbsqlalch.DB().engine.connect() as conn:
            conn.execute(t)
        conn.close()
        dbsqlalch.DB().engine.dispose()
			
if __name__ == "__main__":
    answer = input("Create new tables [type 'y' for create and 'q' for exit]? : ")
    if answer == "y":
        first_init_db()

