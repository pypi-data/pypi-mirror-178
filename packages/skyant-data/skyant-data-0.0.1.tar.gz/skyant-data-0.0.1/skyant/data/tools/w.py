'''
'''


class DocumentExists(Warning):
    '''
    An attempt to save the data if the corresponding document exists and overwrite it is allowed.
    '''

    def __init__(self, path: str, **kw):
        self.path = path
        self.message = f'The document {path} was be overwritten!'
        super().__init__(self.message, **kw)
