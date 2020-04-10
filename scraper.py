import requests
from requests.utils import requote_uri
from bs4 import BeautifulSoup, SoupStrainer

def pagereq(extra):
    response = requests.get(f"http://www.dota2protracker.com/{requote_uri(extra)}")
    strainer = SoupStrainer('table')
    soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
    return soup ,response.status_code


##Pro player names##
def peeps():
    soup,status = pagereq("")
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
    soup,status = pagereq("")
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
    soup,status = pagereq("")
    played = []
    table_id = soup.find(id="table_pro")
    rows = table_id.findAll('tr')
    second_columns = []
    for row in rows[1:]:
        second_columns.append(row.findAll('td')[1].text)
    return second_columns
##Amount each hero is played##
def spam():
    soup,status = pagereq("")
    played = []
    table_id = soup.find(id="table_id")
    rows = table_id.findAll('tr')
    third_columns = []
    for row in rows[1:]:
        third_columns.append(row.findAll('td')[2].text)
    return third_columns

##checks the laning tab in opendota
def lane(hero):
    #checks whether the match has been parsed by opendota using a seperate function to...
    #...verify if div that holds "needs parsing" message exists.
    #hero name is stored in attribute data-for in the img tag
    #lane is in the same tr between span tags where hero name was found
    pass
    
##Specific Hero##
def hero(player, hero,outcome):
    soup, status = pagereq(f"hero/{hero}")
    match_ids,avg_mmr, match_time, loutcome = ([] for _ in range(4))
    if status == 200:
        table = soup.find(id="table_matches")
        rows = table.findAll('tr')
        for row in rows[1:]:
            tds = (row.findAll('td'))
            l = tds[1].find("a")
            if l.attrs['href'] == f"/player/{player}" and row.find("img", class_=f"{outcome}"):
                match_time.append(tds[7].text)
                avg_mmr.append(tds[4].text)
                links = row.find("a", class_="info")
                match_ids.append(''.join(filter(str.isdigit, links.attrs['href'])))
                if outcome == "green":
                    loutcome.append("win")
                else:
                    loutcome.append("loss")
    #order of matches in list is new to old       
    return match_ids[::-1],avg_mmr[::-1], match_time[::-1], loutcome[::-1]

if __name__ == "__main__":
    #tests#
    import time
    start_time = time.process_time()
    print(hero("QO","Phantom Lancer","green"))
    print("--- %s seconds ---" % round(time.process_time() - start_time, 10))
    #list_b = lowl()
    #print(len(list_b))
    #print(list_b)
    #merged = list(zip(list_a, list_b))
    #merged = sorted(merged)
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


