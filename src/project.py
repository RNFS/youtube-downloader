import re
from pytube import YouTube
import sys
import argparse

"""
    TODO we need to allow the user to choose the folder to store the data in
"""


def main():
    # handel the CLI and according to the returned option call either voice or vido func
    args = cli()
    if args["voice"]:
        voice()
    else:
        video()


def option(data, type="video"):
    """return a list of the available options and according to the given data,
    take the input from the user acordding to the printed data,
    and consider the input as the itag for the quality
    for either the muisc func or the verdio fun
    - only supprted format utill now is Mb4"""

    options = {}
    l_options = []
    for i in data:
        # for voice search for the itag and the abr num which like p for vidoes for the quality
        if type == "audio":
            matches = re.search(
                r"^.* itag=\"(\d+).* mime_type=\"audio/mp4\" abr=\"(\d+).*$",
                f"{i}",
                re.IGNORECASE,
            )
        # if a vedio which is the default value for type , search for the itag and the res num
        else:
            matches = re.search(
                r"^.* itag=\"(\d+).* mime_type=\"video/mp4\" res=\"(\d+).*$",
                f"{i}",
                re.IGNORECASE,
            )

        if matches:
            options["itag"], options["qu"] = matches.groups()
            # we need to recreat another dict because we can't override the values data because they are str\
            # str, int, floot, tuple and so on are immutable
            l_options.append(options)

        options = {}

    if not l_options:
        raise ValueError("couldn't find matching patter for the options")

    # after storing the matched data render it to the user so they can choose one tag which is equivalent to itag
    tags = []
    print(f"choose one tag for the desired quality")
    # pixels for video and kilobyte per second for voice quality
    q = "p"
    if type == "audio":
        q = "kbps"

    for i in l_options:
        tags.append(i["itag"])
        print(f"choose {i['itag']} for {i['qu']}{q}")

    itag = input("Tag: ")
    print("...")
    # if input is not in the renderd data then exit with an error message
    if not itag in tags:
        sys.exit("Invalid choise")
    # if everthing went good then return the itag which will be used to download the file
    return itag


# download muisc only
def voice():
    # get the data of that file
    try:
        if url := input("URL: ").strip():
            pass
        else:
            sys.exit("invalid url")

        yt = YouTube(url)
        data = yt.streams.filter(only_audio=True)

        # option will render the avai options itags so the user can choose one of them and then returns it's itag
        itag = int(option(data, type="audio"))

        # download the voice file with the choosen itag and save it in the voice folder
        stream = yt.streams.get_by_itag(itag)
        stream.download("./voice/")

    except:
        # TODO we nedd to parse the exceptions and hundel them individually
        sys.exit("couldn't download this file")

    print("the file has been downloaded sucssfully")


# download  video only
def video():
    # get the data of that file
    try:
        if url := input("URL: ").strip():
            pass
        else:
            sys.exit("Invaild url")

        yt = YouTube(url)

        data = yt.streams.filter(progressive=True)

        # option will render the avai options so the user can choose one of them and then returns it's itag
        itag = int(option(data, type="video"))

        # download the video with the choosen itag and save it in the videos folder
        stream = yt.streams.get_by_itag(itag)
        stream.download("./videos/")

    except:
        # TODO we nedd to parse the exceptions and hundel them individually
        sys.exit("couldn't download this file")

    print("the file has been downloaded sucssfully")


def cli():
    """TODO handel the CLI args get the option [-m | --voice] | [-v|--video]
    then return the option"""
    parser = argparse.ArgumentParser(description="download a voice or a video file from youtube")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m", "--voice", action="store_true", help="download file in a muisc formate"
    )
    group.add_argument(
        "-v", "--video", action="store_true", help="download file in a video format"
    )

    args = parser.parse_args()
    option = {}
    if args.voice:
        option["voice"] = True
        option["video"] = False
    # default format is video if voice is not specifed
    else:
        option["video"] = True
        option["voice"] = False

    return option


if __name__ == "__main__":
    main()