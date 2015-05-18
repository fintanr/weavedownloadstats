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

from oauth2client.client import SignedJwtAssertionCredentials
from urllib2 import urlopen
from datetime import date
from bs4 import BeautifulSoup

dockerUrls = {}
dockerReposList = "docker-urls.txt"

repoUrls = {}
repoList = "github-repos.txt"

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

def updateGithubSheet(gc):
    sh = gc.open(os.environ['WEAVE_STATS_SHEET'])
    ws = sh.worksheet("Github Release Downloads")

    today = str(date.today().strftime('%-m/%-d/%Y'))
    datesList = ws.col_values(1)

    if today in datesList:
        return

    downloadCount = getGithubDownloadCount()
    starCount = getGithubStarCount()

    rc = len(datesList)
    rc += 1

    ws.update_cell(rc,1,date.today())
    ws.update_cell(rc,2,downloadCount)
    ws.update_cell(rc,4,starCount)

def updateDockerSheet(gc):
    sh = gc.open(os.environ['WEAVE_STATS_SHEET'])
    ws = sh.worksheet("Docker Hub")

    today = str(date.today().strftime('%-m/%-d/%Y'))
    datesList = ws.col_values(1)

    if today in datesList:
       return

    loadDockerRepoList(dockerReposList)
    dockerDownloads = extractDockerDownloads(dockerUrls)

    rc = len(datesList)
    rc += 1

    for repo, downloads in dockerDownloads.iteritems():
        ws.update_cell(rc,1,date.today())
        ws.update_cell(rc,2,repo)
        ws.update_cell(rc,3,downloads)
        rc += 1

def getGithubDownloadCount():
    weaveReleaseData = "https://api.github.com/repos/weaveworks/weave/releases/latest"

    jdata = urlopen(weaveReleaseData)
    data = json.loads(jdata.read())

    return data['assets'][0]['download_count']

def getGithubStarCount():
    weaveRepoUrl = "https://api.github.com/repos/weaveworks/weave"

    jdata = urlopen(weaveRepoUrl)
    data = json.loads(jdata.read())

    return data['stargazers_count']

def loadDockerRepoList(inFile):
    for s in (line.strip() for line in open(inFile)):
        tmpRepo = s.split("/")
        repo = "%s/%s" % ( tmpRepo[4], tmpRepo[5])
        dockerUrls[repo] = s

#def loadGithubRepoList(inFile):
#   for s in ( line.strip() for line in open(inFile)):

def extractDockerDownloads(urls):

    dockerDownloads = {}

    for repo, url in urls.iteritems():
        u = urlopen(url)
        r = u.read()

        soup = BeautifulSoup(r)
        tag = soup.find('span', { 'class' : 'downloads'})
        downloads = tag.string.extract()

        dockerDownloads[repo] = downloads

    return(dockerDownloads)

if __name__ == '__main__':
    gc = oauthLogin()
    updateGithubSheet(gc)
    updateDockerSheet(gc)
