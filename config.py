import web

db = web.database(dbn='postgres', db='woldb', user='woluser',
                password='wolpassword')
cache = False
