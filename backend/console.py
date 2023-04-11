import psycopg2
from settings import DB_NAME
conn = psycopg2.connect(dbname = DB_NAME)
cursor = conn.cursor()