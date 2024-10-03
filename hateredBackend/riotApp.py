# try to guess which champion you hate the most using ban data, wr against, times picked, times counterpicked, missing pings against, etc.
# create dict of champions with a value asigned of how much they are hated
# GIT 
from flask import Flask, render_template, request
from pip._vendor import requests
import datetime
import time
class MyCustomException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
charlie_id = "epLML_kUQYCd8gkt3rYS5kUry8hkDFMWsB3VmieVsKS9Z0ygAb6PRK1gjhbWaMKX_QKt0-ODddZTiA"
luca_id = "RzXDVtuDSXzbELdm9rCyWz6oEBFi8gUGWwGjGJxObewnUzEHyZH0KJnEiNIUMWN0LIGlCKxNDJ38Jw"
kyle_id = "xa5CwVf_fYAOXCt0W3vndXkWIKDFAcPWuaae0tvU2c4vHzXgV4RaF0pzjI4jlQX8ggjOG0NyLEcmVw"
adrian_id = "5NS8BS9NVTzm9jMYZS3guMSH-5nMZoUU2U0V4KjdgzFwZnVoKfctQO3TpVa9jpGapQgaMdyA4LdkhA"
andrew_id = "LOWaJF-wrMYFotRf8nXNKoUXTKicwnl6g_-DXSFiWsM2uSJgHaVZqNSCQt45-qpB2F8TthrjWBwykQ"
erik_id = "Dg6SaeFomQ0D5kDjLcVRBjXZRTZjb7Kjywe_QcJ4TdfwFYrqywTwXSZwUBW06iqbGtdtVdU6FqxM2A"
my_api_key = "RGAPI-017dcdf9-bbd1-40ec-95f1-63192fef952a"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
app = Flask(__name__)
@app.route('/data', methods=['GET', 'POST', 'PUT'])
def proxyFunc():
    fill = False
    gameName = str(request.form['game_name'])
    gameTag = str(request.form['game_tag'])
    role = str(request.form['role'])
    queue = str(request.form['queue'])
    games = int(request.form['games'])
    gamesFaced = int(request.form['gamesFaced'])
    if(role=="ALL"):
        fill = True
    print("request received: " + gameName + ", " + gameTag + ", " + role + ", " + queue + ", " + str(games) + ", " + str(gamesFaced))
    retList = find_most_hated(gameName, gameTag, my_api_key, games, fill, role, queue, gamesFaced)
    print("done:   " + retList[0]+ "  " + str(retList[1]))
    return {
        'Most_Hated': str(retList[0]), 
        "Hate_Value": retList[1],
        "Games_Surveyed": retList[2]
        }


def find_most_hated(name, tag, api_key, desiredGames, fill, role, queueId, minGames):
    api_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+name+"/"+tag+"?api_key="+api_key
    resp = requests.get(api_url)
    acc_info = resp.json()
    puuid = acc_info['puuid']
    api_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/"+puuid+"?api_key="+api_key
    resp = requests.get(api_url)
    acc_info = resp.json()
    summonerName = acc_info['gameName']
    api_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"+puuid+"?api_key="+api_key
    resp = requests.get(api_url)
    player_info = resp.json()
    player_id = player_info['id']
    player_accountId = player_info['accountId']
    player_puuid = player_info['puuid']
    player_profileIconId = player_info['profileIconId']
    player_revisionDateEpoch = player_info['revisionDate']
    player_summonerLevel = player_info['summonerLevel']
    dt = datetime.datetime.fromtimestamp(player_revisionDateEpoch/1000)
    player_revisionDateHuman = dt.strftime("%Y-%m-%d %H:%M:%S")

    champions = {}
    games = 0
    sleep = False
    #print(desiredGames/100 + 1)
    for x in range((int)(desiredGames/100)+1):
        #print(x)
        if((desiredGames-(x*100))>=100):
            gamesPerLoop=100
        else:
            gamesPerLoop=desiredGames-(x*100)
        #print(gamesPerLoop)
        api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+str(puuid)+"/ids?queue="+str(queueId)+"&start="+str(x*100)+"&count="+str(gamesPerLoop)+"&api_key="+str(api_key)
        while True:
                resp = requests.get(api_url)
                if(resp.status_code ==429):
                    print("Sleeping: " + str(games) + "/" + str(desiredGames))
                    sleep = True
                    time.sleep(10)
                    continue
                ind_match = resp.json
                break
        if(sleep):
            print("Awake!")
            sleep = False
        resp = requests.get(api_url)
        player_matches = resp.json
        for x in player_matches():
            api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/"+x+"?api_key="+api_key
            while True:
                resp = requests.get(api_url)
                if(resp.status_code ==429):
                    print("Sleeping: " + str(games) + "/" + str(desiredGames))
                    time.sleep(10)
                    continue
                ind_match = resp.json
                break
            if(resp.status_code==200):
                games+=1
                match_info = ind_match()['info']
                # ~~~~~~~
                part = [None for _ in range(2)]
                puuid = [None for _ in range(2)]
                teamPosition = [None for _ in range(2)]
                # ~~~~~~~
                puuid[0] = player_puuid
                for x in match_info['participants']:
                    if(x['puuid']==puuid[0]):
                        part[0] = x
                        break
                teamPosition[0] = part[0]['teamPosition']
                for x in match_info['participants']:
                        if( (x['teamPosition']==teamPosition[0])):
                            if((x['puuid']!=puuid[0])):
                                puuid[1] = x['puuid']
                                part[1] = x
                                break
                #print(str(type(part[1])) + "  " + str(type(part[0])) + "   " + str(fill) + "   " + str(teamPosition[0]) + "   " + str(role))
                if(str(type(part[1]))!="<class 'NoneType'>" and str(type(part[0]))!="<class 'NoneType'>" and (fill or teamPosition[0]==role)):
                    gameLength = part[0]['challenges']['gameLength'] #(adjust non rate stats)
                    if(str(type(part[1]))=="<class 'NoneType'>"):
                        raise TypeError("ooshnapang")
                    teamId = [part[0]['teamId'],part[1]['teamId']]
                    championName = [part[0]['championName'], part[1]['championName']]
                    '''
                    bans = []      ~~ TO BE IMPLIMENTED IF NEEDED BUT FLEX IF NOT NEEDED ~~

                    # doesnt work
                    junglerKillsEarlyJungle = [part[0]['challenges']['junglerKillsEarlyJungle'], part[1]['challenges']['junglerKillsEarlyJungle']]
                    hadAfkTeammate = 0 
                    if(part[0]['challenges']['hadAfkTeammate']!=0 or part[1]['challenges']['hadAfkTeammate']!=0):
                        hadAfkTeammate = 1 #(throws out game)
                    '''

                    # hateLane
                    laneMinionsFirst10Minutes = [part[0]['challenges']['laneMinionsFirst10Minutes'], part[1]['challenges']['laneMinionsFirst10Minutes']]
                    soloKills = [part[0]['challenges']['soloKills'], part[1]['challenges']['soloKills']]
                    turretPlatesTaken = [part[0]['challenges']['turretPlatesTaken'], part[1]['challenges']['turretPlatesTaken']]
                    buffsStolen = [part[0]['challenges']['buffsStolen'], part[1]['challenges']['buffsStolen']]
                    landSkillShotsEarlyGame = [part[0]['challenges']['landSkillShotsEarlyGame'], part[1]['challenges']['landSkillShotsEarlyGame']]
                    pokeBonus = 0
                    if((landSkillShotsEarlyGame[1]+1)/(landSkillShotsEarlyGame[0]+1)>3):
                        pokeBonus = 1.2

                    # hateTeam
                    ccBonus = 0
                    miaBonus = 0
                    ffBonus = 0
                    win = [part[0]['win'], part[1]['win']]
                    pentaKills = [part[0]['pentaKills'], part[1]['pentaKills']]
                    # ~~~~~~~~~~~~~~~
                    gameEndedInSurrender = [part[0]['gameEndedInSurrender'],part[1]['gameEndedInSurrender']]
                    enemyMissingPings = [part[0]['enemyMissingPings'], part[1]['enemyMissingPings']]
                    totalTimeCCDealt = [part[0]['totalTimeCCDealt'], part[1]['totalTimeCCDealt']]
                    if(gameEndedInSurrender[0] and not(win[0])):
                        ffBonus = 1.3
                    else:
                        ffBonus = 0
                    if(totalTimeCCDealt[1] > 50):
                        ccBonus = 1
                    match enemyMissingPings[0]:
                        case x if enemyMissingPings[0]<10:
                            miaBonus = 0
                        case y if enemyMissingPings[0]>30:
                            miaBonus=0.5
                        case z:
                            miaBonus=1
                    
                    # hatePerformance
                    kda = [part[0]['challenges']['kda'], part[1]['challenges']['kda']]
                    champLevel = [part[0]['champLevel'], part[1]['champLevel']]
                    objectivesStolen = [part[0]['objectivesStolen'], part[1]['objectivesStolen']]
                    hateLane = ((soloKills[1]+1)/(soloKills[0]+1))*((laneMinionsFirst10Minutes[1]+1)/(laneMinionsFirst10Minutes[0]+1))*((turretPlatesTaken[1]+1)/(turretPlatesTaken[0]+1)) + (buffsStolen[1]/4) + pokeBonus
                    hateTeam = (ccBonus + ffBonus + miaBonus - win[0] + 2.5*pentaKills[1] - 2.5*pentaKills[0])
                    hatePerformace = ((kda[1])/(kda[0]+1) + ((champLevel[1])/(champLevel[0]+1)) + ((objectivesStolen[1])/(objectivesStolen[0]+1)))
                    if(hateLane>25):
                        hateLane=25
                    hateVal =(hateLane + hateTeam + hatePerformace)

                    if(champions.get(championName[1], "N/A")=="N/A"):
                        champions[championName[1]] = [0, 0, 0, 0, 0]
                    champions[championName[1]][0]=champions[championName[1]][0]*(champions[championName[1]][1]) + hateVal
                    champions[championName[1]][2]=champions[championName[1]][2]*(champions[championName[1]][1]) + hateLane
                    champions[championName[1]][3]=champions[championName[1]][3]*(champions[championName[1]][1]) + hateTeam
                    champions[championName[1]][4]=champions[championName[1]][4]*(champions[championName[1]][1]) + hatePerformace
                    champions[championName[1]][1]+=1
                    champions[championName[1]][0]/=champions[championName[1]][1]
                    champions[championName[1]][2]/=champions[championName[1]][1]
                    champions[championName[1]][3]/=champions[championName[1]][1]
                    champions[championName[1]][4]/=champions[championName[1]][1]
                #else:
                    #print("bad match api data")
            #else:
                #print("bad matchlist api data")
    champions = dict(sorted(champions.items(), key=lambda item: item[1], reverse=True))
    munkle = 0
    printStatement = []
    printStatement.append("")
    printStatement.append("Summoner: " + summonerName + "  </3   Minimum Games Against: " + str(minGames) + "  </3   Role: " + role)
    printStatement.append("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for x in champions:
        if(champions[x][1]>=minGames):
            printStatement.append(x + ": Hate Value: " + str(round(champions[x][0],1)) + ", Games Played: " + str(champions[x][1]) + "       hateLane: " + str(round(champions[x][2],1))+"  hateTeam: "+str(round(champions[x][3],1))+"  hatePerformance: "+str(round(champions[x][4],1))) 
            if(munkle==0):
                mostHated = x
                munkle = 1
            elif(champions[x][0]>champions[mostHated][0]):
                mostHated = x
    retList = []
    if(munkle==0):
        retList.append("N/A, no games surveyed")
        retList.append(-1)
        return retList
    printStatement.append("you hate: " + mostHated)
    printStatement.append("games surveyed: " + str(games))
    printStatement.append("done")
    retList.append("you hate: " + mostHated)
    retList.append(round(champions[mostHated][0],1))
    retList.append(games)
    return(retList)
# Running app
if __name__ == '__main__':
    app.run(debug=True)