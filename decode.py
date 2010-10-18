# simple message decoder for dacp
# released gplv3 by jeffrey sharkey

import sys, struct, re

def format(c):
  if ord(c) >= 128: return "(byte)0x%02x"%ord(c)
  else: return "0x%02x"%ord(c)

def read(queue, size):
  pull = ''.join(queue[0:size])
  del queue[0:size]
  return pull

group = ['cmst','mlog','agal','mlcl','mshl','mlit','abro','abar','apso','caci','avdb','cmgt','aply','adbs','cmpa', 'msrv', 'mcrr']

rebinary = re.compile('[^\x20-\x7e]')

def ashex(s): return ''.join([ "%02x" % ord(c) for c in s ])

def asbyte(s): return struct.unpack('>B', s)[0]
def asint(s): return struct.unpack('>I', s)[0]
def aslong(s): return struct.unpack('>Q', s)[0]


def decode(raw, handle, indent):
  while handle >= 8:
    # read word data type and length
    ptype = read(raw, 4)
    plen = asint(read(raw, 4))
    handle -= 8 + plen

    # recurse into groups
    if ptype in group:
      print '\t' * indent, ptype, str(plen), " --+"
      decode(raw, plen, indent + 1)
      continue

    # read and parse data
    pdata = read(raw, plen)

    nice = '%s' % ashex(pdata)
    if plen == 1: nice = '%s == %s' % (ashex(pdata), asbyte(pdata))
    if plen == 4: nice = '%s == %s' % (ashex(pdata), asint(pdata))
    if plen == 8: nice = '%s == %s' % (ashex(pdata), aslong(pdata))

    if rebinary.search(pdata) is None:
        nice = pdata

    print '\t' * indent, ptype.ljust(6), str(plen).ljust(6), nice
