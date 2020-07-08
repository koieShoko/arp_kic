#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

class device_searcher():
    def __init__(self):
        self.mac_address_list = {}
        self.latest_time = None 
    def start(self):
        sys.path.append('./')
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
        import time
        while True:
            self.arp('utf-8')
            self.register()
            print(self.mac_address_list)
            time.sleep(60)
    def arp(self, encoding_scheme):
        import subprocess
        arp_byte  = subprocess.check_output(['arp',"-a"])
        arp_uni   = arp_byte.decode(encoding_scheme)
        arp_rows  = [ row for  row in arp_uni.split(" ")]
        pattern = '..:..:..:..:..:..'
        import time
        when = time.time()
        self.latest_time = when
        self.reset_mac_address_list()
        self.mac_address_list[when]=[]
        import re
        for string in arp_rows:
            result = re.match(pattern, string)
            if result:
                self.mac_address_list[when].append(string)
    def register(self):
        django.setup()
        from arp_kic.models import Human, Device, Arp_log
        mac_addresses = self.mac_address_list[self.latest_time]
        for mac_address in mac_addresses:
            device = Device.objects.get_or_create(mac_address = mac_address)
            from django.utils import timezone
            now   = timezone.now()
            OBJECT = 0
            CREATED =1
            if  device[CREATED] == True: 
                human = Human.objects.create()
            Arp_log.objects.create(device=device[OBJECT], datetime=now, place="home")
    def get_mac_address_list(self):
        return self.mac_address_list
    def reset_mac_address_list(self):
        self.mac_address_list={}

searcher = device_searcher()
searcher.start()