#!/usr/bin/env python
import sys
import os
import web
from wakeonlan import wol
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import config
import woldb

urls = (
    '/', 'Index',
    '/add/?', 'Add',
    '/add/(\d+)', 'Add',
    '/edit/?', 'Edit',
    '/edit/(\d+)?', 'Edit',
    '/delete/(\d+)', 'Delete',
    '/wol/?', 'Wol',
    '/wol/(\d+)?', 'Wol'
)

render = web.template.render('templates/', cache=config.cache, base='base')


class Index:
    def GET(self):
        hosts = woldb.get_hosts()
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
            woldb.add_host(name, mac, ip)
        except:
            return render.error('Please check your input.')
        return render.success('Host added to database.')


class Edit:
    def GET(self, id=0):
        if id > 0:
            host = woldb.get_host(int(id))
            return render.host_form('edit', host)
        else:
            hosts = woldb.get_hosts()
            return render.edit_hosts(hosts)

    def POST(self, id):
        data = web.input(_method='post')
        try:
            woldb.update_host(id=id, name=data.name, mac=data.mac, ip=data.ip)
        except:
            return render.error('Please check your input.')
        return render.success('Host was successfully edited.')


class Delete:
    def GET(self, id):
        woldb.delete_host(int(id))
        raise web.seeother('/edit')


class Wol:
    def POST(self, id=0):
        id = int(id)
        success = True
        if id > 0:
            host = woldb.get_host(id)
            success = self.wakeup(host)
        else:
            hosts = woldb.get_hosts()
            for host in hosts:
                if not self.wakeup(host):
                    success = False

        if success:
            return render.success('Magic packet was sent.')
        else:
            return render.error('An error occured. Please check your \
                webserver\'s logs.')


    def wakeup(self, host):
        success = True
        try:
            wol.send_magic_packet(host.mac, ip_address=host.ip)
        except:
            success = False
        return success



app = web.application(urls, globals(), autoreload=True)
application = app.wsgifunc()
