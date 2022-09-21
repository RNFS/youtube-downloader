import re
from pytube import YouTube
import sys
import argparse


def main():
    # handel the CML and according to the returned option call either music or vido func
    args = clm()
    if args["music"]:
        music()
    else:
        video()


def option(data, type="video"):
    """we should return a list of the available options and take an input from the user
    acordding to the printed data and chose the itag according to the input for the quality
    for either the muisc func or the verdio fun"""
    options = {}
    l_options = []
    for i in data:
        if type == "audio":
            matches = re.search(
                r"^.* itag=\"(\d+).* mime_type=\"audio/mp4\" abr=\"(\d+).*$",
                f"{i}",
                re.IGNORECASE,
            )
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

    tags = []
    print(f"choose one tag for the desired quality")

    q = "p"
    if type == "audio":
        q = "kbps"

    for i in l_options:
        tags.append(i["itag"])
        print(f"choose {i['itag']} for {i['qu']}{q}")

    itag = input("Tag: ")
    if not itag in tags:
        sys.exit("Invalid choise")
    return itag


# download muisc only
def music():
    # we need to allow the user to choose the folder to store the data in
    try:
        if url := input("URL: ").strip():
            pass
        else:
            sys.exit("invalid url")

        yt = YouTube(url)
        data = yt.streams.filter(only_audio=True)

        # with open("filter.csv", "w") as file:
        #     for line in data:
        #         file.write(f"{line}\n")

        itag = int(option(data, type="audio"))

        stream = yt.streams.get_by_itag(itag)
        stream.download("./music/")
    except:
        # TODO we nedd to parse the exceptions and hundel them individually
        sys.exit("couldn't download this file")

    print("the file has been downloaded sucssfully")


# download  video only
def video():
    # we need to allow the user to choose the folder to store the data in
    try:
        if url := input("URL: ").strip():
            pass
        else:
            sys.exit("Invaild url")

        yt = YouTube(url)

        data = yt.streams.filter(progressive=True)

        # with open("filter.csv", "w") as file:
        #     for line in data:
        #         file.write(f"{line}\n")

        itag = int(option(data, type="video"))

        stream = yt.streams.get_by_itag(itag)
        stream.download("./videos/")

    except:
        # TODO we nedd to parse the exceptions and hundel them individually
        sys.exit("couldn't download this file")

    print("the file has been downloaded sucssfully")


def clm():
    """TODO handel the CLM args get the option [-m|--music] | [-v|--video]
    then return the option"""
    parser = argparse.ArgumentParser(description="download music or video from youtube")
    group = parser.add_mutually_exclusive_group()
    # group.add_argument("url", help="youtube url to download")
    group.add_argument(
        "-m", "--music", action="store_true", help="download file in a muisc formate"
    )
    group.add_argument(
        "-v", "--video", action="store_true", help="download file in a video format"
    )

    args = parser.parse_args()
    option_url = {}
    if args.music:
        option_url["music"] = True
        option_url["video"] = False
    # default format is video if music is not specifed
    else:
        option_url["video"] = True
        option_url["music"] = False
    # print(option_url)
    return option_url


if __name__ == "__main__":
    main()
