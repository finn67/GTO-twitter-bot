import os, cv2, datetime, random, tweepy, re

directory = os.path.normpath('C:/GoldenBoy')

def VideoSelect():

    VideoSelectVar = random.choice(os.listdir(directory))  # change dir name to whatever
    return VideoSelectVar

def Screenshot(randomseconds, VideoPath,time):
    randomseconds = randomseconds * 1000
    time = str(time)

    vidcap = cv2.VideoCapture(VideoPath)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, randomseconds)  # just cue to 20 sec. position
    success, image = vidcap.read()
    if success:
        cv2.imwrite("frame.png", image)  # save frame as JPEG file
        cv2.imshow(time, image)




def LengthOfVideo(VideoSelectVar):

    VideoSelectVar2 = VideoSelectVar

    VideoSelectVar = directory + "/" + VideoSelectVar
    print(VideoSelectVar)
    data = cv2.VideoCapture(VideoSelectVar)
    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f"duration in seconds: {seconds}")
    print(f"video time: {video_time}")
    return seconds,video_time,VideoSelectVar2,VideoSelectVar

def randomtime(seconds):
    seconds = seconds
    #Random time between ranges
    start = datetime.timedelta(hours=0, minutes=0, seconds=0)
    end = datetime.timedelta(hours=0, minutes=0, seconds=seconds)

    random_seconds = random.randint(start.total_seconds(), end.total_seconds())
    random_time = datetime.timedelta(seconds=random_seconds)
    return random_seconds

def Twitter(videotime,Videoselectvar2,seconds):
    auth = tweepy.OAuthHandler("", "")
    auth.set_access_token("", "")
    api = tweepy.API(auth)

    TimeOfSc = str(datetime.timedelta(seconds=seconds))
    rep = {"[Reaktor] GTO - ": "", "[576p][x265][10-bit].mkv": ""}  # define desired replacements here

    # use these three lines to do the replacement
    #https://stackoverflow.com/a/6117124
    rep = dict((re.escape(k), v) for k, v in rep.items())
    # Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], Videoselectvar2)
    print(text)
    print(TimeOfSc)
    media = api.media_upload("frame.jpg")

    # Post tweet with image

    tweet = text + "" + "|" + "" + TimeOfSc

    post_result = api.update_status(status=tweet, media_ids=[media.media_id])

if __name__ == '__main__':
    t = VideoSelect()
    seconds, videotime,Videoselectvar2,Videoselectvar = LengthOfVideo(t)
    y = randomtime(seconds)
    print(y)
    Screenshot(y,Videoselectvar,videotime)
    Twitter(videotime,Videoselectvar2, y)

