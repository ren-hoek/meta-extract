from mayan_api_client import API
import os

class MayanAPI(API):

    def __init__(self, host='', username='', password=''):
        if host == '':
            host = 'http://mayan-edms:80'
        if username == '':
            username = os.environ['MAYAN_USER']
        if password == '':
            password = os.environ['MAYAN_PASS']
        super().__init__(host, username, password)

    def upload_document(self, d, f):
        with open(f, 'rb') as file_object:
            r = self.documents.documents.post(
                {'document_type': d},
                files={'file': file_object}
            )
        return r

