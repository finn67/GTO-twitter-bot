import boto3
import cv2
import uuid
import random
import datetime
import tweepy
import re
import base64

s3 = boto3.client('s3')
bucket = "your bucket"


def randomtime(seconds):
	start = datetime.timedelta(hours=0, minutes=0, seconds=0)

	end = datetime.timedelta(hours=0, minutes=0, seconds=seconds)

	random_seconds = random.randint(start.total_seconds(), end.total_seconds())
	random_time = datetime.timedelta(seconds=random_seconds)
	return random_seconds


def VideoSelect():
	response = s3.list_objects_v2(
		Bucket=bucket,
		Prefix="[Reaktor] GTO - Great Teacher Onizuka Complete [576p][x265][10-bit]/"
	)
	mykeys = []
	for content in response.get('Contents', []):
		print(content['Key'])
		mykeys.append(content['Key'])

	random_key = random.choice(mykeys)
	mykeys.remove(random_key)
	return random_key


def LengthOfVideo(key):
	url = s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': bucket, 'Key': key})
	data = cv2.VideoCapture(url)
	frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
	fps = data.get(cv2.CAP_PROP_FPS)
	seconds = round(frames / fps)
	video_time = datetime.timedelta(seconds=seconds)
	print(f"duration in seconds: {seconds}")
	print(f"video time: {video_time}")
	return seconds, video_time, url


def Screenshot(random_seconds, url, video_time, key):
	random_seconds = random_seconds * 1000
	video_time = str(video_time)

	vidcap = cv2.VideoCapture(url)
	vidcap.set(cv2.CAP_PROP_POS_MSEC, random_seconds)
	success, image = vidcap.read()
	if success:
		cv2.imwrite("/tmp/frame.png", image)  # save frame as JPEG file
		s3.put_object(Bucket=bucket, Key="frame.png", Body=open("/tmp/frame.png", "rb").read())


def twitter(video_time, key, random_seconds):
	key123 = "frame.png"
	auth = tweepy.OAuthHandler("", "")
	auth.set_access_token("",
						  "")
	api = tweepy.API(auth)
	TimeOfSc = str(datetime.timedelta(seconds=random_seconds))
	#https://stackoverflow.com/a/6117124
	rep = {"[Reaktor] GTO - Great Teacher Onizuka Complete [576p][x265][10-bit]/[Reaktor] GTO - ": "",
		   "[576p][x265][10-bit].mkv": ""}
	rep = dict((re.escape(k), v) for k, v in rep.items())
	pattern = re.compile("|".join(rep.keys()))
	text = pattern.sub(lambda m: rep[re.escape(m.group(0))], key)
	print(text)
	print(TimeOfSc)
	s3.download_file(bucket, key123, '/tmp/test.png')
	##url = s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': bucket, 'Key': key123})
	media = api.media_upload('/tmp/test.png')
	tweet = text + "" + "|" + " " + TimeOfSc

	post_result = api.update_status(status=tweet, media_ids=[media.media_id])


def lambda_handler(event, context):
	key = VideoSelect()
	print(key)
	seconds, video_time, url = LengthOfVideo(key)
	random_seconds = randomtime(seconds)
	Screenshot(random_seconds, url, video_time, key)
	twitter(video_time, key, random_seconds)


