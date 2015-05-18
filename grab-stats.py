#!/usr/bin/python
#
# Update google spreadsheet with download data
# for github release of weave
#
# and docker hub...

import gspread
import json
import os
import re
import csv

from oauth2client.client import SignedJwtAssertionCredentials
from urllib2 import urlopen
from datetime import date
from bs4 import BeautifulSoup

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

def extractGithubSheet(gc):
    sh = gc.open(os.environ['WEAVE_STATS_SHEET'])
    ws = sh.worksheet("Github Release Downloads")

    list_of_lists = ws.get_all_values()

    with open("weave-github-downloads.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(list_of_lists)

def extractDockerSheet(gc):
    sh = gc.open(os.environ['WEAVE_STATS_SHEET'])
    ws = sh.worksheet("Docker Hub")

    list_of_lists = ws.get_all_values()

    with open("weave-docker-downloads.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(list_of_lists)

if __name__ == '__main__':
    gc = oauthLogin()
    extractGithubSheet(gc)
    extractDockerSheet(gc)
