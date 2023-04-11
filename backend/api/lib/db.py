from flask import current_app
from flask import g
from api.lib.orm import build_from_record
import psycopg2
from settings import TEST_DB_NAME, DB_NAME



test_conn = psycopg2.connect(dbname = TEST_DB_NAME)
test_cursor = test_conn.cursor()


def build_from_record(Class, record):
    if not record: return None
    attr = dict(zip(Class.columns, record))
    breakpoint()
    obj = Class()
    obj.__dict__ = attr
    return obj

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(dbname = current_app.config['DATABASE'])
        
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def drop_records(cursor, conn, table_name):
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()

def drop_table_records(table_names, cursor, conn):
    for table_name in table_names:
        drop_records(cursor, conn, table_name)

def drop_all_table_records(conn, cursor):
    table_names = ["CountryRegion", "PersonPhone", "PhoneNumberType", 
  "Password", "EmailAddress", "BusinessEntityContact", 
  "ContactType", "BusinessEntityAddress", "ContactType",
  "BusinessEntityAddress", "AddressType", "StateProvince", "Person", "BusinessEntity"]
    drop_table_records(table_names, cursor, conn)


def save(obj, conn, cursor):
    s_str = ', '.join(len(values(obj)) * ['%s'])
   
    venue_str = f"""INSERT INTO {obj.__table__} ({keys(obj)}) VALUES ({s_str}) RETURNING businessentityid;"""

    cursor.execute(venue_str, list(values(obj)))
    #breakpoint()
    id = cursor.fetchone()

    conn.commit()
    cursor.execute(f'SELECT * FROM {obj.__table__} where businessentityid = %s', (id,))
    record = cursor.fetchone()
    #breakpoint()
    return build_from_record(type(obj), record)

def save_address(obj, conn, cursor):
    s_str = ', '.join(len(values(obj)) * ['%s'])
    venue_str = f"""INSERT INTO {obj.__table__} ({keys(obj)}) VALUES ({s_str}) RETURNING addressid;"""
    cursor.execute(venue_str, list(values(obj)))
    id = cursor.fetchone()
    conn.commit()
    cursor.execute(f'SELECT * FROM {obj.__table__} where addressid = %s', (id,))
    record = cursor.fetchone()
    return build_from_record(type(obj), record)

def values(obj):
    venue_attrs = obj.__dict__
    return [venue_attrs[attr] for attr in obj.columns if attr in venue_attrs.keys()]

def keys(obj):
    venue_attrs = obj.__dict__
    selected = [attr for attr in obj.columns if attr in venue_attrs.keys()]
    return ', '.join(selected)