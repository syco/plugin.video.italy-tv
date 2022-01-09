import xbmc
import re
import requests
import urllib

FFUA = 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'

def extract_link(link0, wigiid=None):
  if (not wigiid):
    doc0 = requests.get(link0, headers={'User-Agent': FFUA}).text
    wigiid_re = re.search(r'\/\/wigistream\.to\/embed\/\w+', doc0)
    if wigiid_re:
      wigiid = wigiid_re.group().split('/')[4]
  if wigiid:
    page1 = "https://wigistream.to/embed/{0}".format(wigiid)
    doc1 = requests.get(page1, headers={'User-Agent': FFUA, 'Referer': link0}).text
    wigi0_re = re.search(r'\d+\|\d+\|[^\|]{22}\|m3u8', doc1)
    if wigi0_re:
      wigi00 = wigi0_re.group().split('|')
      wigis = wigi00[2]
      wigie = wigi00[0]
      wigi1_re = re.search(r'isSupported\|\w+\|loader\|\w+', doc1)
      if wigi1_re:
        wigi11 = wigi1_re.group().split('|')
        wigia = wigi11[3]
        wigib = wigi11[1]

        xbmc.log("WIGI URL: {0}".format(page1), xbmc.LOGINFO)
        xbmc.log("WIGI ID: {0}".format(wigiid), xbmc.LOGINFO)
        xbmc.log("WIGI SUB1: {0}".format(wigia), xbmc.LOGINFO)
        xbmc.log("WIGI SUB2: {0}".format(wigib), xbmc.LOGINFO)
        xbmc.log("WIGI S: {0}".format(wigis), xbmc.LOGINFO)
        xbmc.log("WIGI E: {0}".format(wigie), xbmc.LOGINFO)
        xbmc.log("WIGI UA: {0}".format(urllib.parse.quote(FFUA)), xbmc.LOGINFO)
        xbmc.log("WIGI REFER: {0}".format(urllib.parse.quote(page1)), xbmc.LOGINFO)

        return "https://{0}.{1}.net:8443/hls/{2}.m3u8?s={3}&e={4}|User-Agent={5}&Referer={6}".format(wigia, wigib, wigiid, wigis, wigie, urllib.parse.quote(FFUA), urllib.parse.quote(page1))
  return None

