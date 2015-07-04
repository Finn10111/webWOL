import config

db = config.db


def get_hosts():
    return db.select('host', order='name ASC')


def get_host(id):
    return db.select('host', where="id=$id", vars=locals())[0]


def add_host(name, mac, ip):
    db.insert('host', name=name, mac=mac, ip=ip)


def delete_host(id):
    db.delete('host', where="id=$id", vars=locals())


def update_host(id, name, mac, ip):
    db.update('host', where="id=$id", vars=locals(), name=name, mac=mac, ip=ip)
