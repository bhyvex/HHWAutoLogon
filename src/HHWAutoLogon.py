"""
HHWAutoLogon.py - A Typical hotel wifi logon script:

@desc:      Script to enable auto logging on to unsecured (non-WEP/WPA/WPA2) wifi network that requires a username/password web page login prompt.
@author:    PS
@version:   v1.0
@date:      03/05/2017
@license:   GNU v3.0.

Usage and requirements: see Readme.MD for details.

Required Packages:
    - apt-get install python2.7 qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
    - pip install wireless requests beautifulsoup4 dryscrape urllib backoff
"""
from wireless import Wireless
import time
import backoff
import logging
import getpass

logging.basicConfig(format='%(message)s',level=logging.INFO) #,level=logging.DEBUG / WARNING , etc.

from proc_killer import GracefulKiller
from network_utils import check_ping
from config import App
from hotspot_profiles.spb_hotspot import SPB_Hotspot





class DoConnect(object):
    
    def __init__(self, req_obj):
        self.requests = req_obj
        self.term = GracefulKiller()

    @backoff.on_predicate(backoff.fibo, lambda x: x == False, 
                                max_value=App.config("is_at_hotspot_location_max_value"), 
                                max_tries=App.config("is_at_hotspot_location_max_tries"))
    def is_near_hotspot(self):
        wireless = Wireless()
        return str(wireless.current()) in App.config("wireless_access_point_names")
    
    @backoff.on_predicate(backoff.fibo, lambda x: x == True, 
                                max_value=App.config("ping_connected_max_value"), 
                                max_tries=App.config("ping_connected_max_tries"))
    @backoff.on_predicate(backoff.fibo, lambda x: x == False, 
                                max_value=App.config("ping_disconnected_max_value"), 
                                max_tries=App.config("ping_disconnected_max_tries"))
    def do_ping(self):
        return check_ping()
        
    def run(self):
        while not self.term.kill_now:
            # Catch any exceptions and ignore them, unless the script has received a SIGTERM request.
            try:
                self.__loop()
            except Exception as e:
                logging.warn("Exception raised: " + str(e))
                time.sleep(1)
                if self.term.kill_now:
                    break
    
    def __loop(self):
        while self.is_near_hotspot():
            if not self.do_ping():
                res = self.requests.do_initial_login_page()
                if res['res'] is True:
                    time.sleep(1)
                    login_form_url  = res['url']
                    field_dict      = res['fields']
                    self.requests.do_logon_request(login_form_url, field_dict)
                else:
                    logging.error("Unable to connect to login page, despite being connected to hotspot..")
            else:
                print "connected"
            time.sleep(1)
            if self.term.kill_now:
                break


if __name__ == "__main__":
    App.set("username", getpass.getpass('Enter username: <Press Enter>\n') )
    App.set("password", getpass.getpass('Enter password: <Press Enter>\n') )
    
    req_obj = SPB_Hotspot()
    run = DoConnect(req_obj)
    run.run()

