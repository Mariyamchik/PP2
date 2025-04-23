import psycopg2
from config import load_config

def update_user(id, first_name=None, last_name=None, email=None, phone_number=None):
    updated_row_count = 0

    sql = """UPDATE users
             SET
             first_name = COALESCE(%s, first_name),
             last_name = COALESCE(%s, last_name),
             email = COALESCE(%s, email),
             phone_number = COALESCE(%s, phone_number)
             WHERE id = %s"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, email, phone_number, id))
                updated_row_count = cur.rowcount

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return updated_row_count

if __name__ == '__main__':
    update_user(1, "Bon", "Bum", "bombum@example.com", "1111111")
