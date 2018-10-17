import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv
import os
import regex
from sklearn.preprocessing import scale
from wiset.HMP.data.naver_map import *

os.chdir('./wiset/HMP/data')
print(os.getcwd())
df1 = read_csv('W_주거형태_03.csv', engine='python', encoding='cp949')
df2 = read_csv('W_월세_02.csv', engine='python', encoding='cp949')
df3 = read_csv('W_편의시설_02.csv', engine='python', encoding='cp949')
df4 = read_csv('W_설문결과_01.csv', engine='python', encoding='cp949')

# # 도로명주소 추가
# tmp = read_csv('data/tmp.csv', engine='python', encoding='cp949')
# nn = []
# for loc in tmp.new:
#     if len(str(loc)) > 3:
#         nn.append(loc)
#
# n1, n2 = [], []
# for i in range(len(nn)):
#     if i%2 == 0:
#         n1.append(nn[i])
#     else:
#         n2.append(regex.sub('[^가-힣0-9 -]', '', nn[i]))
#
# df_tmp = DataFrame(data=[n1, n2]).T
# df_tmp.columns = ['주소', '도로명주소']
# len(set(df_tmp.주소))
# df_tmp2 = pd.merge(df1, df_tmp, on='주소')
# # 저장
# df_tmp2.to_csv('data/W_주거형태_02.csv', encoding='cp949', index=False)

# # 거리정보 추가
# df1['xy좌표'], df1['이화여대시간'], df1['연세대시간'], df1['서강대시간'] = '', '', '', ''
# l1, l2, l3 = xyloc('서울 서대문구 이화여대길 52'), xyloc('서울 서대문구 연세로 50'), xyloc('서울 마포구 대흥동 산1-30')
# for i in range(df1.shape[0]):
#     tmp = xyloc(df1.도로명주소[i])
#     df1.xy좌표[i] = tmp
#     df1.이화여대시간[i], df1.연세대시간[i], df1.서강대시간[i] = walkroute(tmp, l1)[1], walkroute(tmp, l2)[1], walkroute(tmp, l3)[1]
#     print(i)
#
# # 저장
# df1.to_csv('data/W_주거형태_03.csv', encoding='cp949', index=False)

df123 = pd.merge(df1, df2, on='ID')
df123 = pd.merge(df123, df3, on='ID')
df_ref = df123[:]


def mf_toFloat0(column_):
    res = [0 if len(regex.sub('[^\d]', '', str(i))) == 0 else float(i) for i in list(column_)]
    return res


def mf_toFloatM(column_):
    m = np.nanmean(list(column_))
    res = [m if len(regex.sub('[^\d]', '', str(i))) == 0 else float(i) for i in list(column_)]
    return res

# Null값 처리
for cName in ['보증금', '월세', '관리비']:
    df_ref[cName] = mf_toFloat0(df_ref[cName])

for cName in ['음식점', '카페', '병원/의료', '은행', '마트/슈퍼', '편의점', '생활/편의', '영화/공연', '스포츠시설', '관공서']:
    df_ref[cName] = mf_toFloatM(df_ref[cName])

# 편의시설점수 : 각 칼럼을 칼럼별로 정규화한 후 ID별 평균값을 산출
# # 정규성 검사
# for column_ in ['음식점', '카페', '병원/의료', '은행', '마트/슈퍼', '편의점', '생활/편의', '영화/공연', '스포츠시설', '관공서']:
#     pval = round(stats.shapiro(df_ref[column_])[1], 10)
#     print(column_, 'p-value:', pval)
scale_all = scale(df_ref[['음식점', '카페', '병원/의료', '은행', '마트/슈퍼', '편의점', '생활/편의', '영화/공연', '스포츠시설', '관공서']], axis=0)
df_ref['편의시설점수'] = np.mean(scale_all, axis=1)

# 원룸 공동시설 5,6번 문항 5점으로 치환
for column_ in ['공동시설5', '공동시설6']:
    df4[column_] = [5 if i == 0 else i for i in df4[column_]]

# 설문결과 ID별 문항별 평균값 산출
df_res = DataFrame()
for id_tmp in set(df4.ID):
    df_tmp = DataFrame(np.mean(df4.loc[df4.ID == id_tmp].iloc[:, 4:22])).T
    # cbind - ID, scores
    df_tmp2 = pd.concat([DataFrame([id_tmp], columns=['ID']).reset_index(drop=True), df_tmp], axis=1)
    # rbind - IDs
    df_res = df_res.append(df_tmp2)

df_res['실내환경설문'] = np.mean(df_res[['실내환경1', '실내환경2', '실내환경3', '실내환경4', '실내환경5', '실내환경6', '실내환경7', '실내환경8']], axis=1)
df_res['실외환경설문'] = np.mean(df_res[['실외환경1', '실외환경2']], axis=1)
df_res['주변편의설문'] = np.mean(df_res[['주변편의시설1', '주변편의시설2']], axis=1)
df_res['공동시설설문'] = np.mean(df_res[['공동시설1', '공동시설2', '공동시설3', '공동시설4', '공동시설5', '공동시설6']], axis=1)

df_ref2 = pd.merge(df_ref, df_res, on='ID')
df_ref2['환산비용'] = df_ref2.보증금 + df_ref2.월세*200 + df_ref2.관리비*200

# # 저장
df_ref2.to_csv('W_중간결과_03.csv', encoding='cp949', index=False)


