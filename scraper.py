import requests
import pandas as pd
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
    with open('heroes.json','r') as heroes:
        data = heroes.read()
    from json import loads
    obj = loads(data)
    for h in hero:
        for i in obj:
            for a, v in i.items():
                if a == "localized_name" and v == h:
                    hID = i['id']
                    append = hoes.append
                    append(hID)
    return hoes

##Pro player names and record##
def peeps():
    response = requests.get("http://www.dota2protracker.com/")
    if response.status_code != 200:
        players, played = ([] for _ in range(2))
    else:
        dfs = pd.read_html(response.content, header=0, attrs = {'id': 'table_pro'})[0]
        players , played = dfs.Player.tolist(), dfs.M.tolist()
    return players, played

##Hero names and record##
def heroes():
    response = requests.get("http://www.dota2protracker.com/")
    if response.status_code != 200:
        ids, played = ([] for _ in range(2))
    else:
        dfs = pd.read_html(response.content, header=0, attrs = {'id': 'table_id'})[0]
        ids , played = dfs.Hero.tolist(), dfs.Picks.tolist()
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
        if int(rheader['X-RateLimit-Remaining-Hour']) > 0 and int(rheader['X-RateLimit-Remaining-Minute']) > 0 and int(rheader['X-RateLimit-Remaining-Second']) > 0:
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
    from requests.utils import requote_uri
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

if __name__ == "__main__":
    #tests#
    print(convID(['Centaur Warrunner']))
    #import time
    #start_time = time.process_time()
    #lane()
    #print(hero(["Crit"],"Pangolier","green","Mid",[]))
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


