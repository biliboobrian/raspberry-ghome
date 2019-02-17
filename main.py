#!/usr/bin/env python

from __future__ import print_function

import re
import argparse
import os.path
import json
import vlc
import youtube_dl

import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file


ydl_opts = {
    'default_search': 'ytsearch1:',
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True
}
vlc_instance = vlc.get_default_instance()
vlc_player = vlc_instance.media_player_new()
volume = 100

def change_volume(level):
    volume = level
    if vlc_player.get_state() == vlc.State.Playing:        
        vlc_player.audio_set_volume(volume)

def play_music(name):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(name, download=False)
    except Exception:
        print('Sorry, I can\'t find that song.')
        return

    if meta:
        info = meta['entries'][0]
        vlc_player.set_media(vlc_instance.media_new(info['url']))
        print('Now playing ' + re.sub(r'[^\s\w]', '', info['title']))
        vlc_player.play()
        print('Changement du volume à ', volume)
        vlc_player.audio_set_volume(volume)

def process_event(assistant, event):
    """Pretty prints events.
    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.
    Args:
        event(event.Event): The current event to process.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        if vlc_player.get_state() == vlc.State.Playing:  
            print('Changement du volume à 30')      
            vlc_player.audio_set_volume(30)
        print()

    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()
        if vlc_player.get_state() == vlc.State.Playing:
            vlc_player.audio_set_volume(volume)

    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text.startswith('joue '):
            print('ENTER VLC ASSISTANT PROCESS')
            assistant.stop_conversation()
            play_music(text[5:])
        elif text.startswith('change le volume à '):
            print('ENTER VLC CHANGE LEVEL TO ', text[19:])
            assistant.stop_conversation()
            change_volume(int(text[19:]))
        elif text.startswith('stoppe la musique'):
            assistant.stop_conversation()
            print('STOP CURRENT PLAYBACK ON VLC')
            if vlc_player.get_state() == vlc.State.Playing:
                vlc_player.stop()
        else:
            if vlc_player.get_state() == vlc.State.Playing:
                vlc_player.stop()

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('/home/pi/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials, 'Raspberry') as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()