from project import cli, option, get_tag, music, video
from pytube import YouTube



def test_cli():
    assert cli(argv="-m") == {"music": True, "video": False}
    assert cli(argv="--music") == {"music": True, "video": False}
    assert cli(argv="-v") == {"music": False, "video": True}
    assert cli(argv="--video") == {"music": False, "video": True}

# store the date returned from option func globaly, to use for the get_tag func 
filtered_data_audio = 0
filtered_data_video = 0

# store the itags returned from get_tag func globaly so we can use them in muisc and viedo test funcs
itag_video = 0
itag_audio = 0

def test_option():
    yt = YouTube("https://youtu.be/5ceaqtWhdnI") 
    # store the date returned from the option func to use later with music and video and get_tag funcs

    global filtered_data_audio
    # for music/ audio data
    data = yt.streams.filter(only_audio=True)
    global filtered_data_audio
    filtered_data_audio = option(data, "audio")
    assert filtered_data_audio

    # for video data
    data = yt.streams.filter(progressive=True)
    global filtered_data_video
    filtered_data_video =  option(data, "video")
    assert filtered_data_video


def test_get_tag():
    # choose the first itag , and store the returned itag in a global var to user with music and viedo func
    # for audio data
    global filtered_data_audio
    global itag_audio
    itag_audio = get_tag(filtered_data_audio, itag=1) 
    assert itag_audio 
    
    # for viedo data
    global filtered_data_video
    global itag_video
    itag_video = get_tag(filtered_data_video, itag=1)
    assert itag_video


# use the same data form itag and option funcs 
def test_muisc():
    assert music(
        url="https://youtu.be/5ceaqtWhdnI", download="n", itag=itag_audio, data=filtered_data_audio
        ) == "the file has been downloaded sucssfully"


# use the same data form itag and option funcs 
def test_video():
    assert video(
         url="https://youtu.be/5ceaqtWhdnI", download="n", itag=itag_video, data=filtered_data_video
    ) == "the file has been downloaded sucssfully"