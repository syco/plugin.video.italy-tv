import xbmc
import xbmcgui
import xbmcplugin
import re
import requests
from bs4 import BeautifulSoup

FFUA = 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'

headers = {
    'User-Agent': FFUA,
    'Referer': 'https://easysite.one/'
    }

parsed = []

def list_channels():
  from addon import _pid
  from addon import _handle
  from addon import add_directory_menu

  xbmcplugin.setPluginCategory(_handle, 'WebTvHD')
  xbmcplugin.setContent(_handle, 'videos')

  channels_list = [
      {"title": "Rai 1", "link": "https://webserver.one/Live/Rai_1_HD_Online.php"},
      {"title": "Rai 2", "link": "https://webserver.one/Live/Rai_2_HD_Online.php"},
      {"title": "Rai 3", "link": "https://webserver.one/Live/Rai_3_HD_Online.php"},
      {"title": "Rai 4", "link": "https://webserver.one/Live/Rai_4_HD_Online.php"},
      {"title": "Rai Movie", "link": "https://webserver.one/Live/RaiMovie_HD_Online.php"},
      {"title": "La 7", "link": "https://webserver.one/Live/La_7_HD_Online.php"},
      {"title": "La 7d", "link": "https://webserver.one/Live/La_7d_HD_Online.php"},
      {"title": "Tv 8", "link": "https://webserver.one/Live/Tv_8_Online.php"},
      {"title": "Cielo", "link": "https://webserver.one/Live/Cielo_Tv_Online.php"},
      {"title": "Nove", "link": "https://webserver.one/Live/Nove_Tv_HD_Online.php"},
      {"title": "DMAX", "link": "https://webserver.one/Live/DMAX_HD_Online.php"},
      {"title": "Real Time", "link": "https://webserver.one/Live/RealTime_HD_Online.php"},
      {"title": "Giallo", "link": "https://webserver.one/Live/Giallo_Tv_HD_Online.php"},
      {"title": "Motor Trend", "link": "https://webserver.one/Live/Motor_Trend_HD_Online.php"},
      {"title": "Food Network", "link": "https://webserver.one/Live/Food_Network_HD_Online.php"},
      {"title": "Super", "link": "https://webserver.one/Live/Super_HD_Online.php"},
      {"title": "Spike", "link": "https://webserver.one/Live/Spike_Tv_HD_Online.php"},
      {"title": "Paramount", "link": "https://webserver.one/Live/Paramount_Channel_HD_Online.php"}
      ]

  for channel in channels_list:
    add_directory_menu({"action": "scrape_webtvhd_links", "title": channel['title'], "link": channel['link']}, 'true', False)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
  xbmcplugin.endOfDirectory(_handle)

def add_links_rec(url_in, loop):
  from addon import _pid
  from addon import _handle
  from addon import add_directory_menu

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
        if "mailocal.xyz" in link_strip or "mailocal2.xyz" in link_strip or "easysite.one" in link_strip or "open-live.org" in link_strip:
          add_links_rec(link_strip, loop + 1)
        else:
          add_directory_menu({"action": "play_streamlink", "title": "iframe " + link_strip, "link": link_strip}, 'true', False)
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
      add_directory_menu({"action": "play_streamlink", "title": "video " + link_strip, "link": link_strip}, 'true', False)

    m3u8s_list = re.findall(r'https?:\/\/.*?\.m3u8', html_in)
    for link_strip in m3u8s_list:
      add_directory_menu({"action": "play_directlink", "title": "m3u8 " + link_strip, "link": link_strip}, 'true', False)

    j_channel_re = re.search(r'channel=\'[^\']+', html_in)
    j_g_re = re.search(r'g=\'[^\']+', html_in)
    if j_channel_re and j_g_re:
      j_channel = j_channel_re.group().split('\'')[1]
      j_g = j_g_re.group().split('\'')[1]
      if j_channel and j_g:
        add_directory_menu({"action": "play_janjua", "title": "janjua " + j_channel, "link0": j_channel, "link1": j_g}, 'true', False)

def list_links(params):
  from addon import _handle

  xbmcplugin.setPluginCategory(_handle, 'Italy TV')
  xbmcplugin.setContent(_handle, 'videos')

  add_links_rec(params['link'][0], 0)

  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
  xbmcplugin.endOfDirectory(_handle)

