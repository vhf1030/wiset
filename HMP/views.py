from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.


def home(request):
    datasets = df_summary.set_index('ID').T.to_dict()
    return render(request, "HMP/home.html",
                  {"datasets": datasets})


def detail(request, id_='한우리집'):
    datasets = df_stan.loc[df['ID'] == id_, ].set_index('ID').T.to_dict()

    return render(request, "HMP/detail.html", {"datasets": datasets})


def filter(request):
    form = str(request)[28:len(str(request))-2].split('&')
    option = list(map(lambda s: s[0:2], form))
    form = list(map(lambda s: s[3:], form))
    datasets = df[['ID', '주거형태', '보증금', '월세']]
    if form[4] == 'ih':
        datasets['이동시간'] = df['이화여대시간']
    if form[4] == 'ys':
        datasets['이동시간'] = df['연세대시간']
    if form[4] == 'sg':
        datasets['이동시간'] = df['서강대시간']

    if 'o1' in option:
        datasets['편의시설점수'] = list(map(lambda v: '편의시설점수 : ' + str(v), list(round(df['편의시설점수'], 2))))
    if 'o2' in option:
        datasets['실내환경설문'] = list(map(lambda v: '실내환경설문 : ' + str(v), list(round(df['실내환경설문'], 2))))
    if 'o3' in option:
        datasets['실외환경설문'] = list(map(lambda v: '실외환경설문 : ' + str(v), list(round(df['실외환경설문'], 2))))
    if 'o4' in option:
        datasets['주변편의설문'] = list(map(lambda v: '주변편의설문 : ' + str(v), list(round(df['주변편의설문'], 2))))
    if 'o5' in option:
        datasets['공동시설설문'] = list(map(lambda v: '공동시설설문 : ' + str(v), list(round(df['공동시설설문'], 2))))
    if 'o6' in option:
        datasets['환산비용'] = list(map(lambda v: '환산비용 : ' + str(v) + '만원', list(df['환산비용'])))
    datasets = datasets.loc[datasets['보증금'] >= int(form[0]), ]
    datasets = datasets.loc[datasets['보증금'] <= int(form[1]), ]
    datasets = datasets.loc[datasets['월세'] >= int(form[2]), ]
    datasets = datasets.loc[datasets['월세'] <= int(form[3]), ]
    datasets = datasets.loc[datasets['이동시간'] >= int(form[5]), ]
    datasets = datasets.loc[datasets['이동시간'] <= int(form[6]), ]
    datasets['보증금'] = list(map(lambda v: '보증금 : ' + str(v) + '만원', list(datasets['보증금'])))
    datasets['월세'] = list(map(lambda v: '월세 : ' + str(v) + '만원', list(datasets['월세'])))
    datasets['이동시간'] = list(map(lambda v: '이동시간 : ' + str(v) + '분', list(datasets['이동시간'])))
    datasets = datasets.set_index('ID').T.to_dict()

    columns = ['편의시설점수', '실내환경설문', '실외환경설문', '주변편의설문', '공동시설설문', '환산비용', '이동시간']
    # columns = ['a', 'b']

    return render(request, "HMP/filter.html",
                  {"datasets": datasets,
                   "form": form,
                   "r1": form[0], "r2": form[1],
                   "r3": form[2], "r4": form[3],
                   "r5": form[5], "r6": form[6],
                   "columns": columns})

def datasort(request, string_='환산비용'):
    form = str(request)[28:len(str(request)) - 2].split('&')
    form = list(map(lambda s: s[3:], form))
    datasets = df[['ID', '주거형태', '보증금', '월세']]
    if form[4] == 'ih':
        datasets['이동시간'] = df['이화여대시간']
    if form[4] == 'ys':
        datasets['이동시간'] = df['연세대시간']
    if form[4] == 'sg':
        datasets['이동시간'] = df['서강대시간']

    by_ = str(string_)
    ascend_ = False
    if by_ == '환산비용' or '이동시간':
        ascend_ = True
    datasets[by_] = df_stan[by_]

    datasets = datasets.loc[datasets['보증금'] >= int(form[0]),]
    datasets = datasets.loc[datasets['보증금'] <= int(form[1]),]
    datasets = datasets.loc[datasets['월세'] >= int(form[2]),]
    datasets = datasets.loc[datasets['월세'] <= int(form[3]),]
    datasets = datasets.loc[datasets['이동시간'] >= int(form[5]),]
    datasets = datasets.loc[datasets['이동시간'] <= int(form[6]),]
    datasets = datasets.set_index('ID').T.to_dict()

    columns = ['편의시설점수', '실내환경설문', '실외환경설문', '주변편의설문', '공동시설설문', '환산비용', '이동시간']

    datasets = datasets.sort_values(by=[by_], ascending=ascend_).set_index('ID').T.to_dict()

    return render(request, "HMP/filter.html",
                  {"datasets": datasets,
                   "form": form,
                   "r1": form[0], "r2": form[1],
                   "r3": form[2], "r4": form[3],
                   "r5": form[5], "r6": form[6],
                   "columns": columns})