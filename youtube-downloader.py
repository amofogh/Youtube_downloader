from pytube import YouTube
from os import mkdir
from os.path import isdir
from re import findall
from colorama import Fore,Style
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter


class Youtube_downloader(object):
    
    
    
    def download_video(self):
        print(Fore.MAGENTA + 'Youtube video downloader' + Style.RESET_ALL)
        
        link = input("Paste your video link here > ")
        print(Fore.CYAN + 'Please wait...' + Style.RESET_ALL)
        yt = YouTube(link)
        
        #in progressive make sure video has sound and filter only for mp4 files
        streams = yt.streams.filter(progressive=True , mime_type="video/mp4")
        
        # get res from these example --> '<Stream: itag="22" mime_type="video/mp4" res="720p" fps="25fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">'
        regex = 'res=\"(.*p)\"'
        result = self.__find(regex , streams)
        choice = self.__choose_verification('resoulation' , result)
        name = yt.title
        dir = self.__createdir(name)
        
        print(Fore.GREEN + 'Downloading...' + Style.RESET_ALL)
        if dir == False:
            streams.get_by_resolution(choice).download(f'Downloads',filename = f'{name}-{choice}.mp4')
        else:
            streams.get_by_resolution(choice).download(f'Downloads/{name}',filename = f'{name}-{choice}.mp4')
        print(Fore.GREEN + 'Download completed !!' + Style.RESET_ALL)

    def download_audio(self , mime_type = 'audio/mp4'):
        
        print(Fore.YELLOW + 'Youtube audio downloader' + Style.RESET_ALL)
        
        link = input("Paste your video link here > ")
        print(Fore.CYAN + 'Please wait...' + Style.RESET_ALL)
        yt = YouTube(link)
        streams = yt.streams.filter(only_audio=True , mime_type=mime_type)        
        
        # get abr from these example -->  <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">
        regex_abr = 'abr=\"(.*kbps)\"'
        result = self.__find(regex_abr , streams)
        choice = self.__choose_verification('abr' , result)
        
        # get itag from specifice abr
        regex = f'itag=\"(\d*)\" .*abr=\"{choice}\"'
        itag = self.__find(regex , streams)
        itag = int(itag.get('result_str'))
        
        name = yt.title
        dir = self.__createdir(name)
        
        print(Fore.GREEN + 'Downloading...' + Style.RESET_ALL)
        if dir == False:
            streams.get_by_itag(itag).download(f'Downloads', filename = f'{name}-{choice}.mp3')
        else:
            streams.get_by_itag(itag).download(f'Downloads/{name}', filename = f'{name}-{choice}.mp3')
        print(Fore.GREEN + 'Download completed !!' + Style.RESET_ALL)
    
    def download_subtitle(self):
        print(Fore.BLUE + 'Youtube subtitle downloader' + Style.RESET_ALL)
        link = input("Paste your video link here > ")
        print(Fore.CYAN + 'Please wait...' + Style.RESET_ALL)
        name = YouTube(link).title
        
        regex = 'watch\?v=(.*)'
        link = findall(regex , link)
        link = link[0]
        
        transcript = YouTubeTranscriptApi.get_transcript(link)
        sub_formatter = WebVTTFormatter()

        # .turns the link into a srt file.
        srt = sub_formatter.format_transcript(transcript)
        
        self.__createdir(name)
        
        with open(f'Downloads/{name}/{name}.srt', 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt)
        
    
    def __createdir(self,name):
        #check if dir not exists create it
        if isdir('Downloads') == False:
            mkdir('Downloads')
        while True :
            choice = input('Do you want create and put in folder for your file?(yes/no) > ')
            if choice == 'yes':
                if isdir(f'Downloads/{name}') == False:
                    mkdir(f'Downloads/{name}')
                break
            elif choice == 'no':
                return False
            else:
                print(Fore.RED + 'Choose between yes or no please !' + Style.RESET_ALL)
            
    def __choose_verification(self , types , result):
        '''
        types mean resoulation or abr
        result mean result returned from self.__find
        '''
        while True :
            choice = input(f'{types} available is {result.get("result_str")}choose > ')
            
            verify = False
            for i in result.get("result"):
                if choice == i :
                    verify = True
                    break
                
            if verify == False:
                print(Fore.RED + 'Please Choose between the resolutions !!' + Style.RESET_ALL)
                continue
            break
        return choice
    
    def __find(self , regex , streams):
        
        '''
        example: get res from this -->'<Stream: itag="22" mime_type="video/mp4" res="720p" fps="25fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">'
        '''
        #for check the input for right variable
        result = []
        # for print in choice input
        result_str = ''
        for stream in streams :
            
            res = findall(regex , str(stream))
            if res :
                result_str +=f'{res[0]} '
                #res[0] mean str res EX: res = ['128kbps'] --> '128kbps'
                result.append(res[0])
        
        return {'result':result , 'result_str':result_str}
    

        
y = Youtube_downloader()
# y.download_video()
# y.download_audio()
y.download_subtitle()

'''
https://www.youtube.com/watch?v=vbvyNnw8Qjg
'''

# progress bar for download