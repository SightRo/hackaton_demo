import ftplib
import requests

class radio_manager: 
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

    def invokeMethod(self, methodName, options):
        normalaziedOptions = {}
        for key in options:
            normalaziedOptions[f'a[{key}]'] = options[key]

        normalaziedOptions['xm'] = f'server.{methodName}'
        normalaziedOptions['f'] = 'json'
        normalaziedOptions['a[username]'] = self.username
        normalaziedOptions['a[password]'] = self.password
        
        res = requests.get(self.server + '/api.php', params=normalaziedOptions)
        print(res.status_code)
        return res.content

class radio_files:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

    def upload_file(self, path, file):
        print(path)
        session = ftplib.FTP(self.server, self.username, self.password)
        print(session.storbinary(f'STOR {path}', file))
        session.quit()