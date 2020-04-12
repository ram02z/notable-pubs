import requests
from requests.utils import requote_uri
from bs4 import BeautifulSoup, SoupStrainer
import json
#from selenium import webdriver

def pagereq(url):
    response = requests.get(url)
    strainer = SoupStrainer('table')
    soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
    return soup ,response.status_code

def convID(hero):
    with open('heroes.json','r') as heroes:
        data = heroes.read()
    obj = json.loads(data)
    for i in obj:
        for a, v in i.items():
            if a == "localized_name" and v == hero:
                return(i['id'])

##Pro player names##
def peeps():
    soup,status = pagereq("http://www.dota2protracker.com/")
    players = []
    if status == 200:
        table_pro = soup.find(id="table_pro")
        rows = table_pro.findAll('tr')
        for row in rows[1:]:
            td = (row.findAll('td')[0])
            l = td.find("a")
            players.append(l.attrs['title'])
    return players

##Hero names##
def heroes():
    soup,status = pagereq("http://www.dota2protracker.com/")
    ids = []
    if status == 200:
        table_id = soup.find(id="table_id")
        rows = table_id.findAll('tr')
        for row in rows[1:]:
            td = (row.findAll('td')[1])
            l = td.find("a")
            ids.append(l.attrs['title'])
    return ids

##Player match record##
def lowl():
    soup,status = pagereq("http://www.dota2protracker.com/")
    played = []
    table_id = soup.find(id="table_pro")
    rows = table_id.findAll('tr')
    second_columns = []
    for row in rows[1:]:
        second_columns.append(row.findAll('td')[1].text)
    return second_columns
##Amount each hero is played##
def spam():
    soup,status = pagereq("http://www.dota2protracker.com/")
    played = []
    table_id = soup.find(id="table_id")
    rows = table_id.findAll('tr')
    third_columns = []
    for row in rows[1:]:
        third_columns.append(row.findAll('td')[2].text)
    return third_columns

# ##checks the laning tab in opendota
# def lane_old():
#     #checks whether the match has been parsed by opendota using a seperate function to...
#     #...verify if div that holds "needs parsing" message exists.
#     #hero name is stored in attribute data-for in the img tag
#     #lane is in the same tr between span tags where hero name was found
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     with webdriver.Chrome(executable_path="/Users/Omar/Documents/driver/chromedriver.exe", chrome_options=chrome_options) as driver:
#         driver.get("https://www.opendota.com/matches/5340488516/laning")
#         if driver.find_elements_by_css_selector('table'):
#             strainer = SoupStrainer('table')
#             soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)
#             return soup.prettify()
#         else:
#             return False
#
#Lane check
def lane():
    limited = False
    response = requests.get("https://api.stratz.com/api/v1/match/5348683592/breakdown")
    rheader = response.headers
    if response.status_code == 200:
        if int(rheader['X-RateLimit-Remaining-Hour']) > 0 and int(rheader['X-RateLimit-Remaining-Minute']) > 0 and int(rheader['X-RateLimit-Remaining-Second']) > 0:
            data = response.json()['players']
            for i in range(0,9):
                if data[i]['heroId'] == 90:
                    print(i)
        else:
            limited = True
    else:
        limited = True
    
##Specific Hero##
def hero(player, hero,outcome):
    soup, status = pagereq(f"http://www.dota2protracker.com/hero/{requote_uri(hero)}")
    match_ids,avg_mmr, match_time, loutcome,pro_names = ([] for _ in range(5))
    if status == 200:
        table = soup.find(id="table_matches")
        rows = table.findAll('tr')
        for row in rows[1:]:
            tds = (row.findAll('td'))
            l = tds[1].find("a")
            for i in player:
                if l.attrs['href'] == f"/player/{i}" and row.find("img", class_=f"{outcome}"):
                    if not len(player) == 1:
                        pro_names.append(i)
                    else:
                        pro_names.append("0")
                    match_time.append(tds[7].text)
                    avg_mmr.append(tds[4].text)
                    links = row.find("a", class_="info")
                    match_ids.append(''.join(filter(str.isdigit, links.attrs['href'])))
                    if outcome == "green":
                        loutcome.append("win")
                    else:
                        loutcome.append("loss")
                        
    #order of matches in list is new to old       
    return match_ids[::-1],avg_mmr[::-1], match_time[::-1], loutcome[::-1], pro_names[::-1]

if __name__ == "__main__":
    #tests#
    print(convID("Monkey King"))
    #import time
    #start_time = time.process_time()
    #lane()
    #print(hero(["Kuku"],"Mars","green"))
    #print("--- %s seconds ---" % round(time.process_time() - start_time, 10))
    #list_b = lowl()
    #print(len(list_b))
    #print(list_b)
    #merged = list(zip(list_a, list_b))
    #merged = sorted(merged)hh
    #for i in merged:
    #    print(i[0])
    #A, B, C, D = hero("Taiga","Mars","green")
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


