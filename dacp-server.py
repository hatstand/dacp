#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import struct

from urlparse import urlparse
import decode
import time

def dec(str):
  return decode.decode([c for c in str], len(str), 0)

def encode_num(code, num):
  return struct.pack('>4sII', code, 4, num)

def encode_ver(code, major, minor):
  return struct.pack('>4sIHH', code, 4, major, minor)

def encode_byte(code, byte):
  return struct.pack('>4sIB', code, 1, byte)

def encode_str(code, str):
  return struct.pack('>4sI%ds' % len(str), code, len(str), str)

def encode_long(code, num):
  return struct.pack('>4sIQ', code, 8, num)

def encode_short(code, num):
  return struct.pack('>4sIH', code, 2, num)

class PairingHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    url = urlparse(self.path)
    if url.path == '/login':
      q = url.query
      mstt = encode_num('mstt', 200)
      mlid = encode_num('mlid', int(time.time()))
      mlog = encode_str('mlog', mstt + mlid)

#      self.send_header('Content-Type', 'application/x-dmap-tagged')
      self.send_response(200)
      self.end_headers()
      self.wfile.write(mlog)

    elif url.path == '/server-info':
      mstt = encode_num('mstt', 200)
      mpro = encode_ver('mpro', 1, 0)
      apro = encode_ver('apro', 2, 0)
      minm = encode_str('minm', 'Clementine')

      msau = encode_byte('msau', 0)
      mstm = encode_num('mstm', 1800)

      msex = encode_byte('msex', 0)
      msix = encode_byte('msix', 0)
      msbr = encode_byte('msbr', 0)
      msqy = encode_byte('msqy', 0)
      msup = encode_byte('msup', 0)

      msdc = encode_num('msdc', 1)

#      aeSV = encode_num('aeSV', 0x30000)
#      aeFP = encode_byte('aeFP', 1)
#      ated = encode_short('ated', 3)
#      msed = encode_byte('msed', 1)
#
#      mslr = encode_byte('mslr', 1)
#      msal = encode_byte('msal', 1)
#      msas = encode_byte('msas', 3)
#      mspi = encode_byte('mspi', 1)
#      msrs = encode_byte('msrs', 1)
#
#      mstc = encode_num('mstc', int(time.time()))
#      msto = encode_num('msto', 0)

      msrv_tmp = mstt + mpro + apro + minm + msau + mstm + msex + msix + msbr + msqy + msup + msdc
      msrv = encode_str('msrv', msrv_tmp)

      print dec(msrv)

      self.send_header('Content-Type', 'application/x-dmap-tagged')
      self.send_response(200)
      self.end_headers()
      self.wfile.write(msrv)

    elif url.path == '/databases':
      mstt = encode_num('mstt', 200)
      muty = encode_byte('muty', 0)
      mtco = encode_num('mtco', 1)
      mrco = encode_num('mrco', 1)

      miid = encode_num('miid', 1)
      mper = encode_long('mper', 0xabcdabcdabcdabce)
      minm = encode_str('minm', 'Clementine Library')
      mimc = encode_num('mimc', 1)
      mctc = encode_num('mctc', 1)
      aeMK = encode_num('aeMK', 1)

      mlit = encode_str('mlit', miid + mper + minm + mimc + mctc + aeMK)
      mlcl = encode_str('mlcl', mlit)

      avdb_tmp = mstt + muty + mtco + mrco + mlcl
      avdb = encode_str('avdb', avdb_tmp)

      print dec(avdb)

      self.send_header('Content-Type', 'application/x-dmap-tagged')
      self.send_response(200)
      self.end_headers()
      self.wfile.write(avdb)

    elif url.path == '/ctrl-int':
      mstt = encode_num('mstt', 200)
      mtco = encode_num('mtco', 1)
      mrco = encode_num('mrco', 1)
      muty = encode_byte('muty', 0)

      miid = encode_num('miid', 1)
      cmik = encode_byte('cmik', 1)
      cmsp = encode_byte('cmsp', 1)
      cmsv = encode_byte('cmsv', 1)
      cass = encode_byte('cass', 1)
      casu = encode_byte('casu', 1)
      ceSG = encode_byte('ceSG', 1)

      mlit = encode_str('mlit', miid + cmik + cmsp + cmsv + cass + casu + ceSG)
      mlcl = encode_str('mlcl', mlit)

      caci = encode_str('caci', mstt + mtco + mrco + muty + mlcl)

      print dec(caci)

      self.send_header('Content-Type', 'application/x-dmap-tagged')
      self.send_response(200)
      self.end_headers()
      self.wfile.write(caci)

    elif url.path == '/databases/1/containers':
      mstt = encode_num('mstt', 200)
      muty = encode_byte('muty', 0)
      mtco = encode_num('mtco', 1)
      mrco = encode_num('mrco', 1)

      miid = encode_num('miid', 42)
      mper = encode_num('mper', 42)
      minm = encode_str('minm', 'Playlist 1')
      mimc = encode_num('mimc', 1)

      mlit = encode_str('mlit', miid + mper + minm + mimc)
      mlcl = encode_str('mlcl', mlit)

      aply = encode_str('aply', mstt + muty + mtco + mrco + mlcl)

      print dec(aply)
      self.send_header('Content-Type', 'application/x-dmap-tagged')
      self.send_response(200)
      self.end_headers()
      self.wfile.write(aply)

    elif url.path == '/ctrl-int/1/playstatusupdate':
      mstt = encode_num('mstt', 200)
      cmsr = encode_num('cmsr', 6)
      caps = encode_byte('caps', 3)
      cash = encode_byte('cash', 0)
      carp = encode_byte('carp', 0)
      cavc = encode_byte('cavc', 1)
      caas = encode_num('caas', 2)
      caar = encode_num('caar', 6)
      #canp = 


    else:
      print ':-('
      self.send_response(404)
      self.end_headers()

  def do_POST(self):
    print 'POST!'
    self.send_response(200)
    self.end_headers()


try:
  server = HTTPServer(('', 3689), PairingHandler)
  server.serve_forever()
except KeyboardInterrupt:
  server.socket.close()
