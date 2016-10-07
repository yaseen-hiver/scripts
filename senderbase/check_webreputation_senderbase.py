#!/usr/bin/env python2.7

"""
 Author: Garfield Carneiro
 Date: 14 Aug Jul 2015
 Description: Script to check Web Reputation for a domain using Senderbase
 Senderbase is Email and Web traffic monitoring network
 Given an domain name they give the rating for that domain
 Domains with Neutral and Good rating are safe to browse and recieve  emails fom.
 A Bad reputation means site is Blacklisted by Senderbase

 Purpose: We ned to monitor site for Browser friendliness.
 A  Bad reputation can lead to blacklisting by popular vendors like BlueCoat, Websense Proxies.
 Logic: Senderbase does not offer API. We need to performing web scrapping the Senderbase site for reputation.
 Generally the Web reputation / Web Rating is stored in a <div> element with class=leftside
 (e.g <div class='leftside'> Neutral </div>)

 This is meant for all Nagios Servers
 Usage:

 check_webreputation_senderbase.py [-h] [--domainsearch] [--domain DOMAIN] [--verbose]
 optional arguments:
  -h, --help            show this help message and exit
  --domainsearch, -D    Perform Domain search instead of String search
  --domain DOMAIN, -d DOMAIN
                        Fully Qualified Domain Name of Site
  --verbose, -v         Verbose flag

 Example :

./check_webreputation_senderbase.py -d code.google.com -v
Thu Aug 13 15:18:37 2015 Arguments : Namespace(debugflag=True, domain='code.google.com', domainsearch=False)
Thu Aug 13 15:18:37 2015 Performing String Search
Thu Aug 13 15:18:37 2015 URL is : http://www.senderbase.org/lookup/?search_string=
Thu Aug 13 15:18:37 2015 Query URL is : http://www.senderbase.org/lookup/?search_string=code.google.com
Thu Aug 13 15:18:37 2015 Checking for HTTP 200 Status Code
Thu Aug 13 15:18:37 2015 HTTP Status Code is 200.
Thu Aug 13 15:18:37 2015 HTML Response Length 33190 characters
Thu Aug 13 15:18:37 2015 Parsing HTML
Thu Aug 13 15:18:37 2015 Looking for a <div> element whose 'class' attribute value is 'leftside'
Thu Aug 13 15:18:37 2015 <div class='leftside'>WEBRATING</div>
Thu Aug 13 15:18:37 2015 Found web rating for [code.google.com] as [NEUTRAL]
OK: Web Rating for code.google.com is Neutral
"""

import sys
import argparse
import datetime

# Nagios States and Return Codes
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

try:
    import requests
except:
    print "Error while importing [requests] module."
    exit(STATE_UNKNOWN)

try:
    from bs4 import BeautifulSoup
except:
    print "Error while importing [BeautifulSoup] module."
    exit(STATE_UNKNOWN)


# Defining Search URLs
# Some domains e.g amazon.com require Domain Search entry point /lookup/domain
senderbaseStringQuerySearchURL = 'http://www.senderbase.org/lookup/?search_string='
senderbaseDomainQuerySearchURL = 'http://www.senderbase.org/lookup/domain/?search_string='


def dprint(msg):
    """Print only when debugging is enabled"""
    if argv.debugflag:
        format = "%a %b %d %H:%M:%S %Y"
        today = datetime.datetime.today()
        timestamp = today.strftime(format)
        print str(timestamp + " " + msg)


parser = argparse.ArgumentParser()
parser.add_argument("--domainsearch", "-D", dest="domainsearch", default=False, action="store_true", \
                    help="Perform Domain search instead of String search")
parser.add_argument("--domain", "-d", dest="domain", default="a.rfihub.com", action="store", help="Fully Qualified Domain Name of Site")
parser.add_argument("--verbose", "-v", dest="debugflag", default=False, action="store_true", help="Verbose flag")

argv = parser.parse_args()

dprint("Arguments : " + str(argv))

if argv.domainsearch is True:
    dprint("Performing Domain Search")
    url = senderbaseDomainQuerySearchURL
else:
    dprint("Performing String Search")
    url = senderbaseStringQuerySearchURL

dprint("URL is : %s" % (url))

queryURL = str(url) + str(argv.domain)
dprint("Query URL is : %s" % (queryURL))

# We need to set input field called 'tos_accepted' to 'Yes, I Agree' in HTML Encoding
data = {"tos_accepted": "Yes%2C+I+Agree"}

# Make a request to senderbase with POST data
page = requests.post(queryURL, data)

dprint("Checking for HTTP 200 Status Code")
if page.status_code == 200:
    dprint("HTTP Status Code is %s." % page.status_code)
elif page.status_code != 200:
    print "HTTP Status Code is %s. Expected 200. Exiting" % page.status_code
    exit(STATE_UNKNOWN)

htmldata = page.text
dprint("HTML Response Length %s characters" % len(htmldata))

dprint("Parsing HTML")
parsed_html = BeautifulSoup(htmldata, "lxml")

dprint("Looking for a <div> element whose 'class' attribute value is 'leftside' ")
dprint("<div class='leftside'>WEBRATING</div>")

# Unicode Web Rating
uWebRating = parsed_html.body.find('div', attrs={'class': 'leftside'}).text

# Type Conversion from Unicode to String
webRating = str(uWebRating).lower()

dprint("Found web rating for [%s] as [%s]" % (argv.domain, webRating.upper()))

if webRating == 'neutral' or webRating == 'good':
    print "OK: Web Rating for %s is %s" % (argv.domain, uWebRating)
    exit(STATE_OK)
elif webRating == 'poor':
    print "ALERT: Web Rating for %s is %s" % (argv.domain, uWebRating)
    exit(STATE_CRITICAL)
elif webRating is None or webRating == "":
    print "UNKNOWN: Web Rating not Found"
    exit(STATE_UNKNOWN)
