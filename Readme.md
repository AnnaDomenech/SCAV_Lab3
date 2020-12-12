# SCAV - Lab 3
We assume that the user have all the needed files in a folder called Data.
In this case i will not explain the lab exercice by exercice, i will explain how to manage and how works the final script.

When you call Lab3.py appears the following menu:
1. Define MP4 Container
2. Display Folder files
4. Check Broadcasting of Default video
5. Testing

## Mp4 Container Class
The first step has been implementing a MP4Container class which contains all the requested exercices to do. This class is designed to being able to create a default mp4 container with a predefined parameters - as duration, audio codec - or a personalized mp4 container.
The final container in both options is created using:
````
command = f'ffmpeg -i {self.path / self.video} -i {self.mono} -i {self.monol} -map 0:v -map 1:a -map 2:a -c:a copy -c:v {self.videocodecs[videocodec]} -vf "ass={self.path}/subs.ass" {self.path/aux}.mp4'
        
````
Where -map0:v copy the video stream of the first input, -map1:a and -map2:a copy the audio tracks with its parameters(-c:a copy), the video codec is choosed by the user and the subtitles are added using -vf "ass={self.path}/subs.ass" .

### Personalized Option
In this option you are able to:
- Get all the needed tracks to construct a mp4 container.
- From a chosen video custom the MP4 container:
    - Choose the desired video and cut it or not.
        - From this video the user will be asked to extract audio
    - Choose the desired audio.
    - Choose the desired subtitles.
Notice that in the case the user is not in the desired folder, can change the path to work with the desired folder. Once the user have created the desired mp4 container, the user is returned to the menu.

## Display Folder Files
This menu option is a method of the MP4 container class, i think that is needed that the user being able to see the current state of the folder which is working with.

## Check BBB Broadcasting
In this option the user is able to see the codecs of the default MP4 container and which broadcasting standards fits. 
This are what i have obtained:
`The choosed file have the following audio and video codecs:['h264', 'mp3']`
`This container fits the following broadcasting standards:['DTMB', 'DVB']`

## Testing

Since the user is able to create the wanted MP4 Containers, this option is to check the codecs and the broadcasting containers of three MP4 containers. If the user do not want to check it for 3 videos is able to choose less files by putting 0 instead of the number of the file.
