import csv

class Player:
    def __init__(self, fName, lName, team, pos, fumbles, games, salary, date, time):
        self.fName = fName
        self.lName = lName
        self.fumbles = fumbles
        self.team =  team
        self.pos = pos
        self.games = games
        self.salary = salary
        self.date = date
        self.time = time


    def __eq__(self, other):
        if self.lName == other.lName and self.fName == other.fName and self.fumbles == other.fumbles and self.pos == other.pos:
            return True
        else: return False

class WR(Player):
    def __init__(self, fName, lName, team, pos, fumbles, games, salary, date, time, targets, rec, recYds, recTDs):
        Player.__init__(self, fName, lName, team, pos, fumbles, games, salary, date, time)
        self.targets = targets
        self.recYds = recYds
        self.recTDs = recTDs
        self.rec = rec

    def getYPC(self):
       return self.recYds/self.rec

    def getCatchPct(self):
        return self.rec/self.targets

class TE(WR):
    pass

class RB(WR):
    def __init__(self, fName, lName, team, pos, fumbles, games, salary, date, time, rAtt, rYds, rTD, targets, rec, recYds, recTD):
        WR.__init__(self, fName, lName, team, pos, fumbles, games, salary, date, time, targets, rec, recYds, recTD)
        self.rAtt = rAtt
        self.rYds = rYds
        self.rTD = rTD

    def getYPR(self):
        return self.rYds/self.rAtt

class QB(Player):
    def __init__(self,  fName, lName, team, pos, fumbles, games, salary, date, time, ints, pAtt, pComp, pYds, pTD, rAtt, rYds, rTD):
        Player.__init__(self,  fName, lName, team, pos, fumbles, games, salary, date, time)
        self.ints = ints
        self.pAtt = pAtt
        self.pComp = pComp
        self.pYds = pYds
        self.pTD = pTD
        self.rAtt = rAtt
        self.rYds = rYds
        self.rTD = rTD

    def getYPA(self):
        return self.pYds/self.pAtt

    def getYPComp(self):
        return self.pYds/self.pComp

class K(Player):
    def __init__(self, fName, lName, team, pos, fumbles, games, salary, date, time, FG, FGA, XPT):
        Player.__init__(self, fName, lName, team, pos, fumbles, games, salary, date, time)
        self.FG = FG
        self.FGA = FGA
        self.XPT = XPT

    def getFGPct(self):
        return self.FG/self.FGA







