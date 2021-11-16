import re
import requests

def extract_link(j_channel, j_g):
  janjua_doc = requests.get("https://www.janjua.tv/hembedplayer/{0}/{1}/1920/1080".format(j_channel, j_g), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0', 'Referer': 'https://www.janjua.tv/'}).text
  janjua_video_re = re.search(r'enableVideo\("[^"]+', janjua_doc)
  if janjua_video_re:
    janjua_video = janjua_video_re.group().split('"')[1]
    if janjua_video:
      loadbalancer_doc = requests.get("https://www.tvportremote.com/loadbalancer").text
      loadbalancer = loadbalancer_doc.split('=')[1]
      if loadbalancer:
        return "https://{0}:8088/live/{1}/playlist.m3u8?id=1&pk={2}".format(loadbalancer, j_channel, janjua_video)
  return None

