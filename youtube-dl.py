from pytube import YouTube
from os import mkdir
from os.path import isdir
from re import findall
from colorama import Fore, Style
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from datetime import datetime


class Youtube_downloader(object):

    def download(self,link ,file_type='video'):
        '''
        file_type -> audio or video
        '''
        yt = YouTube(link)
        
        # in progressive make sure video has sound and filter only for video/mp4 files
        try:
            if file_type == 'video':
                streams = yt.streams.filter(progressive=True, mime_type="video/mp4")
            elif file_type == 'audio':
                streams = yt.streams.filter(only_audio=True, mime_type="audio/mp4")
            else :
                return 'file_type is wrong please change it to audio or video'
        except:
            raise TimeoutError('Make sure your internet connection is working normally or turn on the VPN.')
        
        title = yt.title
        resolutions = []
        for stream in streams :
            if file_type == 'video':
                resolutions.append(stream.resolution)
            elif file_type == 'audio':
                resolutions.append(stream.abr)

        str_resolutions = ' '.join(map(str, resolutions))
        
        while True:
            choice = input(f'resolutions available is [{str_resolutions}] choose > ')

            verify = False
            for i in resolutions :
                if choice == i:
                    verify = True
                    break

            if verify == False:
                print(Fore.RED + 'Please Choose between the resolutions !!' + Style.RESET_ALL)
                continue
            break
        
        print(Fore.GREEN + 'Downloading...' + Style.RESET_ALL)
        
        if file_type == 'video':
            yt.streams.filter(res=choice).first().download(f'Downloads/{title}', filename=f'{title}-{choice}.mp4')
        elif file_type == 'audio':
            yt.streams.filter(only_audio=True, abr=choice).first().download(f'Downloads/{title}', filename=f'{title}-{choice}.mp3')

        print(f'completed. file path: ./Downloads/{title}')
    
    def download_subtitle(self, link):

        title = YouTube(link).title

        regex = 'watch\?v=(.*)'
        link = findall(regex, link)[0]

        transcript = YouTubeTranscriptApi.get_transcript(link)
        sub_formatter = WebVTTFormatter()
        # .turns the link into a srt file.
        srt = sub_formatter.format_transcript(transcript)

        # check directories 
        if isdir('Downloads') == False:
            mkdir('Downloads')        
        # if isdir('Downloads/subtitles') == False:
            mkdir('Downloads/subtitles')
            
        try:
            sub_path = f'Downloads/subtitles/{title}/{title}.srt'
            with open(sub_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt)
        except OSError:
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            sub_path = f'Downloads/subtitles/{now}.srt'
            with open(sub_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt)

        print(f'completed. subtitle path: ./{sub_path}')
