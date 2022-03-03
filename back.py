

import nltk
from nltk import word_tokenize
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
import string
import re
import numpy as np
import pandas as pd

stop = set(stopwords.words('english') + list(string.punctuation))
tr_stop = r'\([^()]*\)'

videos = pd.read_csv('TED_TALK.csv')

import random
import datetime
def random_talk():
	ind = random.randint(0, videos.shape[0])
	talk = videos.iloc[ind]
	ans = tedtalk(
		talk['talk__name'],
		talk['talk__description'],
		str(datetime.timedelta(seconds=int(talk['duration']))),
		talk['url__webpage'],
		talk['url__photo__talk'],
		talk['recording_date'],
		talk['speaker__name'],
		talk['speaker__description'],
		talk['url__photo__speaker'])
	if pd.isnull(talk['recording_date']): ans.date = None
	if pd.isnull(talk['speaker__name']): ans.speaker = None
	if pd.isnull(talk['url__photo__speaker']): ans.speaker_pic = None
	if pd.isnull(talk['speaker__description']): ans.speaker_des = None
	return ans

class tedtalk:
	def __init__(self,na,de,du,li,pi,da,sp,spd,spi):
		self.name = na
		self.description = de
		self.duration = du
		self.link = li
		self.pic = pi
		self.date = da
		self.speaker = sp
		self.speaker_des = spd
		self.speaker_pic = spi


	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name