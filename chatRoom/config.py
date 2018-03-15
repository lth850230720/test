import os
options={
    'port':8000
}

BASE_DIRS=os.path.dirname(__file__)

settings={
            'template_path':os.path.join(os.path.dirname(__file__),'templates'),
            'static_path':os.path.join(os.path.dirname(__file__),'static'),
            'cookie_secret':'XtwVd9nTaKpS/GoxkEXDXSZANcAxE+jn7Ko9tnkrIk=',
            '_xsrf_cookie':True
        }
