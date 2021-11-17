import xbmc
import xbmcgui
import xbmcplugin
import re
import requests
import urllib

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Referer': 'https://sportlivefree.xyz/sport1.html'
    }

parsed = []


def list_channels(sportlive_pass):
  from addon import _pid
  from addon import _handle

  xbmcplugin.setPluginCategory(_handle, 'SportLive')
  xbmcplugin.setContent(_handle, 'videos')

  html_doc = requests.get("https://sportlivefree.xyz/{0}.php".format(sportlive_pass), headers=headers).text
  #xbmc.log(html_doc, xbmc.LOGINFO)

  chs_in = re.findall(r'\n.*?<sup>\s\([0-9]+\)<\/sup>', html_doc)
  for ch_in in chs_in:
    link_title = re.sub(r'<[^>]+>', '', ch_in).strip()
    link_id = re.search(r'\(([0-9]+)\)', ch_in).group(1)

    videoItem = xbmcgui.ListItem(link_title)
    videoItem.setInfo('video', {'title': link_title, 'mediatype': 'video'})
    data = {
        "action": "play_wigistream",
        "title": link_title,
        "link" : "https://starlive.xyz/embed.php?id=live{0}m".format(link_id),
        }
    xbmcplugin.addDirectoryItem(handle=_handle, url='{0}?{1}'.format(_pid, urllib.parse.urlencode(data)), listitem=videoItem, isFolder=True)
    xbmc.log("{0}: {1}".format(link_title, link_id), xbmc.LOGINFO)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
  xbmcplugin.endOfDirectory(_handle)

