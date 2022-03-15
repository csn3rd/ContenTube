import copy
import nltk
from nltk import word_tokenize
import ssl
import math
from collections import Counter
from scipy import spatial

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

tr_stop = r'\([^()]*\)'
punctuation = r'[^ a-zA-Z0-9]'
stop = r'\b%s\b' % r'\b|\b'.join(map(re.escape, set(stopwords.words('english'))))
extra_spaces = r'\s\s+'

def sanitize(obj):
	st = str(obj)
	# not speaker
	clean1 = re.sub(tr_stop, ' ', st)

	# lower case
	clean2 = clean1.lower()

	# remove punctuation
	filter1 = re.compile(punctuation)
	clean2 = filter1.sub(' ', clean2)

	# remove stop words
	filter2 = re.compile(stop)
	clean3 = filter2.sub(' ', clean2)

	# remove extra spaces
	clean4 = re.sub(extra_spaces, ' ', clean3)

	san = list(clean4.split(" "))
	return san

videos = pd.read_csv('TED_TALK.csv').head(500)
videos['transcript'] = videos['transcript'].apply(sanitize)

import datetime
def get_talk(ind):
	# print("getting talk:",ind)
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

def idf_calc(doc):
	total_words = set()
	for each in doc:
		total_words.update(each)    
	print("found all words", len(total_words))

	# calculated once for everything
	doc_freq = {x: 0 for x in total_words} #run for every doc; 
	for each in doc:
		words = set(each)
		for each_word in words:
			doc_freq[each_word] += 1
	idf_score = {x: (math.log(int(len(doc))/doc_freq[x])) for x in total_words}
	print("computed idf scores")

	all_tf_idf = []
	for each in doc:
		words = set(each)
		tf_score = Counter(each)
		tf_idf = {x: tf_score[x]*idf_score[x] for x in total_words}
		# all_tf_idf += [tf_idf]      # 0:02:52.818922
		all_tf_idf.append(tf_idf)      # 0:02:46.379710
	print("computed tf-idf scores")
	return (idf_score, all_tf_idf)

idfs, tf_idfs = idf_calc(list(videos['transcript']))

def query_similarity(words,idf_score,all_tf_idf):
	toal_words = set(words)
	query_tf = copy.deepcopy(idf_score)
	query_tf = {x: 0 for x in query_tf}
	for each_word in words:
		if each_word in query_tf:
			query_tf[each_word] += 1
	Q_tf_idf = {x: query_tf[x]*idf_score[x] for x in query_tf}
	similarity=[]
	for each in all_tf_idf:
		cosine_similarity = 1 - spatial.distance.cosine(list(Q_tf_idf.values()),list(each.values()))
		similarity.append(cosine_similarity)
	return similarity

def search(srch, typ):
	start = datetime.datetime.now()
	srch = sanitize(srch)
	sims = query_similarity(srch, idfs, tf_idfs)
	best_ind = sorted(range(0,len(sims)), key=lambda k: sims[k])
	best = []
	i = 1
	while i < len(10) and sims[best_ind[-i]] > 0.02:
		best += [get_talk(best_ind[-i])]
		print(best[i-1].name, sims[best_ind[-i]])
		i+=1
	timetaken = (datetime.datetime.now()-start).total_seconds()
	return (best, timetaken)

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
