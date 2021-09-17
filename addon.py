import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import re
import requests
import urllib
import base64
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Referer': 'https://easysite.one/'
    }

addon = xbmcaddon.Addon()

_pid = sys.argv[0]
_handle = int(sys.argv[1])

liveproxy_enabled = addon.getSettingBool('liveproxy_enabled')
liveproxy_host = addon.getSetting('liveproxy_host')
liveproxy_port = addon.getSetting('liveproxy_port')

parsed = []


def list_channels():
  xbmcplugin.setPluginCategory(_handle, 'Italy TV')
  xbmcplugin.setContent(_handle, 'videos')

  html_doc = requests.get("https://www.livehere.one/", headers=headers).text
  #xbmc.log(html_doc, xbmc.LOGINFO)
  soup = BeautifulSoup(html_doc, 'html.parser')

  channels_cols = soup.find_all('li', ['menu-item-depth-1'])

  for channels_col in channels_cols:
    header = channels_col.find('a', ['menu-link', 'sub-menu-link'])
    header_title = "[COLOR red][B][UPPERCASE]{}[/UPPERCASE][/B][/COLOR]".format(header.getText().strip())

    if header_title not in parsed:
      parsed.append(header_title)

      headerItem = xbmcgui.ListItem(header_title)
      headerItem.setInfo('video', {'title': header_title, 'mediatype': 'video'})
      headerItem.setProperty('IsPlayable', 'false')
      xbmcplugin.addDirectoryItem(handle=_handle, url="", listitem=headerItem, isFolder=False)

      xbmc.log("---------------------------", xbmc.LOGINFO)
      xbmc.log(header_title, xbmc.LOGINFO)

      channels_list = channels_col.find_all('li', ['menu-item-depth-2'])
      for channel in channels_list:
        link = channel.find('a')
        link_title = link.getText().strip()

        videoItem = xbmcgui.ListItem(link_title)
        videoItem.setInfo('video', {'title': link_title, 'mediatype': 'video'})
        data = {
            "action": "scrape",
            "title": link_title,
            "link" : link.get('href')
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=True)
        xbmc.log("{}: {}".format(link_title, link.get('href')), xbmc.LOGINFO)

      xbmc.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^", xbmc.LOGINFO)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
  xbmcplugin.endOfDirectory(_handle)



def add_streamlink(link_strip):
  videoItem = xbmcgui.ListItem(link_strip)
  videoItem.setInfo('video', {'title': link_strip, 'mediatype': 'video'})
  videoItem.setProperty('IsPlayable', 'true')

  if (link_strip.startswith("//")):
    link_strip = "https:" + link_strip

  if (liveproxy_enabled):
    newlink = str.encode("streamlink " + link_strip + " best")
    data = {
        "action": "play",
        "title": link_strip,
        "link" : "http://" + liveproxy_host + ":" + liveproxy_port + "/base64/" + base64.urlsafe_b64encode(newlink).decode('utf-8') + "/"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=False)

    xbmc.log("stream: {}".format(link_strip), xbmc.LOGINFO)


def add_directlink(link_strip):
  videoItem = xbmcgui.ListItem(link_strip)
  videoItem.setInfo('video', {'title': link_strip, 'mediatype': 'video'})
  videoItem.setProperty('IsPlayable', 'true')

  if (link_strip.startswith("//")):
    link_strip = "https:" + link_strip

  data = {
      "action": "play",
      "title": link_strip,
      "link" : link_strip
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=False)
  xbmc.log("direct: {}".format(link_strip), xbmc.LOGINFO)


def add_links_rec(url_in, loop):
  if (loop > 3):
    return

  if (url_in.startswith("//")):
    url_in = "https:" + url_in

  if url_in not in parsed:
    parsed.append(url_in)

    html_in = requests.get(url_in, headers=headers).text
    xbmc.log(html_in, xbmc.LOGINFO)
    soup_in = BeautifulSoup(html_in, 'html.parser')

    iframes_in = soup_in.find_all('iframe')
    for iframe_in in iframes_in:
      try:
        link_strip = iframe_in.get('src')
        if "mailocal2.xyz" in link_strip or "easysite.one" in link_strip or "open-live.org" in link_strip:
          add_links_rec(link_strip, loop + 1)
        else:
          add_streamlink(link_strip)
      except Exception as e:
        xbmc.log("type error: " + str(e), xbmc.LOGERROR)

    natives_in = re.findall(r'https?:\/\/.*?Native.*?\.php', html_in)
    for link_strip in natives_in:
      add_links_rec(link_strip, loop + 1)

    chs_in = re.findall(r'https?:\/\/.*?\/Ch\/.*?\.php', html_in)
    for link_strip in chs_in:
      add_links_rec(link_strip, loop + 1)

    videos_in = soup_in.find_all('video')
    for link_strip in videos_in:
      add_streamlink(link_strip)

    xbmc.log("CHECK FOR m3u8", xbmc.LOGERROR)
    m3u8s_list = re.findall(r'https?:\/\/.*?\.m3u8', html_in)
    for link_strip in m3u8s_list:
      #add_directlink(link_strip)
      add_streamlink(link_strip)


def list_links(params):
  xbmcplugin.setPluginCategory(_handle, 'Italy TV')
  xbmcplugin.setContent(_handle, 'videos')

  add_links_rec(params['link'][0], 0)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)


def play_video(params):
  xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=params['link'][0]))


xbmc.log(" ".join(sys.argv), xbmc.LOGINFO)


def router(paramstring):
  try:
    xbmc.log("paramstring: {}".format(paramstring), xbmc.LOGINFO)
    params = urllib.parse.parse_qs(paramstring)
  except Exception as e:
    xbmc.log("type error: " + str(e), xbmc.LOGERROR)
    params = False

  xbmc.log("params: {}".format(params), xbmc.LOGINFO)

  if params:
    if params['action'][0] == 'play':
      play_video(params)
    elif params['action'][0] == 'scrape':
      list_links(params)
    else:
      list_channels()

  else:
    list_channels()

if __name__ == '__main__':
  router(sys.argv[2][1:])
