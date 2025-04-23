import csv
import psycopg2
from config import load_config

def insert_user(first_name, last_name, email, phone_number):
    sql = """INSERT INTO users(first_name, last_name, email, phone_number)
             VALUES(%s, %s, %s, %s)RETURNING id;"""

    id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, email, phone_number,))

                rows = cur.fetchone()
                if rows:
                    id = rows[0]

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return id

def insert_contact(user_id, first_name, last_name, phone_number, email):
    sql = """INSERT INTO contacts(user_id, first_name, last_name, phone_number, email)
             VALUES(%s, %s, %s, %s, %s);"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (user_id, first_name, last_name, phone_number, email))

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_user_csv(path):
    config = load_config()
    id_map = {}
        
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(path, mode='r', newline='') as file:
                    reader = csv.DictReader(file) 
                    for row in reader:
                        first_name = row['first_name']
                        last_name = row['last_name']
                        email = row['email']
                        phone_number = row['phone_number']

                        sql = """INSERT INTO users(first_name, last_name, email, phone_number)
                                 VALUES(%s, %s, %s, %s) RETURNING id;"""
                        cur.execute(sql, (first_name, last_name, email, phone_number))
                        
                        id = cur.fetchone()[0]
                        id_map[id] = (first_name, last_name)
                        
                    conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return id_map

def insert_contact_csv(path):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(path, mode='r', newline='') as file:
                    reader = csv.DictReader(file)
                    contact_data = []

                    for row in reader:
                        user_id = int(row['user_id'])
                        first_name = row['first_name']
                        last_name = row['last_name']
                        phone_number = row['phone_number']
                        email = row['email']

                        contact_data.append((user_id, first_name, last_name, phone_number, email))

                    if contact_data:
                        sql = """INSERT INTO contacts(user_id, first_name, last_name, phone_number, email)
                                 VALUES(%s, %s, %s, %s, %s);"""
                        cur.executemany(sql, contact_data)

                    conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    insert_user_csv('users.csv')
    insert_contact_csv('contacts.csv')
    id_1 = insert_user('Big', 'Bon', 'bigbon@example.com', '1234567890')
    insert_contact(id_1, 'Master', 'Kan', '111223344', 'mkan@example.com')