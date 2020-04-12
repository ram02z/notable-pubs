from flask import Flask, render_template, request, flash
import scraper
from natsort import humansorted
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
app = Flask(__name__, template_folder='template', static_folder="static", static_url_path='')
app.secret_key = "23df833be15d3ab59ba66172bcfb78a0"
# Fetch player names from dota2protracker.com
player_names = scraper.peeps()
if player_names:
    player_rec = scraper.lowl()
    player_names = list(zip(player_names, player_rec))
    player_names = humansorted(player_names)
else:
    player_names = []
# Fetch hero names from dota2protracker.com
hero_names = scraper.heroes()
if hero_names:
    hero_rec = scraper.spam()
    hero_names = list(zip(hero_names, hero_rec))
    hero_names = sorted(hero_names)
else:
    hero_names = []

def percent(x,y):
    if len(x) == 0 and len(y) > 0:
        return "0%"
    elif len(y) == 0:
        return "100%"
    else:
        fl = len(x)/(len(x)+len(y))
        return str(round(fl*100, 2))+"%"
def duration(x,y):
    times = x+y
    secs = 0
    for i in times:
        m, s = i.split(':')
        secs += (int(m)*60) + int(s)
    avg = int(secs/len(times))
    return '{0:02d}:{1:02d}'.format(*divmod(avg, 60))

def average_mmr(x,y):
    mmrs = x+y
    mmrs = [ int(i) for i in mmrs ]
    return int(sum(mmrs) / len(mmrs))


@app.route("/", methods=["GET","POST"])
def index():
    allmatches = []
    if request.method == "POST":
        hero = request.form.get("heroes")
        player = request.form.getlist("players")
        role = request.form.get("role-radio", "")
        matchup = request.form.get("matchup")
        A, B , C, D ,E = scraper.hero(player,hero,"green")
        F , G , H , I, J = scraper.hero(player, hero, "red")
        if len(player) == 1:
            player = player[0]
        else:
            player = "selected players"
        if len(A) == 0 and len(E) == 0:
            flash(f"No matches from {player} found for {hero}. Please note only matches from the past 8 days are queried.", 'danger')
        else:
            res1 = {key: {'outcome': wol, 'duration': dur, 'avgmmr': mmr, 'name': pn} for key, mmr, dur, wol, pn in zip(A, B , C, D ,E)}
            res2 = {key: {'outcome': wol, 'duration': dur, 'avgmmr': mmr, 'name': pn} for key, mmr, dur, wol, pn in zip(F , G , H , I, J)}
            allmatches = {**res1, **res2}
            flash(f"Showing match-ids from {player} for {hero}. Win Percentage: {percent(A,F)}, Average duration: {duration(C,H)}, Average MMR: {average_mmr(B,G)}.", 'primary')
    return render_template("index.html", player_names = player_names, hero_names= hero_names, result = allmatches)



if __name__ == "__main__":
    app.run(debug=True)