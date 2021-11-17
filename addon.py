import streamlink
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import base64
from bs4 import BeautifulSoup

_pid = sys.argv[0]
_handle = int(sys.argv[1])

import lib_livehereone as lh1
import lib_sportlive as sl1

addon = xbmcaddon.Addon()

liveproxy_enabled = addon.getSettingBool('liveproxy_enabled')
liveproxy_host = addon.getSetting('liveproxy_host')
liveproxy_port = addon.getSetting('liveproxy_port')

sportlive_enabled = addon.getSettingBool('sportlive_enabled')
sportlive_pass = addon.getSetting('sportlive_pass')


def add_streamlink(link_title, link_strip):
  videoItem = xbmcgui.ListItem(link_title)
  videoItem.setInfo('video', {'title': "streamlink " + link_title, 'mediatype': 'video'})
  videoItem.setProperty('IsPlayable', 'true')

  if (link_strip.startswith("//")):
    link_strip = "https:" + link_strip

  data = {
      "action": "play_streamlink",
      "title": "streamlink " + link_title,
      "link" : link_strip
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=False)
  xbmc.log("{0}: {1}".format("streamlink " + link_title, link_strip), xbmc.LOGINFO)

  if (liveproxy_enabled):
    newlink = str.encode("streamlink " + link_strip + " best")
    add_directlink("liveproxy " + link_title, "http://" + liveproxy_host + ":" + liveproxy_port + "/base64/" + base64.urlsafe_b64encode(newlink).decode('utf-8') + "/")


def add_directlink(link_title, link_strip):
  videoItem = xbmcgui.ListItem(link_title)
  videoItem.setInfo('video', {'title': link_title, 'mediatype': 'video'})
  videoItem.setProperty('IsPlayable', 'true')

  if (link_strip.startswith("//")):
    link_strip = "https:" + link_strip

  data = {
      "action": "play_directlink",
      "title": link_title,
      "link" : link_strip
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=False)
  xbmc.log("{0}: {1}".format(link_title, link_strip), xbmc.LOGINFO)


def play_directlink(params):
  xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=params['link'][0]))


def play_streamlink(params):
  streams = streamlink.streams(params['link'][0])
  xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=streams['best'].to_url()))


def print_main_menu():
  xbmcplugin.setPluginCategory(_handle, 'Italy TV')
  xbmcplugin.setContent(_handle, 'videos')

  videoItem = xbmcgui.ListItem("LiveHereOne")
  videoItem.setInfo('video', {'title': "LiveHereOne", 'mediatype': 'video'})
  data = {
      "action": "scrape_livehere_channels",
      "title": "LiveHereOne"
      }
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=True)

  if (sportlive_enabled):
    videoItem = xbmcgui.ListItem("SportLive")
    videoItem.setInfo('video', {'title': "SportLive", 'mediatype': 'video'})
    data = {
        "action": "scrape_sportlive_channels",
        "title": "SportLive"
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=True)

  xbmcplugin.endOfDirectory(_handle)


xbmc.log(" ".join(sys.argv), xbmc.LOGINFO)


def router(paramstring):
  try:
    xbmc.log("paramstring: {0}".format(paramstring), xbmc.LOGINFO)
    params = urllib.parse.parse_qs(paramstring)
  except Exception as e:
    xbmc.log("type error: " + str(e), xbmc.LOGERROR)
    params = False

  xbmc.log("params: {0}".format(params), xbmc.LOGINFO)

  if params:
    if params['action'][0] == 'play_directlink':
      play_directlink(params)
    elif params['action'][0] == 'play_streamlink':
      play_streamlink(params)
    elif params['action'][0] == 'scrape_livehere_channels':
      lh1.list_channels()
    elif params['action'][0] == 'scrape_livehere_links':
      lh1.list_links(params)
    elif params['action'][0] == 'scrape_sportlive_channels':
      sl1.list_channels(sportlive_pass)
    else:
      print_main_menu()
  else:
    print_main_menu()

if __name__ == '__main__':
  router(sys.argv[2][1:])
