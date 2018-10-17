import requests


# start_ = '126.9367577,37.5603216,연세대학교'
# start_ = '126.9502882721,37.5644640671,이화여대길 52'
# desti_ = '126.9466193,37.5617773,이화여자대학교'

def walkroute(start_, desti_):
    if start_.split(',')[0] == desti_.split(',')[0] and start_.split(',')[1] == desti_.split(',')[1]:
        return['0', '0']
    params_ = {'call': 'route2',
               'output': 'json',
               'coord_type': 'naver',
               'search': '0',
               'start': start_,
               'destination': desti_}
    r = requests.get('https://map.naver.com/findroute2/findWalkRoute.nhn',
                     params=params_,
                     headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})
    j = r.json()
    dista = j['result']['summary']['totalDistance']
    ttime = j['result']['summary']['totalTime']
    print(start_, '_', desti_, '\n', dista, 'm_', ttime, '분 is completed...')
    return [dista, ttime]

# walkroute(start_, desti_)
# walkroute('126.9367577,37.5603216,연세대학교', '126.9466193,37.5617773,이화여자대학교')
# walkroute('126.9577,37.5585057,서대문구 북아현동 11-1', '126.9466193,37.5617773,이화여자대학교')

# location_ = '서대문구 북아현동 11-1'
def xyloc(location_):
    address_params = {
        'apikey': '67efd7fa64e0e9fe844041193d18213f7489ca59',
        'q': location_,
        'output': 'json'}

    r = requests.get('http://apis.daum.net/local/geo/addr2coord', params=address_params)
    j = r.json()

    x = str(j['channel']['item'][0]['point_x'])
    y = str(j['channel']['item'][0]['point_y'])

    return(x + ',' + y + ',' + location_)

# xyloc('서대문구 북아현동 11-1')
# xyloc('마포구 신수동 22-2')

# walkroute(xyloc('서대문구 북아현동 11-1'), xyloc('마포구 신수동 22-2'))



