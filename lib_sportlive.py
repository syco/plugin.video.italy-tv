import xbmc
import xbmcgui
import xbmcplugin
import re
import requests
import urllib
from bs4 import BeautifulSoup

from addon import _pid
from addon import _handle
from addon import add_directlink
from addon import add_streamlink

import fn_janjua as janjua

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Referer': 'https://sportlivefree.xyz/sport1.html'
    }

parsed = []


def list_channels(sportlive_pass):
  xbmcplugin.setPluginCategory(_handle, 'SportLive')
  xbmcplugin.setContent(_handle, 'videos')

  html_doc = requests.get("https://sportlivefree.xyz/{0}.php".format(sportlive_pass), headers=headers).text
  #xbmc.log(html_doc, xbmc.LOGINFO)
  soup = BeautifulSoup(html_doc, 'html.parser')

  #channels_grid = soup.find_all('ul', ['dropdown-menu menu-depth-1'])[1]

  #channels_cols = channels_grid.find_all('li', ['menu-item-depth-1'])
  #for channels_col in channels_cols:
  #  header = channels_col.find('a', ['menu-link', 'sub-menu-link'])
  #  header_title = "[COLOR red][B][UPPERCASE]{0}[/UPPERCASE][/B][/COLOR]".format(header.getText().strip())

  #  if header_title not in parsed:
  #    parsed.append(header_title)

  #    headerItem = xbmcgui.ListItem(header_title)
  #    headerItem.setInfo('video', {'title': header_title, 'mediatype': 'video'})
  #    headerItem.setProperty('IsPlayable', 'false')
  #    xbmcplugin.addDirectoryItem(handle=_handle, url="", listitem=headerItem, isFolder=False)

  #    xbmc.log("---------------------------", xbmc.LOGINFO)
  #    xbmc.log(header_title, xbmc.LOGINFO)

  #    channels_list = channels_col.find_all('li', ['menu-item-depth-2'])
  #    for channel in channels_list:
  #      link = channel.find('a')
  #      link_title = link.getText().strip()

  #      videoItem = xbmcgui.ListItem(link_title)
  #      videoItem.setInfo('video', {'title': link_title, 'mediatype': 'video'})
  #      data = {
  #          "action": "scrape_livehere_links",
  #          "title": link_title,
  #          "link" : link.get('href')
  #          }
  #      xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=True)
  #      xbmc.log("{0}: {1}".format(link_title, link.get('href')), xbmc.LOGINFO)

  #    xbmc.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^", xbmc.LOGINFO)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
  xbmcplugin.endOfDirectory(_handle)

