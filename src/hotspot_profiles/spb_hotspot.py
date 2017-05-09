
import requests
from bs4 import BeautifulSoup
import dryscrape
import urllib
import logging

from config import App
from profile_abc import ProfileABC

logging.basicConfig(format='%(message)s',level=logging.INFO) #,level=logging.DEBUG / WARNING , etc.




class SPB_Hotspot(ProfileABC):

    def do_initial_login_page(self):
        """
        Connect to the login page and extract the form and input fields, ready for logon.

        Returns a dict of:
            res: True for StatusCode=200 on connection to login page, False if non-200 status code. If false, rest of dict fields will be unpopulated.
            url: url of form action.
            fields: data fields extracted from input form.
        """
        r = requests.get(App.config("login_page"))
        res = {'res': False, 'url': "", 'fields': {}}
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
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

            field_dict["username"] = App.config("username")
            field_dict["password"] = App.config("password")

            logging.warn('Logon Fields: ' + str(field_dict))
            login_form_url = App.config("login_form_root") + action_url
            res = {'res': True, 'url': login_form_url, 'fields': field_dict}
        return res

    def do_logon_request(self, url, field_dict):
        """
        sudo apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
        sudo pip install dryscrape
        """
        args = urllib.urlencode(field_dict)
        url = url + "?" + args
        logging.warn('Logon URL: ' + str(url))
        session = dryscrape.Session()
        session.visit(url)
