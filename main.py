import configparser

with open("concepts.org") as file:
    currentUnitNum = ""
    currentUnitName = ""
    currentChapterNum = ""
    currentChapterName = ""
    tempList = []
    for line in file:
        line = line[0:-1]  # strip newline T the end
        # set current metadata such as Chapter number if the current line denotes it
        if len(line) > 5:  # random hardcoded value
            if line[0:3] == "** ":  # second level heading (units)
                #print("UNIT: " + line)
                unitLine: str = line[3:]  # strip heading asterisks
                unitSplit = unitLine.split(" - ")  # eg ["Unit 1", "What is ..."]
                currentUnitNum = unitSplit[0]
                currentUnitName = unitSplit[1]
            elif line[0:4] == "*** ":  # third level heading (chapters)
                #print("CHAPTER: " + line)
                chapterLine: str = line[4:]  # strip heading asterisks
                unitSplit = chapterLine.split(" :: ")  # eg ["Civil Rights", "Chapter 9"]
                currentChapterNum = unitSplit[1]
                currentChapterName = unitSplit[0]
                
        if len(line) != 0 and line[0] != "*":  # ignore other headings
            #print(currentUnitNum, currentChapterNum, line)
            tempList.append({
                "UnitNum": currentUnitNum,
                "UnitName": currentUnitName,
                "ChapterNum": currentChapterNum,
                "ChapterName":currentChapterName,
                "Data": line,
            })
            
import json  # FOR DEBUG: prettily look at dict
print(json.dumps(tempList, indent=4))

config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '45',
                     'Compression': 'yes',
                     'CompressionLevel': '9'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
    config.write(configfile)