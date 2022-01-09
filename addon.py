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

import fn_janjua as janjua
import fn_wigistream as wigistream

import lib_livehereone as livehereone
import lib_sportlive as sportlive

addon = xbmcaddon.Addon()

liveproxy_enabled = addon.getSettingBool('liveproxy_enabled')
liveproxy_host = addon.getSetting('liveproxy_host')
liveproxy_port = addon.getSetting('liveproxy_port')

sportlive_enabled = addon.getSettingBool('sportlive_enabled')
sportlive_pass = addon.getSetting('sportlive_pass')

def add_directory_menu(data, _isPlayable, _isFolder):
  if ('link' in data and data['link'].startswith("//")):
    data['link'] = "https:" + data['link']

  videoItem = xbmcgui.ListItem(data['title'])
  videoItem.setInfo('video', {'title': data['title'], 'mediatype': 'video'})
  videoItem.setProperty('IsPlayable', _isPlayable)
  xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=_isFolder)
  xbmc.log(" ".join(data), xbmc.LOGINFO)


#def add_streamlink(link_title, link_strip):
#  add_directory_menu({"action": "play_streamlink", "title": "streamlink " + link_title, "link": link_strip}, 'true', False)
#  if (liveproxy_enabled):
#    newlink = str.encode("streamlink " + link_strip + " best")
#    add_directory_menu({"action": "play_directlink", "title": "liveproxy " + link_title, "link": "http://" + liveproxy_host + ":" + liveproxy_port + "/base64/" + base64.urlsafe_b64encode(newlink).decode('utf-8') + "/"}, 'true', False)


def play_directlink(params):
  xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=params['link'][0]))


def play_streamlink(params):
  streams = streamlink.streams(params['link'][0])
  xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=streams['best'].to_url()))


def play_janjua(params):
  stream = janjua.extract_link(params['link0'][0], params['link1'][0])
  xbmc.log("Final janjua url: {0}".format(stream), xbmc.LOGINFO)
  if stream:
    xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=stream))


def play_wigistream(params):
  if 'wigiid' in params:
    stream = wigistream.extract_link(params['link'][0], params['wigiid'][0])
  else:
    stream = wigistream.extract_link(params['link'][0])
  xbmc.log("Final wigistream url: {0}".format(stream), xbmc.LOGINFO)
  if stream:
    xbmcplugin.setResolvedUrl(_handle, True, listitem=xbmcgui.ListItem(path=stream))


def print_main_menu():
  xbmcplugin.setPluginCategory(_handle, 'Italy TV')
  xbmcplugin.setContent(_handle, 'videos')

  add_directory_menu({"action": "scrape_livehereone_channels", "title": "LiveHereOne"}, 'false', True)

  if (sportlive_enabled):
    add_directory_menu({"action": "scrape_sportlive_channels", "title": "SportLive"}, 'false', True)

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
    elif params['action'][0] == 'play_janjua':
      play_janjua(params)
    elif params['action'][0] == 'play_wigistream':
      play_wigistream(params)
    elif params['action'][0] == 'scrape_livehereone_channels':
      livehereone.list_channels()
    elif params['action'][0] == 'scrape_livehereone_links':
      livehereone.list_links(params)
    elif params['action'][0] == 'scrape_sportlive_channels':
      sportlive.list_channels(sportlive_pass)
    else:
      print_main_menu()
  else:
    print_main_menu()

if __name__ == '__main__':
  router(sys.argv[2][1:])
