#!/usr/bin/python

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import sys

import StringIO
import md5

import urllib2

import decode

service_name = 'ABCDABCDABCDABCD'

pin = sys.argv[1]

DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
server = dbus.Interface(bus.get_object(
    'org.freedesktop.Avahi', '/'), 'org.freedesktop.Avahi.Server')

def new_service(interface, protocol, name, type, domain, flags):
  print "Found service '%s' of type '%s' in domain '%s'" % (name, type, domain)
  server.ResolveService(interface, protocol, name, type, domain, protocol, 0, reply_handler=service_resolved, error_handler=foo)

def foo():
  pass

def service_resolved(*args):
  name = args[2]
  service = args[3]
  domain = args[4]
  address = args[7]
  port = args[8]
  txt = args[9]
  print 'Resolved: %s %s:%d' % (name, address, port)
  txt_records = {}
  for record in txt:
    r = ''.join([chr(x) for x in record])
    f = r.split('=')
    txt_records[f[0]] = f[1]
  print txt_records

  pair(address, port, txt_records['Pair'])


def pair(address, port, pair):
  merged = StringIO.StringIO()
  merged.write(pair)
  for c in pin:
    merged.write(c)
    merged.write("\x00")

  found = md5.new(merged.getvalue()).hexdigest()
  print 'MD5: %s' % found.upper()

  url = 'http://' + address + ':' + str(port) + '/pair?pairingcode=' + found.upper() + '&servicename=' + service_name
  print url

  reply = urllib2.urlopen(url).read()
  decoded = decode.decode([c for c in reply], len(reply), 0)
  print decoded


print server.GetVersionString()

obj_path = server.ServiceBrowserNew(2, 0, '_touch-remote._tcp', 'local', dbus.UInt32(0))
browser = dbus.Interface(
    bus.get_object('org.freedesktop.Avahi', obj_path), 'org.freedesktop.Avahi.ServiceBrowser')

entry_group_path = server.EntryGroupNew()
entry_group = dbus.Interface(
    bus.get_object('org.freedesktop.Avahi', entry_group_path), 'org.freedesktop.Avahi.EntryGroup')

#txt = [
#  'Password=0',
#  'Machine ID=5C52268ED398',
#  'Media Kinds Shared=0',
#  'Machine Name=zem',
#  'OSsi=0x1F5',
#  'Version=196617',
#  'dmv=131078',
#  'Database ID=18F589722F6A982B',
#  'MID=0x43204F8025562868',
#  'iTSh Version=196611',
#  'txtvers=1',
#]

txt = [
  'txtvers=1',
  'DbId=ABCDABCDABCDABCE',
  'CtlN=Clementine Library',
  'OSsi=0x10313',
  'DvSv=2561',
  'DvTy=iTunes',
  'iV=196611',
  'Ver=131073',
]

#entry_group.AddService(2, 0, 0, 'clementine', '_daap._tcp', 'local', 'zem.local', 8000, txt)
entry_group.AddService(2, 0, 0, 'ABCDABCDABCDABCD', '_touch-able._tcp', 'local', 'zem.local', 3689, txt)
entry_group.Commit()

loop = gobject.MainLoop()
browser.connect_to_signal('ItemNew', new_service)

loop.run()

