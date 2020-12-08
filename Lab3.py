import sys
import os
import re
from pathlib import Path
import json, subprocess

DEFAULT = 1
PERSONALIZED = 2

class MP4container:
    inp: str
    files: list
    path: str
    mono: str
    monol: str
    video: str
    subtitles: str
    def __init__(self,inp=None, files=None, path=None, name=False):
        self.inp, self.path = self.setdirectory(name)
        self.files = self.setfiles(self.path)
        self.mono = None
        self.monol = None
        self.video = None
        self.subtitles = None

    def setdirectory(self,name=False):
        path =  Path.cwd() / "Data"#set path to Data folder
        if not name:
            name = "BBB.mp4"
        file_path= [ subp for subp in path.iterdir() if subp.match(name)]
        file_path.sort()
        #for each file in folder get input path (BBB.mp4)
        return str(file_path[0].name),path

    def setfiles(self,path):
        files = [i for i in os.listdir(path) if i != '.DS_Store' and i != '.vscode' ]  # ignore random files
        return [(s + 1, i) for (s, i) in enumerate(files)]

    def print_files(self):
        for file in self.files:
            print('{} - {}'.format(file[0], file[1]))

    def extractAudiofromVideo(self,dur,init):
        keep=str(input("Extract audio?[y/n]"))
        if keep =='y':
            self.extractMonoTrack(dur=dur,init=init)
    
            
    def videosettings(self):
        self.print_files()
        index = int(input("Indicate video track:"))
        self.inp=self.files[index-1][1]
        x = str(input("You want to cut the video?[y/n]"))
        if x =='y':
            dur=str(input("Enter desired duration in XX:XX:XX format :"))
            init=str(input("Enter desired init time in XX:XX:XX format:"))
            self.extractAudiofromVideo(dur,init)
            self.cutvideo(dur,init)
        else:
            self.cutvideo()
        

    def cutvideo(self, dur = '00:01:00', init ='00:00:00', keep = False):
        output = str(self.path / "cut_{}".format(self.inp))#set output video name
        if keep:#keep audio
            command = f"ffmpeg -ss {init} -i {self.path / self.inp} -t {dur} {output}"#ffmpeg command
        else:
            command = f"ffmpeg -ss {init} -i {self.path / self.inp} -t {dur} -an {output}"#ffmpeg command
        os.system(command)
        self.video = output #change input dir to work with the cutted video
    
    def audiosettings(self):
        self.print_files()
        index= str(input("Enter audio track to include in mp4 container:\n"))
        self.mono = self.files[index-1][1]
        
    def extractMonoTrack(self, codec = 'mp3', lowerbitrate=True, dur = '00:01:00', init = '00:00:00'):
        name = self.inp.split('.')
        self.mono = str(self.path / "mono_{}.{}".format(name[0],codec))#set output video name and path
        command = f"ffmpeg -ss {init} -i  {self.path / self.inp}  -t {dur} -acodec {codec} -ac 1 {self.mono}"#ffmpeg command
        os.system(command)
        if lowerbitrate:
            self.monol = str(self.path / "mono_lowerbitrate_{}.{}".format(name[0],codec))#set output video name and path
            command =f"ffmpeg -i  {self.mono} -ac 1 -ar 44100 -b:a 32k -map 0 {self.monol}"
            os.system(command)  

    def subtitlesettings(self):
        self.print_files()
        index = str(input("Enter the subtitle track to include in mp4 container:"))
        self.setsubtitles(self.files[index-1][1])

    def setsubtitles(self,name=None):
        if name == None:
           name = "subtitles.srt"
        self.subtitles = str(self.path / "video_subs.mp4")#set output video name and path
        #os.system('ffmpeg -i {self.path / self.inp} -c copy -map 0:s -f null - -v 0 -hide_banner && echo {1} || echo {0}')
        #command = f"ffmpeg -i {self.path / self.inp} -i {self.path / name} -c copy -c:s mov_text Data/prova.mp4"
        #os.system(command)
        # check_command= 'ffmpeg {self.path / self.inp} -c copy -map 0:s -f null - -v 0 -hide_banner && echo {1} || echo {0}'
        # output = str(subprocess.Popen(check_command, shell = True, stdout=subprocess.PIPE).communicate()[0])
        # os.system(check_command)
        command = f"ffmpeg -i {self.path / self.video} -i {self.path / name}  -c:s mov_text {self.subtitles}"
        os.system(command)

    def setPath(self):
        path=str(input("Enter folder name:"))
        self.path = Path.cwd() / "{}".format(path)
        print(self.path)
        self.files=self.setfiles(self.path)
        
    def finalContainer(self,type):
        if type == DEFAULT:
            self.cutvideo()
            self.extractMonoTrack()
            self.setsubtitles()
        elif type == PERSONALIZED:
            aux = input("You are in the desired folder?[y/n]")
            if aux =='n':
                self.setPath()
                self.finalContainer(type)
            elif aux == 'y':
                self.videosettings()
                self.audiosettings()
                self.subtitlesettings()
        command =f"ffmpeg -i  {self.path / self.video} -i {self.mono} -i {self.path}/subtitles.srt -i {self.monol} -map 0:v -map 1:a -c:s mov_text -map 1:a Data/outpot.mp4"
        os.system(command)
    

if __name__ == "__main__": 
    var = int(input("[1] Default mp4 (BBB)\n [2]Personalized"))
    x = MP4container()
    x.finalContainer(var)
  
        
           

            
