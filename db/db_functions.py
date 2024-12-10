import psycopg2
from faker import Faker
from random_word import RandomWords
import random
import hashlib
from datetime import time, datetime
from psycopg2.extras import execute_values
import string

fake = Faker()
random_words = RandomWords()


def get_query_from_file(filename):
  sql_query = ""
  with open(filename, "r", encoding='utf-8') as f:
    for l in f.readlines():
      sql_query = sql_query + l
  f.close()
  return sql_query


def generate_random_string(length):
  return ''.join(
      random.choices(
          '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
          k=length))


def generate_real_word(length=10):
  # Keep fetching words until one meets the length requirement
  word = random_words.get_random_word()
  while word is None or len(word) > length:
    word = random_words.get_random_word()
  return word


def generate_phone_number():
  return '09' + ''.join(random.choices('0123456789', k=8))


def generate_password():
  return hashlib.md5(str(random.random()).encode()).hexdigest()[:16]


def generate_time(start, end):
    hour = str(start).zfill(2)
    minute = str(end).zfill(2)
    return f"{hour}:{minute}:00"



def generate_address():
  return f"{random.randint(100, 999)}, {generate_real_word(random.randint(3, 10))} Street, {generate_real_word(random.randint(3, 10))} City"

def db_conn():
    conn = psycopg2.connect(host="junction.proxy.rlwy.net",
                          port=45436,
                          database="railway",
                          user="postgres",
                          password="rHDdcNSyKZNyrctIWpNFnAYBfqRuxnIl")

    cur = conn.cursor()
    return conn, cur

def connect_db(query):

    conn, cur = db_conn()

    cur.execute(query)
    print(f"sql executed successfully")

    conn.commit()
    print("sql committed")

    cur.close()
    conn.close()
    print('sql connection test completed')

    return conn

def select_query(query):
    conn, cur = db_conn()

    cur.execute(query)
    print(f"sql executed successfully")

    results = cur.fetchall()    
    for row in results:
        print(row)

    conn.commit()
    print("sql committed")

    cur.close()
    conn.close()
    print('sql connection test completed')
    return results

def connect_db_gen(query='', gen_count = 100):
    conn, cur = db_conn()

    # code area 
    counter = 0
    for _ in range(500):
        try:
            data = []
            for _ in range(20):

                characters = string.digits + string.ascii_letters 
                
                cusername = generate_real_word(11) + '_' + ''.join(random.choices(characters, k=3))
                cpassword = generate_password()
                cname = fake.first_name()[:15]
                clname = fake.last_name()[:15]
                cphone = generate_phone_number()

                data.append((cusername, cpassword, cname, clname, cphone))
                print((cusername, cpassword, cname, clname, cphone))

                query = f"""
                INSERT INTO CUSTOMER (CUsername, CPassword, CName, CLname, CPhone)
                VALUES (%s, %s, %s, %s, %s);
                """
            # cur.executemany(query, data)
            # print(f"{cusername, cpassword, cname, clname, cphone}")
                cur.execute(query, (cusername, cpassword, cname, clname, cphone))
            # execute_values(cur, query, data)

        except Exception as E:
            print("Duplicate PK")
            conn.rollback()
            continue
        else:
            conn.commit()
            print("sql committed")
            counter += 20
            print(f"{counter} Customers added")
            if counter >= gen_count:
                break

    cur.close()
    conn.close()
    print('sql connection closed')

    return conn


                # DELIVERY_RIDER

                # drid = generate_random_string(6)
                # drname = fake.first_name()[:10]
                # drphone = generate_phone_number()

                # query = f"""
                #   INSERT INTO DELIVERY_RIDER (DRId, DRName, DRPhone)
                #   VALUES (%s, %s, %s);
                # """

                # cur.execute(query, (drid, drname, drphone))

                # RESTAURANT

                # rusername = generate_real_word(random.randint(5, 15))
                # rpassword = generate_password()
                # rname = generate_real_word(random.randint(3, 20))
                # rphone = generate_phone_number()
                # address = generate_address() 
                # opentime = generate_time(0, 11)
                # closetime = generate_time(13, 23)

                # query = f"""
                # INSERT INTO RESTAURANT 
                # (RUsername, RPassword, RName, RPhone, Address, OpenTime, CloseTime)
                # VALUES (%s, %s, %s, %s, %s, %s, %s);
                # """

                # cur.execute(
                #     query,
                #     (rusername, rpassword, rname, rphone, address, opentime, closetime))

                # print(f"{i}, sql executed successfully")

def connect_gen_restaurant():
    conn, cur = db_conn()

    # code area 
    counter = 0
    for _ in range(3):

        rusername = generate_real_word(random.randint(5, 15))
        rpassword = generate_password()
        rname = generate_real_word(random.randint(3, 20))
        rphone = generate_phone_number()
        address = generate_address() 
        opentime = generate_time(0, 11)
        closetime = generate_time(13, 23)

        cur.execute(
            """
            INSERT INTO Restaurant (RUsername, RPassword, RName, RPhone, Address, OpenTime, CloseTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (rusername, rpassword, rname, rphone, address, opentime, closetime)
        )
        
        conn.commit()
        print("sql committed")


    cur.close()
    conn.close()
    print('sql connection closed')

    return conn


                # DELIVERY_RIDER

                # drid = generate_random_string(6)
                # drname = fake.first_name()[:10]
                # drphone = generate_phone_number()

                # query = f"""
                #   INSERT INTO DELIVERY_RIDER (DRId, DRName, DRPhone)
                #   VALUES (%s, %s, %s);
                # """

                # cur.execute(query, (drid, drname, drphone))

                # RESTAURANT

                # rusername = generate_real_word(random.randint(5, 15))
                # rpassword = generate_password()
                # rname = generate_real_word(random.randint(3, 20))
                # rphone = generate_phone_number()
                # address = generate_address() 
                # opentime = generate_time(0, 11)
                # closetime = generate_time(13, 23)

                # query = f"""
                # INSERT INTO RESTAURANT 
                # (RUsername, RPassword, RName, RPhone, Address, OpenTime, CloseTime)
                # VALUES (%s, %s, %s, %s, %s, %s, %s);
                # """

                # cur.execute(
                #     query,
                #     (rusername, rpassword, rname, rphone, address, opentime, closetime))

                # print(f"{i}, sql executed successfully")

def write_csv(gen_count):  # Threshold in seconds
    with open('customers.csv', 'w') as f:
        for i in range(gen_count):
            if not i % 100:
                print(f"Processing row {i}")

            characters = string.digits + string.ascii_letters 
            cusername = generate_real_word(11) + '_' + ''.join(random.choices(characters, k=3))
            cpassword = generate_password()
            cname = fake.first_name()[:15]
            clname = fake.last_name()[:15]
            cphone = generate_phone_number()


            # Construct the line to write
            line = f"{cusername},{cpassword},{cname},{clname},{cphone}\n"

            f.write(line)
        
        f.close()

def copy_insert(iters):
    inserted = 0
    for i in range(iters):
        write_csv(1000)
        try:
            conn, cur = db_conn()

            with open('customers.csv', 'r') as f:
                cur.copy_from(f, "customer", sep=',', columns=('cusername', 'cpassword', 'cname', 'clname', 'cphone'))
                conn.commit()
                print("sql committed")
                inserted += 1000
                print(f"{inserted} data inserted")
        except Exception as E:
            print("Duplicate PK")
            conn.rollback()
            continue
        finally:
            cur.close()
            conn.close()

def get_column_names(table):
    conn, cur = db_conn()
    query = f'SELECT * FROM "{table}" LIMIT 0'
    cur.execute(query)
    column_names = [desc[0] for desc in cur.description]
    conn.commit()
    cur.close()
    conn.close()
    return tuple(column_names)

def copy_insert_with_file(table, filename):

    column_names = get_column_names(table)
    print(column_names)
    conn, cur = db_conn()
    with open(filename, 'r', encoding='utf-8') as f:
        cur.copy_from(f, table, sep=',', columns = column_names)
        conn.commit()
        print("sql committed")
    cur.close()
    conn.close()

def connect_gen_coupon():
    conn, cur = db_conn()

    restaurants = select_query(get_query_from_file("gen_coupon.txt"))

    for _ in range(40):
        rand_rest = random.choice(restaurants)[0]

        ccode = hashlib.md5(str(random.random()).encode()).hexdigest()[:5]
        cdiscount = random.randint(6,9) / 10
        
        rand_month_start = random.randint(1, 22)
        rand_month_diff = random.randint(1, 23 - rand_month_start)

        print(rand_month_start, rand_month_diff)
        cbegins_at = datetime(year = 2022 + rand_month_start // 12, month = 1 + rand_month_start % 12, day = 1)
        cends_at = datetime(year = 2022 + (rand_month_start + rand_month_diff) // 12, month = 1 + (rand_month_start + rand_month_diff) % 12, day = 1)
        issuedby = rand_rest
        
        print(ccode, cdiscount, cbegins_at, cends_at, issuedby)

        cur.execute(
            """
            INSERT INTO COUPON (ccode, cdiscount, cbeginsat, cendsat, issuedby)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (ccode, cdiscount, cbegins_at, cends_at, issuedby)
        )
        
        conn.commit()
        print("sql committed")


    cur.close()
    conn.close()
    print('sql connection closed')

    return conn

def connect_gen_coupon():
    conn, cur = db_conn()

    restaurants = select_query(get_query_from_file("gen_coupon.txt"))

    for _ in range(40):
        rand_rest = random.choice(restaurants)[0]

        ccode = hashlib.md5(str(random.random()).encode()).hexdigest()[:5]
        cdiscount = random.randint(6,9) / 10
        
        rand_month_start = random.randint(1, 22)
        rand_month_diff = random.randint(1, 23 - rand_month_start)

        print(rand_month_start, rand_month_diff)
        cbegins_at = datetime(year = 2022 + rand_month_start // 12, month = 1 + rand_month_start % 12, day = 1)
        cends_at = datetime(year = 2022 + (rand_month_start + rand_month_diff) // 12, month = 1 + (rand_month_start + rand_month_diff) % 12, day = 1)
        issuedby = rand_rest
        
        print(ccode, cdiscount, cbegins_at, cends_at, issuedby)

        cur.execute(
            """
            INSERT INTO COUPON (ccode, cdiscount, cbeginsat, cendsat, issuedby)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (ccode, cdiscount, cbegins_at, cends_at, issuedby)
        )
        
        conn.commit()
        print("sql committed")


    cur.close()
    conn.close()
    print('sql connection closed')

    return conn