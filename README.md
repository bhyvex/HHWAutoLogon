# HHWAutoLogon v1.0 (Hallelujah Hotel Wifi Auto-logon)
To automate log on to hotel / apartment wifi networks that uses a login web page. Typically for unsecured (non-WEP/WPA/WPA2) connections that use the crappy "splash" screen login prompt where the "remember me" checkbox is borked. 

* Linux only ATM. However, forks, improvements and pull requests are welcome.
* License: GNU v3.0

### Back story: 
I got bored of manually loading up our apartment's Wifi provider's 192.x.x.x page and clicking on their broken "Login" button every time we turn on our machines. It required two clicks, first to refresh an already loaded page and second to click "Login", each time waiting on an overloaded hotspot's microprocessor. Instead, I wrote this project in an evening to run in the background and give back some piece of mind..

### Noteworthy Mentions and Imports:
- `wireless` - to collect wireless access point names (plus interface, driver, etc).
- `backoff` - function decorators for fibonacci/exponential backoff/ retries on failures.
- `dryscrape` - HTTP requests to web pages dependent on loaded javascript, then scraping its content.
- `beautifulsoup` and `lxml` - for DOM parsing.
- `requests` - for HTTP requests issuing.
- `urllib` - for url encoding.
- `proc_killer` - for a callback hook on a SIGKILL interrupt.
- `App` - an uncomplicated hardcoded-config class. Alternative is `ConfigParser`.
- `getpass` - for taking password inputs on the console.

## Installation:
1. Clone the repo: `git clone https://github.com/pmdscully/HHWAutoLogon.git`
2. Install the required packages (below)
3. Run it.

### Required packages:
* `sudo apt-get install python2.7 qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb`
* `sudo pip install wireless requests beautifulsoup4 dryscrape urllib backoff`

## How to use:
1. Update as appropriate - `App` configuration class, with SSID names, username, password, login URL, etc.
2. Update as appropriate - `IssueHTTPRequests_Dryscrape` class. A good solution here is to subclass `IssueHTTPRequests_Dryscrape` and override the two methods that:
   * collect to login page form and fill in the username / password
   * send the form data and wait for confirmation page load.
3. Update as appropriate - Logging level `logging.basicConfig(format='%(message)s',level=logging.INFO)`, e.g. level=logging.DEBUG / WARNING , etc.
4. Run: 
   * Foreground: `python HHWAutoLogon.py` 
   * Background: `nohup python HHWAutoLogon.py &; disown;`
