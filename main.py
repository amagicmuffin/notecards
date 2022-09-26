# TODO [Include] gets reset on [return], weird

import configparser
import random
import string

# static variables
config = configparser.ConfigParser()
vocabList = []
includeChapters = []
unitNum = False
unitTitle = False
chapterNum = False
chapterTitle = False
term = False
# definition = (under development)

def updateVocabList():
    with open("concepts.org") as file:
        currentUnitNum = ""
        currentUnitName = ""
        currentChapterNum = ""
        currentChapterName = ""
        for line in file:
            line = line[0:-1]  # strip newline at the end
            
            # to temp variables above, save current metadata such as Chapter number if the current line denotes it
            if len(line) > 5:  # random hardcoded value to avoid error
                if line[0:3] == "** ":  # line denotes a unit
                    unitLine: str = line[3:]  # strip heading asterisks
                    unitSplit = unitLine.split(" - ")  # eg ["Unit 1", "What is ..."]
                    currentUnitNum = unitSplit[0]
                    currentUnitName = unitSplit[1]
                elif line[0:4] == "*** ":  # line denotes a chapter
                    chapterLine: str = line[4:]  # strip heading asterisks
                    unitSplit = chapterLine.split(" :: ")  # eg ["Civil Rights", "Chapter 9"]
                    currentChapterNum = unitSplit[1]
                    currentChapterName = unitSplit[0]
    
            # if line is a vocab word, add it to vocabList
            # TODO ignores emacs bold.
            if len(line) != 0 and line[0] != "*":  # ignore other headings
                vocabList.append({
                    "UnitNum": currentUnitNum,
                    "UnitName": currentUnitName,
                    "ChapterNum": currentChapterNum + " ",  # stop looking at Chapter 12.1 as Chapter 1
                    "ChapterName":currentChapterName,
                    "Data": line,
                })
                
# import json  # FOR DEBUG: prettily look at dict
# print(json.dumps(vocabList, indent=4))
# for i in vocabList:
#     print(i)

def updateConfig():
    """"""
    config.read("config.ini")

    # update includeChapters
    chapters = config["Chapters"]["chapters"]
    includeChapters.clear()
    for chapter in chapters.split(","):
        includeChapters.append(f"Chapter {chapter} ")

    # update Include settings
    global unitNum
    global unitTitle
    global chapterNum
    global chapterTitle
    global term
    include = config["Include"]
    unitNum = include["unitNum"] == "true"
    unitTitle = include["unitTitle"] == "true"
    chapterNum = include["chapterNum"] == "true"
    chapterTitle = include["chapterTitle"] == "true"
    term = include["term"] == "true"


def getCard():
    """return card dict according to confog.ini"""
    found: bool = False
    while not found:
        vocabCard = random.choice(vocabList)
        for chapter in includeChapters:
            if chapter in vocabCard["ChapterNum"]:
                found = True  # technically not needed since we return out but just in case
                return vocabCard

def changeIncludeChapters(chapters: str):
    config["Chapters"]["chapters"] = chapters
    with open("config.ini", "w") as f:
        config.write(f)

    updateConfig()

if __name__ == "__main__":
    updateVocabList()
    updateConfig()

    while True:
        print("\n"*50)
        cardDict = getCard()

        # print unit line
        if unitNum:
            print(cardDict["UnitNum"] + ": ", end="")
        else:
            print("Unit: ", end="")
        if unitTitle:
            print(cardDict["UnitName"])

        # print chapter line
        if chapterNum:
            print(cardDict["ChapterNum"][0:-1] + ": ", end="")
        else:
            print("Chapter: ", end="")
        if chapterTitle:
            print(cardDict["ChapterName"])

        # print term
        if term:
            print(cardDict["Data"])

        # wait forinput
        i = input()
        if i != "":
            # TODO add changing settings from cmd line

            # change IncludeChapters config if input includes only digits, commas, or spaces
            for char in i:
                if char in string.digits + ", ":
                    changeIncludeChapters(i)
            

            
