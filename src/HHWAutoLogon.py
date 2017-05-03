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
from proc_killer import GracefulKiller
from network_utils import check_ping

from wireless import Wireless
import time
import requests
import backoff
from bs4 import BeautifulSoup
import logging
from lxml import html
import getpass
import dryscrape
import urllib 
   
logging.basicConfig(format='%(message)s',level=logging.INFO) #,level=logging.DEBUG / WARNING , etc.




class App(object):
    wireless_access_point_names = ['linksys806B', 'linksys 711B', 'linksys']
    login_page = "http://192.168.100.1:3990/prelogin"
    login_form_root = "http://192.168.100.1/uam/"
    username = ""
    password = ""
    is_at_apartment_max_tries = 3
    is_at_apartment_max_value = 5
    ping_disconnected_max_tries = 3
    ping_disconnected_max_value = 5
    ping_connected_max_tries = 3
    ping_connected_max_value = 5

    @staticmethod
    def config(name):
        return App.__dict__[name]



    
class DoConnect(object):
    
    def __init__(self, req_obj):
        self.requests = req_obj
        self.term = GracefulKiller()

    @backoff.on_predicate(backoff.fibo, lambda x: x == False, 
                                max_value=App.config("is_at_apartment_max_value"), 
                                max_tries=App.config("is_at_apartment_max_tries"))
    def is_at_apartment(self):
        wireless = Wireless()
        return str(wireless.current()) in App.wireless_access_point_names    
    
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
        while self.is_at_apartment():
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


class IssueHTTPRequests_Dryscrape():
    
    def do_initial_login_page(self):
        """
        Connect to the login page and extract the form and input fields, ready for logon.
        
        Returns a dict of:
            res: True for StatusCode=200 on connection to login page, False if non-200 status code. If false, rest of dict fields will be unpopulated.
            url: url of form action.
            fields: data fields extracted from input form.
        """
        r = requests.get( App.login_page )
        res = {'res': False, 'url':"", 'fields': {}}
        if r.status_code == 200:
            soup = BeautifulSoup( r.text, "lxml" )
            field_dict = {}
            action_url = ""
            for form in soup.find_all('form'):  
                # <form action="hotspotlogin.php" method="get" name="form1">
                action_url = form.get("action")
                for field in soup.find_all('input'):
                    field_dict[field.get("name")] = field.get("value")
                    #    <input name="uamip" type="hidden" value="192.168.100.1"/>
                    #    <input name="uamport" type="hidden" value="3990"/>
                    #    <input name="challenge" type="hidden" value="6b93457f0bd5bdbbc299f61ece6cef24"/>
                    #    <input name="redirurl" type="hidden" value=""/>
                    #    <input name="nasid" type="hidden" value="nas01"/>
                    #    <input name="ip" type="hidden" value="192.168.101.110"/>
                    #    <input name="mac" type="hidden" value="C4-85-08-1A-6A-B2"/>
                    #    <input class="styleinput" id="username" name="username" size="18" type="text" value=""/>
                    #    <input class="styleinput" id="password" name="password" size="18" type="password" value=""/>
                    #    <input name="rememberme" type="checkbox" value="1"/>
                    #    <input class="stylebutton" id="login" name="login" onclick="javascript:ProtectNetwork('192.168.100.1', '54-04-A6-2B-09-FD', '192.168.101.110', 'C4-85-08-1A-6A-B2')" type="submit" value="Login"/>
            # Example login url:
            # -- http://192.168.100.1/uam/hotspotlogin.php?uamip=192.168.100.1&uamport=3990&challenge=06de9988e1df1ec009eebb1e2e2e9ff9&redirurl=&nasid=nas01&ip=192.168.101.110&mac=C4-85-08-1A-6A-B2&username=xxxxx&password=xxxxx&rememberme=1&login=Login
            # -- http://192.168.100.1/uam/?username=xxxxxxx&password=xxxx&rememberme=1&ip=192.168.101.110&challenge=49a2f4d9aca525d74aaed01109201672&uamip=192.168.100.1&mac=C4-85-08-1A-6A-B2&uamport=3990&login=Login&redirurl=&nasid=nas01

            field_dict["username"] = App.username
            field_dict["password"] = App.password
            
            logging.warn('Logon Fields: ' + str(field_dict))
            login_form_url = App.login_form_root + action_url
            res = {'res': True, 'url':login_form_url, 'fields': field_dict}
        return res



    def do_logon_request(self, url, field_dict):
        """
        sudo apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
        sudo pip install dryscrape
        """
        args = urllib.urlencode(field_dict)
        url = url+"?"+args
        logging.warn('Logon URL: '+str(url))
        session = dryscrape.Session()
        session.visit(url)
        

if __name__ == "__main__":
    App.username = getpass.getpass('Enter username: <Press Enter>\n')
    App.password = getpass.getpass('Enter password: <Press Enter>\n')
    
    req_obj = IssueHTTPRequests_Dryscrape()
    run = DoConnect(req_obj)
    run.run()

