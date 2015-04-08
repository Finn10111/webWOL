#!/usr/bin/env python
import sys
import os
import web
from wakeonlan import wol
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import config
import db

urls = (
    '/', 'Index',
    '/add/?', 'Add',
    '/add/(\d+)', 'Add',
    '/edit/?', 'Edit',
    '/edit/(\d+)?', 'Edit',
    '/delete/(\d+)', 'Delete',
    '/wol/(\d+)', 'Wol'
)

render = web.template.render('templates/', cache=config.cache, base='base')


class Index:
    def GET(self):
        hosts = db.get_hosts()
        return render.hosts(hosts)


class Add:
    def GET(self):
        return render.host_form('add', None)

    def POST(self):
        data = web.input(_method='post')
        try:
            name = data.name
            mac = data.mac
            if data.ip:
                ip = data.ip
            else:
                ip = None
            db.add_host(name, mac, ip)
        except:
            return render.error('Please check your input.')
        return render.success('Host added to database.')


class Edit:
    def GET(self, id=0):
        if id > 0:
            host = db.get_host(int(id))
            return render.host_form('edit', host)
        else:
            hosts = db.get_hosts()
            return render.edit_hosts(hosts)

    def POST(self, id):
        data = web.input(_method='post')
        try:
            db.update_host(id=id, name=data.name, mac=data.mac, ip=data.ip)
        except:
            return render.error('Please check your input.')
        return render.success('Host was successfully edited.')


class Delete:
    def GET(self, id):
        db.delete_host(int(id))
        raise web.seeother('/edit')


class Wol:
    def POST(self, id):
        id = int(id)
        host = db.get_host(id)

        try:
            wol.send_magic_packet(host.mac, ip_address=host.ip)
        except:
            return render.error('An error occured. Please check your \
                webserver\'s logs.')
        return render.success('Magic packet was sent.')


app = web.application(urls, globals(), autoreload=True)
application = app.wsgifunc()
