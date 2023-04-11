class BusinessEntityAddress:
    __table__ = 'person.businessentityaddress'
    columns = ['addressid', 'businessentityid', 'addresstypeid']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        self.__dict__ = kwargs

    

    