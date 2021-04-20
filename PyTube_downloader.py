import PySimpleGUI as sg
from pytube import YouTube
from datetime import date
import os
import time
import logging
import subprocess
import sys
import requests
import wget
from PIL import Image

today = date.today() #date for new folder
d1 = today.strftime("%Y_%m_%d")
in_res=''


layout = [
			[sg.Image(key='-THUMB-')],
			[sg.Text("Video URL")],
			[sg.Input(),sg.Button('check')],
			[sg.Text("Choose resolution")],
			[sg.Button('H(1080p)')
			,sg.Button('M(720p)')
			,sg.Button('L(480p)')],
			[sg.Checkbox('open dir', default=True, key='-DIR-'), sg.Checkbox('Open vid', default=False, key='-PLAY-')],
			[sg.Text(size=(40,1), key='-OUTPUT-')],
			[sg.Button('Ok'), sg.Button('Quit')],
			[sg.Text(size=(80,5), key='-DEBUG-')],
			]

window = sg.Window('Youtube downloader', layout)
event, values = window.read()


debugos = ''

while event != 'Quit' or event != sg.WINDOW_CLOSED:
	event, values = window.read()
	

	if event=='H(1080p)':
		in_res='1080p'
	elif event=='M(720p)':
		in_res='720p'
	elif event=='L(480p)':
		in_res='480p'

	if event=='check':
		
		try:
			vid = YouTube(values[0]) 
		except:
			window['-OUTPUT-'].update('Invalid URL!', text_color='red')
		else:
			thumb_name = wget.download(vid.thumbnail_url, out = 'D:\\youtubedl\\thumb')
			im = Image.open(thumb_name)
			img =im.resize((192,108))
			img.save(thumb_name, "png", optimize=True)
			window['-THUMB-'].update(thumb_name)
			if in_res!='':
				window['-OUTPUT-'].update(vid.title + ' in '+ in_res , text_color='greenyellow')
			else:
				window['-OUTPUT-'].update('"' + vid.title+ '"' +' Please select a resolution!', text_color='yellow')

	
	if event == 'Ok':
		vid = YouTube(values[0])
		if in_res=='':
			window['-OUTPUT-'].update('"' + vid.title+ '"' +' Please select a resolution!', text_color='yellow')
		else:
			for i in vid.streams: print(str(i))
			vid.streams.filter(res=in_res).first().download(r"D:\youtubedl"'\\' +d1+ '_vid')
			debugos+= 'Video is downloaded'
			window['-DEBUG-'].update(debugos);
			vid.streams.filter(only_audio=True).first().download(r"D:\youtubedl"'\\' +d1+ '_aud')
			debugos+='\nAudio is downloaded'
			window['-DEBUG-'].update(debugos);
			debugos+='D:\\Program_files\\ffmpeg\\bin\\ffmpeg.exe -i \'D:\\youtubedl\\'+d1+ '_vid\\'+vid.title+'.mp4\' -i \'D:\\youtubedl\\'+d1+ '_aud\\'+vid.title+'.mp4\' \'D:\\youtubedl\\final\\'+vid.title+'.mp4\''
			window['-DEBUG-'].update(debugos);
			print(debugos)
			os.system('D:\\Program_files\\ffmpeg\\bin\\ffmpeg.exe -i "D:\\youtubedl\\'+d1+ '_vid\\'+vid.title+'.mp4" -i "D:\\youtubedl\\'+d1+ '_aud\\'+vid.title+'.mp4" "D:\\youtubedl\\final\\'+vid.title+'.mp4"')
			window['-OUTPUT-'].update('Done!', text_color='greenyellow')
			if values['-DIR-']:
				path = 'D:\\youtubedl\\'+d1+'_vid' #open directory
				path = os.path.realpath(path)
				os.startfile(path)
			if values['-PLAY-']:
				new=vid.title.replace("|", "")
				os.startfile(r"D:\youtubedl"'\\' +d1+ r"_vid"'\\' + new + '.mp4' )

		
	if event == sg.WINDOW_CLOSED or event == 'Quit':
		break

window.close()

	

	
