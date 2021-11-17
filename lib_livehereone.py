import xbmc
import xbmcgui
import xbmcplugin
import re
import requests
import urllib
from bs4 import BeautifulSoup

import fn_janjua as janjua

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Referer': 'https://easysite.one/'
    }

parsed = []

def list_channels():
  from addon import _pid
  from addon import _handle

  xbmcplugin.setPluginCategory(_handle, 'LiveHereOne')
  xbmcplugin.setContent(_handle, 'videos')

  html_doc = requests.get("https://www.livehere.one/", headers=headers).text
  #xbmc.log(html_doc, xbmc.LOGINFO)
  soup = BeautifulSoup(html_doc, 'html.parser')

  channels_grid = soup.find_all('ul', ['dropdown-menu menu-depth-1'])[1]

  channels_cols = channels_grid.find_all('li', ['menu-item-depth-1'])
  for channels_col in channels_cols:
    header = channels_col.find('a', ['menu-link', 'sub-menu-link'])
    header_title = "[COLOR red][B][UPPERCASE]{0}[/UPPERCASE][/B][/COLOR]".format(header.getText().strip())

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
            "action": "scrape_livehere_links",
            "title": link_title,
            "link" : link.get('href')
            }
        xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=True)
        xbmc.log("{0}: {1}".format(link_title, link.get('href')), xbmc.LOGINFO)

      xbmc.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^", xbmc.LOGINFO)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
  xbmcplugin.endOfDirectory(_handle)

def add_links_rec(url_in, loop):
  from addon import add_directlink
  from addon import add_streamlink

  if (loop > 3):
    return

  if (url_in.startswith("//")):
    url_in = "https:" + url_in

  if url_in not in parsed:
    parsed.append(url_in)

    #html_in = requests.get(url_in, headers=headers).text
    html_in = re.sub(r'<!--(.*?)-->', '', requests.get(url_in, headers=headers).text)
    #xbmc.log(html_in, xbmc.LOGINFO)
    soup_in = BeautifulSoup(html_in, 'html.parser')

    iframes_in = soup_in.find_all('iframe')
    for iframe_in in iframes_in:
      try:
        link_strip = iframe_in.get('src')
        if "mailocal2.xyz" in link_strip or "easysite.one" in link_strip or "open-live.org" in link_strip:
          add_links_rec(link_strip, loop + 1)
        else:
          add_streamlink("iframe " + link_strip, link_strip)
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
      add_streamlink("video " + link_strip, link_strip)

    m3u8s_list = re.findall(r'https?:\/\/.*?\.m3u8', html_in)
    for link_strip in m3u8s_list:
      add_directlink("m3u8 " + link_strip, link_strip)

    j_channel_re = re.search(r'channel=\'[^\']+', html_in)
    j_g_re = re.search(r'g=\'[^\']+', html_in)
    if j_channel_re and j_g_re:
      j_channel = j_channel_re.group().split('\'')[1]
      j_g = j_g_re.group().split('\'')[1]
      if j_channel and j_g:
        link_janjua = janjua.extract_link(j_channel, j_g)
        if link_janjua:
          add_directlink("janjua", link_janjua)

def list_links(params):
  from addon import _handle

  xbmcplugin.setPluginCategory(_handle, 'Italy TV')
  xbmcplugin.setContent(_handle, 'videos')

  add_links_rec(params['link'][0], 0)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

