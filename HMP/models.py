from django.db import models

import os
from pandas import read_csv
# Create your models here.

# print(os.getcwd())
# df = read_csv('H:/2018/django/wiset/HMP/data/W_중간결과_03.csv', engine='python', encoding='cp949')
df = read_csv('HMP/data/W_result.csv', engine='python', encoding='cp949')
df_stan = df[['ID', '주거형태', '위치', '주소', '이화여대시간', '연세대시간', '서강대시간',
            '보증금', '월세', '관리비', '전용면적', '편의시설점수',
            '실내환경설문', '실외환경설문', '주변편의설문', '공동시설설문', '환산비용']]

df_summary = df[['ID', '주거형태', '보증금', '월세', '이화여대시간', '연세대시간', '서강대시간']]
# df_summary['이화여대시간'] = ['이화여대 ' + str(m) + '분' for m in list(df_summary['이화여대시간'])]
# df_summary['연세대시간'] = ['연세대 ' + str(m) + '분' for m in list(df_summary['연세대시간'])]
# df_summary['서강대시간'] = ['서강대 ' + str(m) + '분' for m in list(df_summary['서강대시간'])]

