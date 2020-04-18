import time
import requests
from flask import Flask, render_template, request, flash, Markup, make_response
from flask_minify import minify
import scraper
from natsort import humansorted
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
app = Flask(__name__, template_folder='template')
minify(app=app, html=True, js=True, cssless=True)
app.secret_key = "23df833be15d3ab59ba66172bcfb78a0"


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

from werkzeug.exceptions import default_exceptions, abort


def _handle_http_exception(e):
    return make_response(render_template("error.html", code=e.code, description=e.description), e.code)

for code in default_exceptions:
    app.errorhandler(code)(_handle_http_exception)

@app.route("/", methods=["POST", "GET"])
def index():
    selected = False
    # Fetch player names from dota2protracker.com
    player_names, player_rec = scraper.peeps()
    if player_names:
        player_names = list(zip(player_names, player_rec))
        player_names = humansorted(player_names)
    else:
        player_names = []
        app.logger.info("Player names is empty")
    # Fetch hero names from dota2protracker.com
    hero_names, hero_rec = scraper.heroes()
    if hero_names:
        hero_names = list(zip(hero_names, hero_rec))
        hero_names = sorted(hero_names)
    else:
        hero_names = []
        app.logger.info("Hero names is empty")
    #initalize allmatches
    allmatches = []
    if request.method == "POST" and "players" not in request.form:
        hero = request.form.get("heroes")
        selected = hero
        player_names = humansorted(scraper.plimiter(hero))
        message = Markup(f"Player list has been updated to only show players that have played <strong>{hero}</strong> in the last 8 days.")
        flash(message, 'plimited')
    elif request.method == "POST":
        hero = request.form.get("heroes")
        player = request.form.getlist("players")
        role = request.form.get("role-radio", "")
        matchup = request.form.getlist("matchup")
        A, B , C, D ,E , limited = scraper.hero(player,hero,"green", role, matchup)
        if matchup:
            time.sleep(1)
        F , G , H , I, J , limited = scraper.hero(player, hero, "red", role, matchup)
        if limited:
            message = Markup("<strong>Missing potential results</strong> The Stratz API request limit has been reached. Please wait before reattempting query.")
            flash(message, 'limited')
        extra = ""
        if role != "Any":
            extra = f"(playing on {role.lower()} lane)."
            if matchup:
                extra = f"(playing on {role.lower()} lane versus {matchup[0]})."
                if len(matchup) > 1:
                    extra = f"playing on {role.lower()} lane versus selected matchups."
        if len(player) == 1:
            player = f"<strong>{player[0]}</strong>"
        else:
            player = "selected players"
        if len(A) == 0 and len(F) == 0:
            message = Markup(f"No matches from <strong>{player}</strong> found for <strong>{hero}</strong> <em>{extra}</em><small> <br> Please note only matches from the past 8 days are queried</small>")
            flash(message, 'danger')
        else:
            res1 = {key: {'outcome': wol, 'duration': dur, 'avgmmr': mmr, 'name': pn} for key, mmr, dur, wol, pn in zip(A, B , C, D ,E)}
            res2 = {key: {'outcome': wol, 'duration': dur, 'avgmmr': mmr, 'name': pn} for key, mmr, dur, wol, pn in zip(F , G , H , I, J)}
            allmatches = {**res1, **res2}
            message = Markup(f"Showing match-ids from {player} for <strong>{hero}</strong>; <em>{extra}</em> <br>Win Percentage: <strong>{percent(A,F)}</strong>, "
                             f"Average duration: <strong>{duration(C,H)}</strong>, Average MMR: <strong>{average_mmr(B,G)}</strong>.")
            flash(message, 'primary')
        limitNO = 0
        response = requests.get(f"https://api.stratz.com/api/v1/Language")
        if response.status_code == 200:
            limitNO = int(response.headers['X-RateLimit-Remaining-Hour'])
        if limitNO == 0:
            return render_template("index.html", player_names=player_names, hero_names=hero_names, result=allmatches, limit = True, selected = selected)
    return render_template("index.html", player_names = player_names, hero_names= hero_names, result = allmatches, limit= False, selected= selected)

@app.route('/match/<int:match_id>')
def parse(match_id):
    stats, parsed = scraper.parser(match_id)
    if parsed:
        from datetime import datetime
        now = datetime.now()
        date_format = "%d/%m/%Y %H:%M:%S"
        current = now.strftime("%d/%m/%Y %H:%M:%S")
        a = datetime.strptime(current, date_format)
        b = datetime.strptime(stats['endtime'], date_format)
        delta = (a - b).days
        return render_template("parsed.html", match = match_id, stats =stats, days = delta)
    else:
        abort(404, f"Match-id({match_id}) is not a valid match / Stratz API limit reached!")

if __name__ == "__main__":
    app.run()
