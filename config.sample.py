# Copy this file to config.py and change the database parameters.
import web

db = web.database(dbn='postgres', db='woldb', user='woluser',
                password='wolpassword')
cache = False
