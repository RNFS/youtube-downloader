# youtube-downloader
#### Video Demo:      
### Description: - this a command line tool to download music or video files from YouTube 
- user can download either a video or a music file, 
  according to the URL that will be given by the user and the   command line option
- by default, it will download a video if the user didn't specify the option
- you can choose the quality of the music file and the video file as well, mix quality for videos 720p till now
- the file will be downloaded in the same directory in a fill called videos or music according to the file type
- if an exception occurs the program will be terminated with an error message 
- usage: project.py [-h] [-m | -v]

        download music or videos from youtube

        optional arguments:
        -h, --help         show this help message and exit
        -m, --music      download file in a muisc formate
        -v, --video      download file in a video format
        
### project structure         
  we have two main files which are project.py and test_project.py
  and we have secondary files which are requirements.txt and README.md
## project.py 
  this file has the source code of the project, I have implemented in this file only functions 
  I didn't use any classes, and it imports two third-party libraries 
* pytube
* argparse
  and two built-in libraries 
* re
* import sys
  in this file we have 5 functions 
* __main__: which just calls the right function for downloading either a video or audio file 
* __cli__: for__ parsing the command line arguments and it returns a dictionary including the option chosen 
* __option__: for parsing the data received from the youtube API and returning the quality options available 
* __get_tag__: it prints the options available returned from the option function to the user, 
   and takes input as itag 
  and return that input so we can choose to download the file according to the selected itag
* __music__: it is responsible for downloading audio files 
* __video__: is responsible for downloading MB4/video files   
## test_project.py 
  in this file, I have implemented the test functions for each function 
  except for the main function in the project.py file
  test functions are 
* __test_cli__: which tests the function for parsing the command line arguments 
* __test_option__: which tests the function for parsing the data received from the youtube API 
  and return the quality options available 
* __test_get_tag__: for testing the function which prints the options available to the user and takes input as itag 
  and return that input so we can choose to download the file according to the selected itag
* __test_music__: test the function which is responsible for downloading audio files 
* __test_video__: test the function which is responsible for downloading audio files

## requirements.txt:
* pip install pytube
* pip install pytest
* pip install argparse

### README.md: just has the Description for this project