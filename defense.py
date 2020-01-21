class Team:
    def __init__(self, city, nickname, abbreviation, salary, date, time):
        self.city = city
        self.nickname = nickname
        self.abbreviation = abbreviation
        self.salary = salary
        self.date = date
        self.time = time

    def __eq__(self, other):
        if self.city == other.city and self.nickname == other.nickname:
            return True
        else: return False

class WR(Team):
    def __init__ (self, city, nickname, abbreviation, salary, date, time, recYdsAllowed, recTDsAllowed, targetsAllowed, recAllowed, avgPtsAllowed):
        Team.__init__(self, city, nickname, abbreviation, salary, date, time)
        self.recYdsAllowed = recYdsAllowed
        self.recTDsAllowed = recTDsAllowed
        self.targetsAllowed = targetsAllowed
        self.recAllowed = recAllowed
        self.avgPtsAllowed = avgPtsAllowed

    def YPC(self):
        return self.recYdsAllowed/self.recAllowed

    def catchPct(self):
        return self.recAllowed/self.targetsAllowed

class TE(WR):
    pass

class RB(WR):
    def __init__(self, city, nickname, abbreviation, salary, date, time, rYdsAllowed, rTDsAllowed, rAttempts, recYdsAllowed, recTDsAllowed, targetsAllowed, recAllowed, avgPtsAllowed):
        WR.__init__(self, city, nickname, abbreviation, salary, date, time, recYdsAllowed, recTDsAllowed, targetsAllowed, recAllowed, avgPtsAllowed)
        self.rYdsAllowed = rYdsAllowed
        self.rTDsAllowed = rTDsAllowed
        self.rAttempts = rAttempts

    def YPR(self):
        return self.rYdsAllowed/self.rAttempts



class QB(Team):
    def __init__(self, city, nickname, abbreviation, salary, date, time, pYdsAllowed, pTDsAllowed, pAttempts, pCompletionsAllowed, rYdsAllowed, rTDsAllowed, rAttempts, ints, avgPtsAllowed):
        Team.__init__(self, city, nickname, abbreviation, salary, date, time)
        self.pYdsAllowed = pYdsAllowed
        self.pTDsAllowed = pTDsAllowed
        self.pAttempts = pAttempts
        self.pCompletionsAllowed = pCompletionsAllowed
        self.rYdsAllowed = rYdsAllowed
        self.rTDsAllowed = rTDsAllowed
        self.rAttempts = rAttempts
        self.ints = ints
        self.avgPtsAllowed = avgPtsAllowed

    def attemptsPerInt(self):
        return self.pAttempts/self.ints

    def YPA(self):
        return self.pYdsAllowed/self.pAttempts

    def tdsAllowedPerAttempt(self):
        return self.pTDsAllowed/self.pAttempts