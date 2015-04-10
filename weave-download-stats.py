#!/usr/bin/python
#
# Update google spreadsheet with download data
# for github release of weave

import gspread
import json
import os
import re

from oauth2client.client import SignedJwtAssertionCredentials
from urllib2 import urlopen
from datetime import date

def oauthLogin():
    try:
        os.environ['GOOGLE_KEY']
        os.environ['GOOGLE_EMAIL']
        os.environ['WEAVE_STATS_SHEET']
    except KeyError:
        print "Please ensure you have GOOGLE_KEY, GOOGLE_EMAIL and WEAVE_STATS_SHEET set"
        exit(1)

    pemFile = os.environ['GOOGLE_KEY']
    f = file(pemFile, 'rb')
    key = f.read()
    f.close()

    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(os.environ['GOOGLE_EMAIL'], key, scope)

    try:
        gc = gspread.authorize(credentials)
    except AuthenticationError:
        print "Authentication Error"
        exit(1)

    return (gc)

def updateSheet(gc):
    sh = gc.open(os.environ['WEAVE_STATS_SHEET'])
    ws = sh.worksheet("Github Downloads")

    today = str(date.today().strftime('%-m/%-d/%Y'))
    datesList = ws.col_values(1)

    if today in datesList:
        exit(0)

    downloadCount = getDownloadCount()

    rc = len(datesList)
    rc += 1

    ws.update_cell(rc,1,date.today())
    ws.update_cell(rc,2,downloadCount)

def getDownloadCount():
    weaveReleaseData = "https://api.github.com/repos/weaveworks/weave/releases/latest"

    jdata = urlopen(weaveReleaseData)
    data = json.loads(jdata.read())

    return data['assets'][0]['download_count']

if __name__ == '__main__':
    gc = oauthLogin()
    updateSheet(gc)
