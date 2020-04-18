from datetime import datetime
import requests
from requests import exceptions
import pandas as pd
from json import loads
from requests.utils import requote_uri
#from selenium import webdriver

def pagereq(url):
    response = requests.get(url)
    from bs4 import BeautifulSoup, SoupStrainer
    strainer = SoupStrainer('table')
    soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
    return soup ,response.status_code

def convID(hero):
    #checks if parameter is a string so the "for h in hero" statement works
    if not isinstance(hero, list):
        hero = [hero]
    hoes = []
    with open('heroes.json','r') as heroids:
        data = heroids.read()
    obj = loads(data)
    for h in hero:
        for i in obj:
            for a, v in i.items():
                if a == "localized_name" and v == h:
                    hID = i['id']
                    append = hoes.append
                    append(hID)
    return hoes
def conv2ID(hID):
    hero = 'N/A'
    with open('heroes.json', 'r') as heroids:
        data = heroids.read()
    obj = loads(data)
    for i in obj:
        for a, v in i.items():
            if a == "id" and v == hID:
                hero = i["localized_name"]
    return hero


##Pro player names and record##
def peeps():
    try:
        response = requests.get("http://www.dota2protracker.com/", timeout=4)
        dfs = pd.read_html(response.content, header=0, attrs = {'id': 'table_pro'})[0]
        players , played = dfs.Player.tolist(), dfs.M.tolist()
    except (exceptions.ConnectionError, exceptions.Timeout,
                exceptions.HTTPError, exceptions.RequestException) as e:
            players, played = ([] for _ in range(2))
    return players, played

##Hero names and record##
def heroes():
    try:
        response = requests.get("http://www.dota2protracker.com/", timeout=4)
        dfs = pd.read_html(response.content, header=0, attrs = {'id': 'table_id'})[0]
        ids , played = dfs.Hero.tolist(), dfs.Picks.tolist()
    except (exceptions.ConnectionError, exceptions.Timeout,
                exceptions.HTTPError, exceptions.RequestException) as e:
        ids, played = ([] for _ in range(2))
    return ids, played


# ##checks the laning tab in opendota
# def lane_old():
#     #checks whether the match has been parsed by opendota using a seperate function to...
#     #...verify if div that holds "needs parsing" message exists.
#     #hero name is stored in attribute data-for in the img tag
#     #lane is in the same tr between span tags where hero name was found
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     with webdriver.Chrome(executable_path="/Users/#/Documents/driver/chromedriver.exe", chrome_options=chrome_options) as driver:
#         driver.get("https://www.opendota.com/matches/5340488516/laning")
#         if driver.find_elements_by_css_selector('table'):
#             strainer = SoupStrainer('table')
#             soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)
#             return soup.prettify()
#         else:
#             return False
#

#Lane check
def lane(mID, hID,role, matchup):
    # flag is used to track if match was found and limited is used to check if API requests fails
    limited, flag = False, False
    if role == "Mid":
        laneno , xlane = 2, 0#mid and nolane
    if role == "Off":
        laneno, xlane = 3 , 1#offlane and safe lane
    if role == "Safe":
        laneno ,xlane = 1 ,3#safe lane and offlane
    response = requests.get(f"https://api.stratz.com/api/v1/match/{mID}/breakdown")
    rheader = response.headers
    if response.status_code == 200:
        if int(rheader['x-ratelimit-remaining-hour']) > 0 and int(rheader['x-ratelimit-limit-minute']) > 0 and int(rheader['x-ratelimit-limit-second']) > 0:
            data = response.json()['players']
            if 'lane' in data[0]:
                for i in range(0,10):
                    if data[i]['heroId'] in hID and data[i]['lane'] == laneno:
                        if not matchup:
                            flag = True
                        elif matchup:
                            h2ID = convID(matchup)
                            if laneno == 2:
                                for j in range(0,10):
                                    if data[j]['heroId'] in h2ID and data[j]['lane'] == laneno:
                                        flag = True
                            elif xlane:
                                side = data[i]['isRadiant']
                                for k in range(0,10):
                                    if data[k]['heroId'] in h2ID and data[k]['lane'] == xlane and data[k]['isRadiant'] != side:
                                        flag = True

        else:
            limited = True
    else:
        limited = True
    return flag, limited
    
##Specific Hero##
def hero(player, hero,outcome, role, matchup):
    hID = convID(hero)
    limited = False
    soup, status = pagereq(f"http://www.dota2protracker.com/hero/{requote_uri(hero)}")
    match_ids,avg_mmr, match_time, loutcome,pro_names = ([] for _ in range(5))
    if status == 200:
        table = soup.find(id="table_matches")
        rows = table.findAll('tr')
        for row in rows[1:]:
            if limited:
                break
            tds = (row.findAll('td'))
            l = tds[1].find("a")
            for i in player:
                if l.attrs['href'] == f"/player/{i}" and row.find("img", class_=f"{outcome}"):
                    links = row.find("a", class_="info")
                    mID = ''.join(filter(str.isdigit, links.attrs['href']))
                    flag = True
                    if not role == "Any":
                        flag , limited = lane(mID,hID,role, matchup)
                    if flag == True and limited == False:
                        if not len(player) == 1:
                            pro_names.append(i)
                        else:
                            pro_names.append("0")
                        match_time.append(tds[7].text)
                        avg_mmr.append(tds[4].text)
                        match_ids.append(mID)
                        if outcome == "green":
                            loutcome.append("win")
                        else:
                            loutcome.append("loss")
                        
    #order of matches in list is new to old       
    return match_ids[::-1],avg_mmr[::-1], match_time[::-1], loutcome[::-1], pro_names[::-1], limited


#Limits player list based on hero chosen
def plimiter(hero):
    try:
        response = requests.get(f"http://www.dota2protracker.com/hero/{requote_uri(hero)}", timeout=4)
        dfs = pd.read_html(response.content, header=0, attrs = {'id': 'table_matches'})[0]
        dfs.rename(columns={ dfs.columns[1]: "Name" }, inplace=True)
        noplist = dfs['Name'].tolist()
        plist = []
        for i in noplist:
            if 'won' in i:
                p = i.partition("won")[0]
                plist.append(p.strip())
            if 'lost' in i:
                p = i.partition("lost")[0]
                plist.append(p.strip())
        counter = [[x,plist.count(x)] for x in set(plist)]
    except (exceptions.ConnectionError, exceptions.Timeout,
            exceptions.HTTPError, exceptions.RequestException) as e:
        counter = []
    return counter


def convRegion(rID):
    rname = "?"
    with open('regions.json','r') as r:
        data = r.read()
    obj = loads(data)
    for i in obj:
        for a, v in i.items():
            if a == "id" and v == rID:
                rname = i['name']
    return rname

def convLane(lID):
    lane = "?"
    if lID == 1:
        lane = "Safe lane"
    elif lID == 2:
        lane = "Mid lane"
    elif lID == 3 or lID == 4:
        lane = "Offlane"
    elif lID == 5:
        lane = "Offlane and Safe lane"
    elif lID == 6:
        lane = "all lanes"
    elif lID == 0:
        lane = "Jungle"
    return lane

def parser(mID):
    parsed = False
    stats = {
        'winner': 'dire',
        'duration': 0,
        'region': '',
        'endtime': 'DD/MM/YYYY HH:MM:SS',
        'goodscore': 0,
        'badscore': 0,
        'players':{
            0:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm': 0,
                'xpm': 0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False


            },
            1:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm': 0,
                'xpm': 0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            2:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            3:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            4:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            5:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            6:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            7:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            8:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            },
            9:{
                'id': -1,
                'hero':'',
                'name':'',
                'gpm':0,
                'xpm':0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'cs10': -1,
                'networth': 0,
                'lane': -1,
                'roaming': False,
                'pro': False

            }
        }
    }
    response = requests.get(f"https://api.stratz.com/api/v1/match/{mID}/breakdown")
    rheader = response.headers
    if response.status_code == 200:
        if int(rheader['x-ratelimit-remaining-hour']) > 0 and int(rheader['x-ratelimit-limit-minute']) > 0 and int(rheader['x-ratelimit-limit-second']) > 0:
            parsed = True
            data = response.json()
            if data['didRadiantWin'] == True:
                stats['winner'] = 'radiant'
            seconds = data['durationSeconds']
            stats['duration'] = '{0:02d}:{1:02d}'.format(*divmod(seconds, 60))
            stats['region'] = convRegion(data['regionId'])
            ts = int(data['endDateTime'])
            ftime = datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
            stats['endtime'] = ftime
            goodscore = 0
            for i in range(5):
                goodscore+= data['players'][i]['numKills']
                stats['players'][i]['id'] = data['players'][i]['heroId']
                stats['players'][i]['hero'] = conv2ID(data['players'][i]['heroId'])
                stats['players'][i]['name'] = data['players'][i]['steamAccount']['name']
                if 'proSteamAccount' in data['players'][i]['steamAccount']:
                    stats['players'][i]['name'] = data['players'][i]['steamAccount']['proSteamAccount']['name']
                    stats['players'][i]['pro'] = True
                stats['players'][i]['gpm'] = data['players'][i]['goldPerMinute']
                stats['players'][i]['xpm'] = data['players'][i]['experiencePerMinute']
                stats['players'][i]['kills'] = data['players'][i]['numKills']
                stats['players'][i]['deaths'] = data['players'][i]['numDeaths']
                stats['players'][i]['assists'] = data['players'][i]['numAssists']
                stats['players'][i]['networth'] = data['players'][i]['networth']
                if 'lane' in data['players'][i]:
                    stats['players'][i]['lane'] = convLane(data['players'][i]['lane'])
                    if data['players'][i]['lane'] == 0:
                        rlane = data['players'][i]['roamLane']
                        ##manually setting the lane since there is a value overlap
                        if rlane == 3:
                            stats['players'][i]['lane'] = "Safe and Mid lane"
                        else:
                            stats['players'][i]['lane'] = convLane(rlane)
                        stats['players'][i]['roaming'] = True
                if 'stats' in data['players'][i] and data['durationSeconds'] >= 660:
                    cscount = 0
                    for m in range(10):
                        cscount+= data['players'][i]['stats']['lastHitPerMinute'][m]
                    stats['players'][i]['cs10']= cscount
            stats['goodscore'] = goodscore
            badscore = 0
            for j in range(5, 10):
                badscore+= data['players'][j]['numKills']
                stats['players'][j]['id'] = data['players'][j]['heroId']
                stats['players'][j]['hero'] = conv2ID(data['players'][j]['heroId'])
                stats['players'][j]['name'] = data['players'][j]['steamAccount']['name']
                if 'proSteamAccount' in data['players'][j]['steamAccount']:
                    stats['players'][j]['name'] = data['players'][j]['steamAccount']['proSteamAccount']['name']
                    stats['players'][j]['pro'] = True
                stats['players'][j]['gpm'] = data['players'][j]['goldPerMinute']
                stats['players'][j]['xpm'] = data['players'][j]['experiencePerMinute']
                stats['players'][j]['kills'] = data['players'][j]['numKills']
                stats['players'][j]['deaths'] = data['players'][j]['numDeaths']
                stats['players'][j]['assists'] = data['players'][j]['numAssists']
                stats['players'][j]['networth'] = data['players'][j]['networth']
                if 'lane' in data['players'][j]:
                    stats['players'][j]['lane'] = convLane(data['players'][j]['lane'])
                    if data['players'][j]['lane'] == 0:
                        rlane = data['players'][j]['roamLane']
                        ##manually setting the lane since there is a value overlap
                        if rlane == 3:
                            stats['players'][j]['lane'] = "Safe and Mid lane"
                        else:
                            stats['players'][j]['lane'] = convLane(rlane)
                        stats['players'][j]['roaming'] = True
                if 'stats' in data['players'][j] and data['durationSeconds'] >= 660:
                    cscount = 0
                    for k in range(10):
                        cscount+= data['players'][j]['stats']['lastHitPerMinute'][k]
                    stats['players'][j]['cs10']= cscount
            stats['badscore'] = badscore
    return stats, parsed

if __name__ == "__main__":
    #tests#
    #print(heroes())
    #print(plimiter("Pangolier"))
    stats , parsed = parser(5350537124)
    print(stats)
    #print(convID(['Centaur Warrunner']))
    #import time
    #start_time = time.process_time()
    #lane()
    #print(hero(["Gorgc"],"Nature's Prophet","green","Any",[]))
    #print(hero(["Gorgc"],"Nature's Prophet","red","Any",[]))
    #print(hero(["Crit"], "Pangolier", "red", "Mid", []))
    #print("--- %s seconds ---" % round(time.process_time() - start_time, 10))
    #list_b = lowl()
    #print(len(list_b))
    #merged = list(zip(list_a, list_b))
    #merged = sorted(merged)hh
    #for i in merged:
    #    print(i[0])
    #A, B, C, D , E= hero("Taiga","Mars","green")
    #E, F, G, H = hero("Taiga","Mars","red")
    #times = C + G
    #print(times)
    #secs = 0
    #for i in times:
    #    m, s = i.split(':')
    #    secs += (int(m)*60) + int(s)
    #print(secs)
    #avg = secs/len(times)
    #print(avg)
    #res1 = {key: {'outcome': wol, 'duration': dur, 'avgmmr': mmr} for key, mmr, dur, wol in zip(A, B, C, D)}
    #res2 = {key: {'outcome': wol, 'duration': dur, 'avgmmr': mmr} for key, mmr, dur, wol in zip(E, F, G, H)}
    #allmatches = {**res1, **res2}


