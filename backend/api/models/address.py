class Address:
    __table__ = 'person.address'
    columns = ['addressid', 'addressline1', 'addressline2', 
               'city', 'stateprovinceid', 'postalcode', 
               'spatiallocation', 'rowguid', 'modifieddate']
    
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        self.__dict__ = kwargs
    
    