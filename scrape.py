import csv
import requests
import bs4
import players
import defense
import pandas
from collections import OrderedDict
import math

def populateDateTime(playerObject, gameInfo):
    spaceCount = 0
    timeLengthCount = 0
    playerObject['date'] = ""
    playerObject['time'] = ""
    for i in gameInfo:
        if i == " ":
            spaceCount+=1
        elif spaceCount == 1:
            playerObject['date'] += i
        elif spaceCount == 2:
            if i == '0' and timeLengthCount == 0:
                continue
            else:
                playerObject['time'] += i
            timeLengthCount +=1
    return

def getAbbrevFromName(teamName):
    with open("teams/nfl_teams.csv", "r") as file:
        myReader = csv.reader(file, delimiter= ',')
        for i, val in enumerate(myReader):
            if teamName == val[0]:
                return val[1]

def removeParentheses(myString):
    newString = ""
    if myString[0] == '(' and myString[len(myString) - 1] == ")":
        i = 1
        while i < len(myString) - 1:
            newString+=myString[i]
            i+=1
    return newString

def getNameID(fName, lName, team, position):
    temp_id = []
    for i, val in enumerate(fName.replace(".", "")):
        if i > 1:
            break
        temp_id.append(val)
    for j, val in enumerate(lName.replace(".", "")):
        if j > 2:
            break
        temp_id.append(val)
    temp_id.append(team)
    temp_id.append(position)
    final_id = ''.join(temp_id)
    return final_id.upper()

def populateDefenseList(theList, position):
    position.upper()
    with open("teams/nfl_teams.csv", "r") as file:
        myReader = csv.reader(file, delimiter= ',')
        for i, val in enumerate(myReader):
            if i > 0:
                if position == "WR":
                    if len(val[0].split()) > 2:
                        newDef = defense.WR(val[0].split()[0] + " " + val[0].split()[1] , val[0].split()[2], val[1], None, None, None,
                                            None, None, None, None, None)
                    else:
                        newDef = defense.WR(val[0].split() [0], val[0].split()[1], val[1], None, None, None, None, None, None, None, None)
                    theList[val[1]] = newDef.__dict__
                if position == "QB":
                    if len(val[0].split()) > 2:
                        newDef = defense.QB(val[0].split()[0] + " " + val[0].split()[1] , val[0].split()[2], val[1], None, None, None, None, None, None,
                                        None, None, None, None, None, None)
                    else:
                        newDef = defense.QB(val[0].split()[0], val[0].split()[1], val[1], None, None, None, None, None, None,
                                        None, None, None, None, None, None)
                    theList[val[1]] = newDef.__dict__
                if position == "RB":
                    if len(val[0].split()) > 2:
                        newDef = defense.RB(val[0].split()[0] + " " + val[0].split()[1] , val[0].split()[2], val[1], None, None, None,None, None, None,
                                            None, None, None, None, None)
                    else:
                         newDef = defense.RB(val[0].split()[0], val[0].split()[1], val[1], None, None, None, None, None, None,
                                             None, None, None, None, None)
                    theList[val[1]] = newDef.__dict__
                if position == "TE":
                    if len(val[0].split()) > 2:
                        newDef = defense.TE(val[0].split()[0] + " " + val[0].split()[1], val[0].split()[2],
                                            val[1], None, None, None,
                                            None, None, None, None, None)
                    else:
                        newDef = defense.TE(val[0].split()[0], val[0].split()[1], val[1], None, None, None,
                                            None, None, None, None, None)
                    theList[val[1]] = newDef.__dict__
    site = requests.get("https://www.pro-football-reference.com/years/2019/fantasy-points-against-" + position + ".htm")
    src = site.content
    soup = bs4.BeautifulSoup(src, 'lxml')
    allList = (soup.tbody.find_all('tr'))
    for i, val in enumerate(allList):
        tempEntry = allList[i]
        tempList = tempEntry.find_all('td')
        if getAbbrevFromName(tempEntry.th.get_text()) in theList:
            if position == "WR":
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recYdsAllowed'] = tempList[3].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recTDsAllowed'] = tempList[4].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['targetsAllowed'] = tempList[1].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recAllowed'] = tempList[2].get_text()
                if tempList[9].get_text() != "" and tempList[10].get_text() != "":
                    theList[getAbbrevFromName(tempEntry.th.get_text())]['avgPtsAllowed'] = float("{0:.2f}".format((float(tempList[9].get_text()) + float(tempList[10].get_text())))) / 2
                else:
                    theList[getAbbrevFromName(tempEntry.th.get_text())]['avgPtsAllowed'] = 0
            if position == "TE":
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recYdsAllowed'] = tempList[3].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recTDsAllowed'] = tempList[4].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['targetsAllowed'] = tempList[1].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recAllowed'] = tempList[2].get_text()
                if tempList[9].get_text() != "" and tempList[10].get_text() != "":
                    theList[getAbbrevFromName(tempEntry.th.get_text())]['avgPtsAllowed'] = float("{0:.2f}".format((float(tempList[9].get_text()) + float(tempList[10].get_text())))) / 2
                else:
                    theList[getAbbrevFromName(tempEntry.th.get_text())]['avgPtsAllowed'] = 0
            if position == "RB":
                theList[getAbbrevFromName(tempEntry.th.get_text())]['rAttempts'] = tempList[1].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['rYdsAllowed'] = tempList[2].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['rTDsAllowed'] = tempList[3].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recYdsAllowed'] = tempList[6].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recTDsAllowed'] = tempList[7].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['targetsAllowed'] = tempList[4].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['recAllowed'] = tempList[5].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['avgPtsAllowed'] = float("{0:.2f}".format((float(tempList[12].get_text()) + float(tempList[13].get_text())))) / 2
            if position == "QB":
                theList[getAbbrevFromName(tempEntry.th.get_text())]['pCompletionsAllowed'] = tempList[1].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['pAttempts'] = tempList[2].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['pYdsAllowed'] = tempList[3].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['pTDsAllowed'] = tempList[4].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['ints'] = tempList[5].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['rAttempts'] = tempList[8].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['rYdsAllowed'] = tempList[9].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['rTDsAllowed'] = tempList[10].get_text()
                theList[getAbbrevFromName(tempEntry.th.get_text())]['avgPtsAllowed'] = float("{0:.2f}".format((float(tempList[15].get_text()) + float(tempList[16].get_text())))) / 2
    return

# better variable names needed dog
def populatePositionList(theList, position):
    site = requests.get("https://www.fantasypros.com/nfl/stats/" + position.lower() + ".php")
    src = site.content
    soup = bs4.BeautifulSoup(src, 'lxml')
    allList = (soup.tbody.find_all('tr'))
    for i, val in enumerate(allList):
        tempList = allList[i].find_all('td')
        if position == "WR":
            if len(tempList[0].get_text().split()) > 3:
                newWR = players.WR(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1] + " " + tempList[0].a.get_text().split()[2].replace(".", ""),
                                   removeParentheses(tempList[0].get_text().split()[3]), position, None, None, None, None, None, None, None, None, None)
            else:
                newWR = players.WR(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1], removeParentheses(tempList[0].get_text().split()[2]), position, None, None, None, None, None, None, None, None, None)
            theList[getNameID(newWR.fName, newWR.lName, newWR.team, position)] = newWR.__dict__
            theList[getNameID(newWR.fName, newWR.lName, newWR.team, position)]['games'] = tempList[12].get_text()
            theList[getNameID(newWR.fName, newWR.lName, newWR.team, position)]['rec']= tempList[1].get_text()
            theList[getNameID(newWR.fName, newWR.lName, newWR.team, position)]['recYds']= tempList[3].get_text()
            theList[getNameID(newWR.fName, newWR.lName, newWR.team, position)]['recTDs']= tempList[7].get_text()
            theList[getNameID(newWR.fName, newWR.lName, newWR.team, position)]['targets']= tempList[2].get_text()
            theList[getNameID(newWR.fName, newWR.lName, newWR.team, position)]['fumbles']= tempList[11].get_text()
        if position == "TE":
            if len(tempList[0].get_text().split()) > 3:
                newTE = players.TE(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1] + " " + tempList[0].a.get_text().split()[2].replace(".", ""),
                                   removeParentheses(tempList[0].get_text().split()[3]), position, None, None, None, None, None, None, None, None, None)
            else:
                newTE = players.TE(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1], removeParentheses(tempList[0].get_text().split()[2]), position, None, None, None, None, None, None, None, None, None)
            theList[getNameID(newTE.fName, newTE.lName, newTE.team, position)] = newTE.__dict__
            theList[getNameID(newTE.fName, newTE.lName, newTE.team, position)]['games'] = tempList[12].get_text()
            theList[getNameID(newTE.fName, newTE.lName, newTE.team, position)]['rec']= tempList[1].get_text()
            theList[getNameID(newTE.fName, newTE.lName, newTE.team, position)]['recYds']= tempList[3].get_text()
            theList[getNameID(newTE.fName, newTE.lName, newTE.team, position)]['recTDs']= tempList[7].get_text()
            theList[getNameID(newTE.fName, newTE.lName, newTE.team, position)]['targets']= tempList[2].get_text()
            theList[getNameID(newTE.fName, newTE.lName, newTE.team, position)]['fumbles']= tempList[11].get_text()
        if position == "RB":
            if len(tempList[0].get_text().split()) > 3:
                newRB = players.RB(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1] + " " + tempList[0].a.get_text().split()[2].replace(".", ""),
                                   removeParentheses(tempList[0].get_text().split()[3]), position, None, None, None,
                                   None, None, None, None, None, None, None, None, None)
            else:
                newRB = players.RB(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1], removeParentheses(tempList[0].get_text().split()[2]), position, None, None, None, None, None, None, None, None, None, None, None, None)
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)] = newRB.__dict__
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['rAtt'] = tempList[1].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['rYds'] = tempList[2].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['rTD'] = tempList[6].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['rec'] = tempList[7].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['targets'] = tempList[8].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['recYds'] = tempList[9].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['recTDs'] = tempList[11].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['fumbles'] = tempList[12].get_text()
            theList[getNameID(newRB.fName, newRB.lName, newRB.team, position)]['games'] = tempList[13].get_text()
        if position == "QB":
            if len(tempList[0].get_text().split()) > 3:
                newQB = players.QB(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1] + " " + tempList[0].a.get_text().split()[2].replace(".", ""),
                                   removeParentheses(tempList[0].get_text().split()[3]), position, None, None, None,
                                   None, None, None, None, None, None, None, None, None, None)
            else:
                newQB = players.QB(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1], removeParentheses(tempList[0].get_text().split()[2]), position, None, None, None, None, None, None, None, None, None, None, None, None, None)
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)] = newQB.__dict__
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['pComp'] = tempList[1].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['pAtt'] = tempList[2].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['pYds'] = tempList[4].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['pTD'] = tempList[6].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['ints'] = tempList[7].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['rAtt'] = tempList[9].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['rYds'] = tempList[10].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['rTD'] = tempList[11].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['games'] = tempList[13].get_text()
            theList[getNameID(newQB.fName, newQB.lName, newQB.team, position)]['fumbles'] = tempList[12].get_text()
    return

def populateDKinfo(theList, position):
    data = pandas.read_csv('https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=21&draftGroupId=32781', usecols=['Position', 'Name', 'Salary', 'Game Info', 'TeamAbbrev'])
    i = 0
    while i < data.count()[1]:
        if position == "WR" and data['Position'][i] == "WR":
            theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])]['salary'] = data['Salary'][i]
            populateDateTime(theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])], data['Game Info'][i])
        if position == "TE" and data['Position'][i] == "TE":
            theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])]['salary'] = data['Salary'][i]
            populateDateTime(theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])], data['Game Info'][i])
        if position == "RB" and data['Position'][i] == "RB":
            theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])]['salary'] = data['Salary'][i]
            populateDateTime(theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])], data['Game Info'][i])
        if position == "QB" and data['Position'][i] == "QB":
            theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])]['salary'] = data['Salary'][i]
            populateDateTime(theList[getNameID(data['Name'][i].split()[0], data['Name'][i].split()[1], data['TeamAbbrev'][i], data['Position'][i])], data['Game Info'][i])
        if position == "DST" and data['Position'][i] == "DST":
            theList[data['TeamAbbrev'][i]]['salary'] = data['Salary'][i]
            populateDateTime(theList[data['TeamAbbrev'][i]], data['Game Info'][i])
        i+=1
    return

def main():

    wrList = {}
    rbList = {}
    teList = {}
    qbList = {}

    wrDefList = {}
    rbDefList = {}
    teDefList = {}
    qbDefList = {}


    # site = requests.get("https://www.fantasypros.com/nfl/stats/qb.php")
    # src = site.content
    # soup = bs4.BeautifulSoup(src, 'lxml')
    # allList = (soup.tbody.find_all('tr'))
    # tempList = allList[105].find_all('td')
    # print(len(allList))
    # print(tempList[0].get_text().split())
    # print(getNameID(tempList[0].a.get_text().split()[0].replace(".", ""), tempList[0].a.get_text().split()[1], removeParentheses(tempList[0].get_text().split()[2]), "Qb"))




    populateDefenseList(wrDefList, "WR")
    populateDefenseList(teDefList, "TE")
    populateDefenseList(rbDefList, "RB")
    populateDefenseList(qbDefList, "QB")
    #
    populatePositionList(wrList, "WR")
    populatePositionList(teList, "TE")
    populatePositionList(rbList, "RB")
    populatePositionList(qbList, "QB")

    populateDKinfo(wrDefList, 'DST')
    populateDKinfo(teDefList, 'DST')
    populateDKinfo(qbDefList, 'DST')
    populateDKinfo(rbDefList, 'DST')

    populateDKinfo(wrList, 'WR')
    populateDKinfo(teList, 'TE')
    populateDKinfo(rbList, 'RB')
    populateDKinfo(qbList, 'QB')
    #
    #
    print(wrList)
    print(teList)
    print(qbList)
    print(rbList)
    #
    print(wrDefList)
    print(teDefList)
    print(wrDefList)
    print(teDefList)


if __name__ == "__main__":
    main()

