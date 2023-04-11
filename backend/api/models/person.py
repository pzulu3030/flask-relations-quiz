from api.lib.orm import build_from_record
from api.lib.db import save
from api.lib.db import drop_records, get_db, close_db, test_conn, test_cursor, save, save_address
from api.lib.orm import *
import api.models as models

class Person:
    __table__ = 'person.person'
    columns = ['businessentityid', 'persontype', 'namestyle', 'title', 'firstname',
      'middlename', 'lastname', 'suffix', 'emailpromotion', 
      'additionalcontactinfo', 'demographics', 'rowguid', 'modifieddata']
    
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        self.__dict__ = kwargs

    @classmethod
    def find_or_create_by_first_last_name_and_id(self, conn, firstname, lastname, businessentityid):
        cursor = conn.cursor()
        query = f'''select * from person.person where firstname = %s and lastname = %s and businessentityid = %s'''
        cursor.execute(query, (firstname, lastname, businessentityid))
        record = cursor.fetchone()
        if record:
            return build_from_record(Person, record)
        else:
            person = Person(firstname = firstname, lastname = lastname, businessentityid = businessentityid)
            saved_person = save(person, conn, cursor)
            return saved_person
        
    def addresses(self, cursor):
        query = '''select person.address.* from person.address 
        join person.businessentityaddress 
        on person.address.addressid = person.businessentityaddress.addressid 
        join person.person on person.person.businessentityid = person.businessentityaddress.businessentityid
        where person.person.businessentityid = %s
        '''
        cursor.execute(query, (self.businessentityid,))
        address_records = cursor.fetchall()
        addresses = [build_from_record(models.Address, address_record) for address_record in address_records]
        
        return addresses
    
    def to_json(self, cursor):
        addresses = self.addresses(cursor)
        address_dicts = [address.__dict__ for address in addresses]
        person_dict = self.__dict__ 
        person_dict['addresses'] = address_dicts
        return person_dict
        
        
        

    