

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

import copy

def idf_calc(doc):
    total_words = set()
    for each in doc:
        total_words.update(each)    
# calculated once for everything
    idf_score = {} #run for every doc; 
    for each_word in total_words:
        word_count = 0
        for every in doc:
            if each_word in every:
                word_count = word_count +1
        idf_score[each_word] = (math.log(int(len(doc))/word_count)) 
    all_tf_idf = []
    tf_score = copy.deepcopy(idf_score)
    for each in doc:
        tf_score = {x: 0 for x in tf_score}
        for each_word in each:
            tf_score[each_word] += 1
        tf_idf = {x: tf_score[x]*idf_score[x] for x in tf_score}
        all_tf_idf.append(tf_idf)
    return (idf_score, all_tf_idf)
def query_similarity(query,idf_score,all_tf_idf): 
    
    words = query.split()
    toal_words = set(words)
    query_tf = copy.deepcopy(idf_score)
    query_tf = {x: 0 for x in query_tf}
    for each_word in words:
        query_tf[each_word] += 1
    Q_tf_idf = {x: query_tf[x]*idf_score[x] for x in query_tf}
    similarity=[]
    for each in all_tf_idf:
        cosine_similarity= 1- spatial.distance.cosine(list(Q_tf_idf.values()),list(each.values()))
        similarity.append(cosine_similarity)

    return(similarity)


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
