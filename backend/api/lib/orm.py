
def build_from_record(Class, record):
    if not record: return None
    attr = dict(zip(Class.columns, record))
    obj = Class()
    obj.__dict__ = attr

    #print("Inside build_from_record")
    return obj
def build_from_records(Class, records):
   return [build_from_record(Class, record) for record in records]

def find_all(Class,cursor, limit = 10):
    sql_str = f"SELECT * FROM {Class.__table__} LIMIT {limit};"
    breakpoint()
    cursor.execute(sql_str)
    records = cursor.fetchall()
    objs = [build_from_record(Class, record) for record in records]
    return objs
def find(Class, cursor, businessentityid):
    sql_str = f"SELECT * FROM {Class.__table__} WHERE businessentityid = %s"
    cursor.execute(sql_str,(businessentityid,))
    record = cursor.fetchone()
    obj = build_from_record(Class, record)

    return obj

