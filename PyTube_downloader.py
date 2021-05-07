import PySimpleGUI as gui
from pytube import YouTube,Stream
from datetime import date
import os
import time
import logging
import subprocess
import sys
import traceback

today = date.today() #date for new folder
d1 = today.strftime("%Y_%m_%d")
in_res=''

gui.theme('DarkTeal2')


layout = [
			[gui.Text("Video URL"), gui.Input(key='-URL-'), gui.Button('Fetch')],
			[gui.Text("Choose resolution")],
			[gui.Combo('',key='-RES_PICKER-')],
			[gui.Checkbox('open dir',default=True,key='-DIR-'), gui.Checkbox('Open vid',default=False,key='-PLAY-')],
			[gui.Text(size=(40,1), key='-OUTPUT-')],
			[gui.Button('Ok'), gui.Button('Quit')],
			[gui.Multiline(size=(80,5),key='-DEBUG-', auto_refresh=True)],
			]

window = gui.Window('Youtube downloader', layout)


debugos = ''

while True:
	event, values = window.read()
	if event in ('Quit', gui.WINDOW_CLOSED):
		break
	

	if event=='Fetch':
		window['-DEBUG-'].update(values);
		
		
		try:
			vid = YouTube(values['-URL-']) 
			res_set = set()
			dbg = ''
			for stream in vid.streams.filter(only_video='true'):
				dbg += 'Adding ' + stream.resolution + '\n'
				window['-DEBUG-'].update(dbg);
				res_set.add(stream.resolution)
			res_list = []
			res_list.extend(res_set)
			res_list.sort(key=lambda r: int(r[:-1]))
			window['-RES_PICKER-'].update(values=res_list);
			window['-DEBUG-'].update(res_list);
		except:
			window['-DEBUG-'].update(sys.exc_info());
			window['-OUTPUT-'].update('Invalid URL!', text_color='red')
		else:
			if in_res!='':
				window['-OUTPUT-'].update(vid.title + ' in '+ in_res , text_color='greenyellow')
			else:
				window['-OUTPUT-'].update('"' + vid.title+ '"' +' Please select a resolution!', text_color='yellow')

	
	if event == 'Ok':
		vid = YouTube(values['-URL-'])
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

		
	if event == gui.WINDOW_CLOSED or event == 'Quit':
		break

window.close()

	

	
