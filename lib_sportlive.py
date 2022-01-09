import xbmc
import xbmcgui
import xbmcplugin
import re
import requests
from bs4 import BeautifulSoup

FFUA = 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'

headers = {
    'User-Agent': FFUA,
    'Referer': 'https://sportlivefree.xyz/sport1.html'
    }

parsed = []


def list_channels(sportlive_pass):
  from addon import _pid
  from addon import _handle
  from addon import add_directory_menu

  xbmcplugin.setPluginCategory(_handle, 'SportLive')
  xbmcplugin.setContent(_handle, 'videos')

  html_doc = requests.get("https://sportlivefree.xyz/{0}.php".format(sportlive_pass), headers=headers).text
  html_doc = html_doc.replace('<tr class="">', '</td></tr><tr class="">')
  #xbmc.log(html_doc, xbmc.LOGINFO)
  soup = BeautifulSoup(html_doc, 'html.parser')

  seriea = soup.find('div', id='seriea')
  if seriea:
    cols = seriea.find_all('td');

    for col in cols:
      link_title = col.get_text().strip()
      link_id_re = re.search(r'\(([0-9]+)\)', link_title)
      if link_id_re:
        link_id = link_id_re.group(1)
        add_directory_menu({"action": "play_wigistream", "title": link_title, "link": "https://starlive.xyz/embed.php?id=live{0}m".format(link_id)}, 'true', False)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
  xbmcplugin.endOfDirectory(_handle)

