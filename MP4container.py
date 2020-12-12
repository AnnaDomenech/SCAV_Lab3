import sys
import os
import re
from pathlib import Path
import json, subprocess
import numpy as np

DEFAULT = 1
PERSONALIZED = 2

class MP4container:
    videocodecs=['mpeg2video', 'h264','mp4']
    audiocodecs=['aac', 'mp3', 'ac3','dra','mp2']
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
        self.codecs = None
        self.subtitles = None
        self.output = None

    # DVB  : Audio: AAC, Dolby Digital (AC-3), MP3 // Video: MPEG2, h.264
    # ATCS : Audio: AC-3 // Video: MPEG2, h.264
    # ISDB : Audio: AAC // Video: MPEG2, h.264
    # DTMB : Audio: DRA, AAC, AC-3, MP2, MP3 // Video: MPEG2, h.264, AVS, AVS+

    def getVBroadcastingStd(self):
        video_std = []
        if ('h264' in self.codecs or 'mpeg2video' in self.codecs):
            video_std.extend(["DVB", "ATCS", "ISDB", "DTMB"])
        elif ('avs' in self.codecs or 'avs+' in self.codecs):
            video_std.append("DTMB")
        return video_std

    def getABroadcastingStd(self):
        audio_std = []
        if 'aac' in self.codecs:
            audio_std.extend(["DVB", "ISDB", "DTMB"])
        if 'mp3' in self.codecs:
            audio_std.extend(["DVB", "DTMB"])
        if 'ac3' in self.codecs:
            audio_std.extend(["DVB", "ATCS", "DTMB"])
        if ("dra" in self.codecs or "mp2" in self.codecs):
            audio_std.append("DTMB")
        return audio_std

    def getBroadcastingStd(self):
        proc = subprocess.Popen(
            [f"ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {self.video}"], stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
        output, err = proc.communicate()
        codeclist = str(output).split("'")[1].split('\\n')
        codeclist.pop()
        self.codecs = list(np.unique(codeclist))
        print('\nThe choosed file have the following audio and video codecs:\n', self.codecs)

        broadcasting_std = list(set(self.getVBroadcastingStd()) & set(self.getABroadcastingStd()))
        if not broadcasting_std:
            print("ERROR: Any broadcasting standard fit")
        else:
            print('This container fits the following broadcasting standards:\n',
                  broadcasting_std)

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

    def print_files(self,ext):
        self.setfiles(self.path)
        if ext == 'all':
            for file in self.files:
                print('{} - {}'.format(file[0], file[1]))
        elif ext in self.videocodecs:
            for file in self.files:
                if file[1].split('.')[1]==ext:
                    print('{} - {}'.format(file[0], file[1]))
        elif ext in self.audiocodecs:
            for file in self.files:
                if file[1].split('.')[1]==ext:
                    print('{} - {}'.format(file[0], file[1]))
        elif ext=='str':
            for file in self.files:
                if file[1].split('.')[1]==ext:
                    print('{} - {}'.format(file[0], file[1]))


    def extractAudiofromVideo(self,dur = '00:01:00', init ='00:00:00', cut=True):
        keep=str(input("Extract Mono audio?[y/n]"))
        if keep =='y':
            self.extractMonoTrack(dur=dur,init=init, cut=cut)
        
  
    def videosettings(self):
        self.print_files('mp4')
        index = int(input("Indicate video track:"))
        self.inp=self.files[index-1][1]
        x = str(input("Do you want to cut the video?[y/n]"))
        if x =='y':
            dur=str(input("Enter desired duration in XX:XX:XX format :"))
            init=str(input("Enter desired init time in XX:XX:XX format:"))
            self.extractAudiofromVideo(dur,init)
            self.cutvideo(dur,init)
        else:
            self.cutvideo(cut=False)
            self.extractAudiofromVideo()
        

    def cutvideo(self, dur = '00:01:00', init ='00:00:00', cut=True ):
        output = str(self.path / "cut_{}".format(self.inp))#set output video name
        if not cut:
            self.video=self.inp
        elif cut:
            command = f"ffmpeg -ss {init} -i {self.path / self.inp} -t {dur} -an {output}"#ffmpeg command
            os.system(command)
            self.video = output #change input dir to work with the cutted video
    
    def audiosettings(self):
        if self.mono==None:
            self.print_files('mp3')
            index= int(input("Enter audio track to include in mp4 container:\n"))
            self.mono = self.files[index-1][1]
        if self.monol == None:
            index= int(input("Enter another audio track to include in mp4 container:\n 0-To do not add more"))
            if index>0:
                self.mono = self.files[index-1][1]

        
    def extractMonoTrack(self, codec = 'mp3', lowerbitrate=True, dur = '00:01:00', init = '00:00:00',cut=True):
        name = self.inp.split('.')
        self.mono = str(self.path / "mono_{}.{}".format(name[0],codec))#set output video name and path
        if cut:
            command = f"ffmpeg -ss {init} -i  {self.path / self.inp}  -t {dur} -acodec {codec} -ac 1 {self.mono}"#ffmpeg command
        elif not cut:
            command = f"ffmpeg -i  {self.path / self.inp} -acodec {codec} -ac 1 {self.mono}"#ffmpeg command
        os.system(command)
        if lowerbitrate:
            self.monol = str(self.path / "mono_lowerbitrate_{}.{}".format(name[0],codec))#set output video name and path
            command =f"ffmpeg -i  {self.mono} -ac 1 -ar 44100 -b:a 32k -acodec {codec} -map 0 {self.monol}"
            os.system(command)  

    def subtitlesettings(self):
        self.print_files(ext='str')
        index = int(input("Enter the subtitle track to include in mp4 container:"))
        self.setsubtitles(self.files[index-1][1])

    def setsubtitles(self,name=None):
        if name == None:
           name = "subtitles.srt"
        self.subtitles = str(self.path / "subtitles.mp4")
        command = f"ffmpeg -i {self.path / name} {self.path}/subs.ass"
        os.system(command)
        command = f'ffmpeg -i {self.path / self.video} -i {self.path}/subs.ass -vf "ass={self.path}/subs.ass" {self.subtitles}'
        os.system(command)
        
    def setPath(self):
        path=str(input("Enter folder name:"))
        self.path = Path.cwd() / "{}".format(path)
        print(self.path)
        self.files=self.setfiles(self.path)
    
    def createContainer(self, var):
        if var == DEFAULT:
            self.cutvideo()
            self.extractMonoTrack()
            self.setsubtitles()
        if var == PERSONALIZED:
            self.videosettings()
            self.audiosettings()
            self.subtitlesettings()

    def finalContainerMenu(self,type):
        if type == DEFAULT:
            self.createContainer(type)
        elif type == PERSONALIZED:
            aux = input("You are in the desired folder?[y/n]")
            if aux =='n':
                self.setPath()
                self.finalContainerMenu(type)
            elif aux == 'y':
                self.createContainer(type)

        aux=str(input("Enter MP4 Container name(without.mp4):"))
        print(self.videocodecs[0], self.videocodecs[1])
        videocodec = int(input("Which video codec do you want?(1 or 2)"))
        command = f'ffmpeg -i {self.path / self.video} -i {self.mono} -i {self.monol} -map 0:v -map 1:a -map 2:a -c:a copy -c:v {self.videocodecs[videocodec]} -vf "ass={self.path}/subs.ass" {self.path/aux}.mp4'
        os.system(command)
       