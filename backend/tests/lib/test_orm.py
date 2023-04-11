from api.lib.orm import find_all, find
from api.models.person import Person
from api.lib.db import test_cursor, test_conn, drop_records, save
import pytest

def build_records(conn, cursor):
    for i in range(1, 15):
        sam = Person(firstname =f'Sam {i}', lastname = 'ok', businessentityid = i, persontype = 'EM')
        
        save(sam, conn, cursor)


@pytest.fixture()
def build_people():
    drop_records(test_cursor, test_conn, 'person.person')
    build_records(test_conn, test_cursor)

    yield

    drop_records(test_cursor, test_conn, 'person.person')

def test_find_returns_the_person_with_the_specified_id(build_people):
    person = find(test_cursor, Person, 2)
    assert person.firstname == "Sam 2"


def test_find_all(build_people):
    persons = find_all(test_cursor, Person)
    assert len(persons) == 10

def test_find_all_limits_by_provided_value(build_people):
    persons = find_all(test_cursor, Person, 5)
    assert len(persons) == 5

def test_find_all_returns_instances_of_the_class(build_people):
    persons = find_all(test_cursor, Person, 1)
    person = persons[0]
    assert isinstance(person, Person)
    assert person.firstname == 'Sam 1'


