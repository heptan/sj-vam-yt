import PySimpleGUI as gui
from pytube import YouTube,Stream
import os
import sys
import requests
import wget
from PIL import Image
import traceback


debug = gui.Print
gui.theme('DarkTeal2')

layout = [
            [gui.Text("Video URL"), gui.Input(key='-URL-', default_text="https://www.youtube.com/watch?v=uan8qs0gRjI"), gui.Button('Fetch',key='-FETCH_BUTTON-'), gui.Image(key='-THUMB-')],
            [gui.Text("Choose resolution")],
            [gui.Combo('',key='-RES_PICKER-', enable_events=True)],
            [gui.Text("Choose outpu folder")],
            [gui.FolderBrowse()],
            [gui.Checkbox('Open dir',default=True,key='-DIR-'), gui.Checkbox('Open vid',default=False,key='-PLAY-')],
            [gui.Button("Download",key='-DL_BUTTON-',disabled=True), gui.Button('Quit')],
            [gui.Text(size=(40,1), key='-OUT-')]
        ]


window = gui.Window('Youtube downloader', layout)


def fetch(values):
    try:
        vid = YouTube(values['-URL-']) 
        debug('vid initialized')
        
        res_set = set()
        for stream in vid.streams.filter(only_video='true'): #
            res_set.add(stream.resolution)
        res_list = list(res_set)
        res_list.sort(key=lambda r: int(r[:-1]))
        window['-RES_PICKER-'].update(values=res_list);
        thumb_name = wget.download(vid.thumbnail_url, out = 'D:\\youtubedl\\thumb')
        im = Image.open(thumb_name)
        img =im.resize((192,108))
        img.save(thumb_name, "png", optimize=True)
        window['-THUMB-'].update(thumb_name)
    except:
        debug(sys.exc_info());




#pytube.helpers.safe_filename !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# test  asdf    asdf    asdf    jf  adsfj   jjj jjjj    jj  j   jj  j



def download(values):
    vid = YouTube(values['-URL-'])
    debug('RES value: '+values['-RES_PICKER-'])
    vid.streams.filter(res=values['-RES_PICKER-']).first().download(r"D:\youtubedl\video_streams")
    debug('Video is downloaded');
    vid.streams.filter(only_audio=True).first().download(r"D:\youtubedl\audio_streams")
    debug('Audio is downloaded');
    debug(r'D:\Program_files\ffmpeg\bin\ffmpeg.exe -i "D:\youtubedl\video_streams'+'\\'+vid.title+r'.mp4" -i "D:\youtubedl\audio_streams'+'\\'+vid.title+r'.mp4" "D:\youtubedl\final'+'\\'+vid.title+r'.mp4"');
    os.system(r'D:\Program_files\ffmpeg\bin\ffmpeg.exe -i "D:\youtubedl\video_streams'+'\\'+vid.title+r'.mp4" -i "D:\youtubedl\audio_streams'+'\\'+vid.title+r'.mp4" "D:\youtubedl\final'+'\\'+vid.title+r'.mp4"')
    debug('Done')
    window['-OUT-'].update('Done!', text_color='greenyellow')
    if values['-DIR-']:
        path = os.path.realpath(r"D:\youtubedl\final")
        os.startfile(path)
    if values['-PLAY-']:
        new=vid.title.replace("|", "")
        os.startfile(r"D:\youtubedl\final"+"\\"+vid.title+r".mp4")


while True:
    event, values = window.read()

    if event in ('Quit', gui.WINDOW_CLOSED):
        break
        
    if event == '-RES_PICKER-':
        window['-DL_BUTTON-'].update(disabled=False)
        continue
    
    if event == '-FETCH_BUTTON-':
        fetch(values)
        continue

    if event == '-DL_BUTTON-':
        download(values)
        continue
        
        
window.close()
