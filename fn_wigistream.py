import re
import requests

def extract_link(link0):
  doc0 = requests.get(link0, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}).text
  wigiid_re = re.search(r'\/\/wigistream\.to\/embed\/\w+', doc0)
  if wigiid_re:
    wigiid = wigiid_re.group().split('/')[4]
    if wigiid:
      doc1 = requests.get("https://wigistream.to/embed/{0}".format(wigiid), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0', 'Referer': link0}).text
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

          return "https://{0}.{1}.net:8443/hls/{2}.m3u8?s={3}&e={4}|User-Agent={5}&Referer={6}".format(wigia, wigib, wigiid, wigis, wigie, urllib.parse.urlencode('Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'), urllib.parse.urlencode("https://wigistream.to/embed/{0}".format(wigiid)))
  return None

