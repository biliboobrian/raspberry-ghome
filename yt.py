#!/usr/bin/env python

import pafy
import vlc, time

url = "https://www.youtube.com/watch?v=cvRbhpvnUuc"
video = pafy.new(url)
best = video.getbestaudio()
playurl = best.url

Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(playurl)
Media.get_mrl()
player.set_media(Media)
player.play()

print(player.get_state())
time.sleep(1.5)
duration = player.get_length() / 1000
time.sleep(duration)