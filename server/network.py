# source https://gist.github.com/terbo/a8d4021af0cb4729133a
import os, re, sys, time, string
import subprocess, humanize as pp

from netaddr import *

class HotSpot(object):
    def __init__(self):
        self.HOSTAPD_CONTROL_PATH = '/var/run/hostapd'
        self.HOSTAPD_CLI_PATH = '/usr/sbin/hostapd_cli'
        self.IFCONFIG_PATH = '/sbin/ifconfig'
        self.ARP_PATH = '/usr/sbin/arp'
        self.ARP_FLAGS = '-an'

        self.hostapd_interfaces = os.listdir(self.HOSTAPD_CONTROL_PATH)
        self.hostapd_uptime = 0

        self.clients = dict()
        self.arp_table = dict()
        self.hostapd_stats = dict()

        self.get_hostapd()
        self.get_arp_table()
        self.show()

    def get_hostapd(self):
      for hostapd_iface in self.hostapd_interfaces:
        hostapd_cli_cmd = [self.HOSTAPD_CLI_PATH,'-i',hostapd_iface,'all_sta']
        self.hostapd_uptime = time.time() - int(os.stat('%s/%s' % (self.HOSTAPD_CONTROL_PATH, hostapd_iface))[9])

        all_sta_output = subprocess.Popen(hostapd_cli_cmd,stdout=subprocess.PIPE).communicate()[0]
        hostapd_output = subprocess.Popen([self.HOSTAPD_CLI_PATH,'status'],stdout=subprocess.PIPE).communicate()[0].split('\n')

        channel = re.sub('channel=','',hostapd_output[16])
        bssid = re.sub('bssid\[0\]=','',hostapd_output[24])
        ssid = re.sub('ssid\[0\]=','',hostapd_output[25])
        clientcount = int(re.sub('num_sta\[0\]=','',hostapd_output[26]))

        self.hostapd_stats[hostapd_iface] = [ssid, bssid, channel, clientcount]

        macreg = r'^('+r'[:-]'.join([r'[0-9a-fA-F]{2}'] * 6)+r')$'
        stas = re.split(macreg,all_sta_output, flags=re.MULTILINE)

        mac = rx = tx = ctime = ''
        for sta_output in stas:

          for line in sta_output.split('\n'):
            if re.match(macreg,line):
              mac = line
            if re.match('rx_packets',line):
              rx = re.sub('rx_packets=','',line)
            if re.match('tx_packets',line):
              tx = re.sub('tx_packets=','',line)
            if re.match('connected_time=',line):
              ctime = re.sub('connected_time=','',line)

          if mac and rx and tx and ctime:
            self.clients[mac] = [ctime, rx, tx]

    def get_arp_table(self):
      arp_output = subprocess.Popen([self.ARP_PATH,self.ARP_FLAGS],stdout=subprocess.PIPE).communicate()[0].split('\n')

      for line in xrange(len(arp_output)):
        l = arp_output[line].split(' ')
        try:
          iface = l[6]

          if iface in self.hostapd_interfaces:
            ip = l[1]
            hostname = l[2]
            mac = l[3]

            if re.match('[A-Z0-9][A-Z0-9]:',mac,re.IGNORECASE):
              self.arp_table[mac] = [ip, hostname, iface]
        except:
          pass

    def get_vendor(self, mac):
      try: vendor = EUI(mac).oui.registration().org
      except: vendor = 'Unknown'
      return vendor

    def show(self):
        for hostapd_iface in self.hostapd_interfaces:
          iface = self.hostapd_stats[hostapd_iface]
          print '%s (%s / %s, channel %s): %s Client%s, Started: %s' % ( iface[0], iface[1], self.get_vendor(iface[1]), iface[2],
              iface[3], 's' if iface[3]>1 else '',
              pp.naturaltime(self.hostapd_uptime) )

          for mac in self.clients:
            print '  %s' % self.arp_table[mac][0],
            print '  [%s / %s]' % (mac, self.get_vendor(mac)),
        print ': connected %s, %sk in / %sk out' % (pp.naturaltime(self.clients[mac][2]), pp.intcomma(self.clients[mac][0]), pp.intcomma(self.clients[mac][1]))