from api.models.person import Person
from api.lib.db import save, test_cursor, test_conn, drop_records
import pytest

def build_records(conn, cursor):
    for i in range(1, 3):
        sam = Person(firstname =f'Sam {i}', lastname = 'ok', businessentityid = i, persontype = 'EM')
        
        save(sam, conn, cursor)

@pytest.fixture()
def build_people():

    drop_records(test_cursor, test_conn, 'person.person')
    build_records(test_conn, test_cursor)

    yield

    drop_records(test_cursor, test_conn, 'person.person')

def test_person_accepts_mass_assignment():
    person = Person(persontype = 'EM', namestyle = 'f', 
                    firstname = 'Ken', middlename = 'J', lastname = 'Sanchez')
    assert person.firstname == 'Ken'

def test_person_has_property_of__table__():
    assert Person.__table__ == 'person.person'

def test_person_has_property_of_columns():
    assert Person.columns == ['businessentityid', 'persontype', 'namestyle', 'title', 'firstname',
      'middlename', 'lastname', 'suffix', 'emailpromotion', 
      'additionalcontactinfo', 'demographics', 'rowguid', 'modifieddata']
     
def test_find_or_create_by_first_and_last_name_finds_the_related_person_if_already_in_the_database(build_people):
    person = Person.find_or_create_by_first_last_name_and_id(firstname = 'Sam 1', lastname = 'ok', businessentityid = 1, conn = test_conn)

    assert person.firstname == 'Sam 1'
    assert person.businessentityid == 1
    test_cursor.execute('select count(*) from person.person')
    num_records = test_cursor.fetchone()
    assert num_records == (2,)

def test_find_or_create_by_first_and_last_name_creates_a_new_person_when_not_in_db(build_people):
    person = Person.find_or_create_by_first_last_name_and_id(firstname = 'Sam 10', lastname = 'ok', 
                                                             businessentityid = 3, conn = test_conn)
    assert person.firstname == 'Sam 10'
    assert person.lastname == 'ok'    
    test_cursor.execute('select count(*) from person.person')
    num_records = test_cursor.fetchone()
    assert num_records == (3,)

