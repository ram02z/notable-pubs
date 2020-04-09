from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def pagereq(extra):
    try:
        with urlopen(f"http://www.dota2protracker.com/{quote(extra)}") as response:
            soup = BeautifulSoup(response, 'lxml')
        return soup
    except HTTPError as e:
        return str(e)
    except URLError as e:
        return str(e)
        

##Pro player names##
def peeps():
    soup = pagereq("")
    players = []
    if "<urlopen error" not in soup:
        table_pro = soup.find(id="table_pro")
        tbody = table_pro.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            for td in tds:
                l= td.find("a")
                if l is not None:
                    players.append(l.attrs['title'])
    return players

##Hero names##
def heroes():
    soup = pagereq("")
    ids = []
    if "<urlopen error" not in soup:
        table_id = soup.find(id="table_id")
        tbody = table_id.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            for td in tds:
                l= td.find("a")
                if l is not None:
                    ids.append(l.attrs['title'])
        ids = [i for n, i in enumerate(ids) if i not in ids[:n]] 
    return ids
##Player match record##
def lowl():
    soup = pagereq("")
    played = []
    table_id = soup.find(id="table_pro")
    rows = table_id.findAll('tr')
    second_columns = []
    for row in rows[1:]:
        second_columns.append(row.findAll('td')[1].text)
    return second_columns
##Amount each hero is played##
def spam():
    soup = pagereq("")
    played = []
    table_id = soup.find(id="table_id")
    rows = table_id.findAll('tr')
    third_columns = []
    for row in rows[1:]:
        third_columns.append(row.findAll('td')[2].text)
    return third_columns
    
##Specific Hero##
def hero(player, hero,outcome):
    soup = pagereq(f"hero/{hero}")
    match_ids,avg_mmr, match_time, loutcome = ([] for _ in range(4))
    if "<urlopen error" not in soup:
        table_matches = soup.find(id="table_matches")
        tbody = table_matches.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            for td in tds:
                l= td.find("a")
                if l is not None:
                    if l.attrs['href'] == f"/player/{player}" and tr.find("img", class_=f"{outcome}"):
                        data = tr.find_all("td", { "class":"dt-body-center" })
                        numbers = [d.text for d in data]
                        for i in numbers:
                            if ":" in i:
                                match_time.append(i)
                        avg_mmr.append(max(numbers))
                        links = tr.find("a", class_="info")
                        match_ids.append(''.join(filter(str.isdigit, links.attrs['href'])))
                        if outcome == "green":
                            loutcome.append("win")
                        else:
                            loutcome.append("loss")
    #order of matches in list is new to old       
    return match_ids[::-1],avg_mmr[::-1], match_time[::-1], loutcome[::-1]

if __name__ == "__main__":
    #tests#
    list_a = heroes()
    #print(len(list_a))
    list_b = spam()
    #print(len(list_b))
    #print(list_b)
    merged = list(zip(list_a, list_b))
    merged = sorted(merged)
    for i in merged:
        print(i[0])
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
    #import pprint
    #for k, parent in allmatches.items():
    #    print(parent['duration'])

    #pprint.pprint(allmatches.items())
    #match-ids based on mmr in descending order#
    #sortbyMMR = [x for _, x in sorted(zip(B,A), key=lambda pair: pair[0],reverse= True)]
    #print(sortbyMMR)
    #match-ids based on match duration in descending order
    #sortbyDUR = [x for _, x in sorted(zip(C,A), key=lambda pair: pair[0], reverse=True)]
    #print(sortbyDUR)
