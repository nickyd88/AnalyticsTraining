#                            #
#                            #
# SCRAPING FOR SPECIFIC DATA #
#                            #
#                            #

import urllib2
from bs4 import BeautifulSoup
import unicodedata
from namemapper import Ascii

class BaseballPressReader:

    def __init__(self, urlstring):
        req = urllib2.Request(urlstring)
        connection = urllib2.urlopen(req)
        document = connection.read()
        self.soup = BeautifulSoup(document, "html.parser")
        self.starters = []

    def ReadStartingLineups(self):

        if len(self.starters) == 0:
            games = self.soup.find_all('div', {'class' : 'game clearfix'})
            for game in games: #i = 0 through # of games
                pitchers = game.find_all('a', {'class' : 'player-link'})
                for player in pitchers:
                    self.starters.append([0, player.text, 'NA', 'SP'])
                matchup = game.find_all('div', {'class' : 'cssDialog clearfix'})[0]
                teams = matchup.find_all('div', {'class' : 'team-lineup clearfix'})
                for team in teams:
                    playerdata = team.find_all('div', {'class' : 'players'})[0]
                    players = playerdata.find_all('div')
                    for player in players:
                        order = int(player.text.split('.')[0])
                        name = player.a.text
                        asciiname = Ascii(name)
                        handedness = player.text.split("(")[1].split(") ")[0]
                        position = player.text.split("(")[1].split(") ")[1]
                        self.starters.append([order, asciiname, handedness, position])
            return self.starters
        else:
            return self.starters

