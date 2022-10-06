import re
from pytube import YouTube
import sys
import argparse

""" 
    TODO we need to allow the user to install a whole play list "cause i want to download my fav music list"
    TODO we need to allow the user to choose the folder to store the data in
"""


def main():
    # handel the CLI and according to the returned option call either music or vido func
    args = cli()
    if args["music"]:
        print(music())
    else:
        print(video())


def option(data, type_):
    """return a list of the available options and according to the given data,
    take the input from the user acordding to the printed data,
    and consider the input as the itag for the quality
    for either the muisc func or the verdio fun
    - only supprted format utill now is Mb4"""
    
    options = {}
    l_options = []
    num = 1

    if not data:
        raise ValueError("Couldn't handel the data!")
    # get all the mb4 options and store them in a the option dict
    for i in data:
        # for music search for the itag and the abr value e.g abr=140kbps which like p for vidoes for the quality
        if type_ == "audio":
            matches = re.search(
                r"^.* itag=\"(\d+).* mime_type=\"audio/mp4\" abr=\"(\d+).*$",
                f"{i}",
                re.IGNORECASE,
            )
        # if a vedio which is the default value for type , search for the itag and the res e.g res=720p num
        else:
            matches = re.search(
                r"^.* itag=\"(\d+).* mime_type=\"video/mp4\" res=\"(\d+).*$",
                f"{i}",
                re.IGNORECASE,
            )

        # if there are matches then add store them as a list of dicts
        if matches:
            options["itag"], options["qu"] = matches.groups()
            # we will use this number to render it to the user so they can choose it as the tag number to be clear
            options["num"] = num
            num += 1
            l_options.append(options)

        # we need to recreat another dict because we can't override the values data because they are str\
        # str, int, floot, tuple and so on are immutable
        options = {}
    if not l_options:
        raise ValueError("Couldn't handel the data!!")
    return {"l_options": l_options, "type_": type_}
    


""" this func to render the options to the user so he can choose an option and then return the choosed tag
get the list of options and the type of the file and a num equivalent to the itag number, as a dict
we have the itag parm to be able to pass it's value from the test file  
"""
def get_tag(dict, itag=None):
    l_options = dict["l_options"]
    type_ = dict["type_"]

    # the tag is what we will use to choose the deiserd qualty from the data the we get from Youtube
    # we will use get_by_itag object to choose the deiserd qualty

    if not l_options:
        raise ValueError("couldn't find matching patter for the options")

    """ after getting avai tags render it to the user so they can choose one choice which is 
    equivalent to itag for the qualty of the file  """

    tags = []
    print(f"choose one the following Choices for the desired quality")

    # pixels for video and kilobyte per second for music quality
    q = "p"
    if type_ == "audio":
        q = "kbps"

    for i in l_options:
        tags.append(i["num"])
        print(f"Choose: {i['num']}, for {i['qu']}{q}")
    
    if not itag:
        try:
            itag = int(input("Choice: "))
        except:
            print("Invalid Choise")
            sys.exit()

    # if input is not in the renderd data then exit with an error message
    if not itag in tags:
        print("Invalid Choise")
        sys.exit("Invalid choise !!")
    # l_options is list of dicts each dict has index itag = the index for that dict
    # which is the num inside that dict

    itag = l_options[itag - 1]["itag"]

    # if everthing went good then return the itag which will be used to download the file
    return itag



# download muisc only
""" we use all of the following args to be able to pass them form the test func in tests file,
without passing them the func will work normally too """

def music(url=None, download="y", itag=None, data=None):
    # get the data of that file
    try:
        if not url:
            if url := input("URL: ").strip():
                pass
            else:
                sys.exit("invalid url")

        print("Please wait ....")
        yt = YouTube(url)
        
        if not data:
            data = yt.streams.filter(only_audio=True)

        # option will render the avai options itags so the user can choose one of them and then returns it's itag
        if not itag:
            itag = int(get_tag(option(data=data, type_="audio")))
        print("Please wait ....")

        # download the music file with the choosen itag and save it in the music folder
        stream = yt.streams.get_by_itag(itag)
        if download == "y":
            stream.download("./music/")

    except:
        # TODO we nedd to parse the exceptions and hundel them individually
        sys.exit("couldn't download this file")

    return "the file has been downloaded sucssfully"


""" download  video only
# we use all of the following args to be able to pass them form the test func in tests file,
without passing them the func will work normally too """
def video(url=None, download="y", itag=None, data=None):
    # get the data of that file
    try:
        if not url:
            if url := input("URL: ").strip():
                pass
            else:
                sys.exit("Invaild url")

        print("Please wait ....")

        yt = YouTube(url)
        if not data:
            data = yt.streams.filter(progressive=True)

        # option will render the avai options so the user can choose one of them and then returns it's itag
        if not itag:
            itag = int(get_tag(option(data=data, type_="video")))
        print("Please wait ....")

        # download the video with the choosen itag and save it in the videos folder

        stream = yt.streams.get_by_itag(itag)
        if download=="y":
            stream.download("./videos/")

    except:
        # TODO we nedd to parse the exceptions and hundel them individually
        sys.exit("couldn't download this file")

    return "the file has been downloaded sucssfully"


def cli(argv=None):
    # we use argv to be able to pass a value from the test file
    if argv:
        try:
            sys.argv[1] = argv

        except IndexError:
            raise IndexError("couldn't assign argv to sys.argv[1]")
    
    """ handel the CLI args get the option [-m | --music] | [-v|--video]
    then return the option"""

    parser = argparse.ArgumentParser(
        description="download an audio or video file from youtube"
    )
    # parser.add_argument("-s", help="for test with pytest")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m", "--music", action="store_true", help="download file in a audio formate"
    )
    group.add_argument(
        "-v", "--video", action="store_true", help="download file in a video format"
    )

    args = parser.parse_args()
    option = {}
    if args.music:
        option["music"] = True
        option["video"] = False
    # default format is video if music is not specifed
    else:
        option["music"] = False
        option["video"] = True

    return option


if __name__ == "__main__":
    main()
