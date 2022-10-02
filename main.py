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
definition = False
include_longform = False
starred_only = False

def updateVocabList():
    with open("concepts.org") as file:
        currentUnitNum = ""
        currentUnitName = ""
        currentChapterNum = ""
        currentChapterName = ""
        for line in file:
            line = line[0:-1]  # strip newline at the end
            
            ### to temp variables above, save current metadata such as Chapter number if the current line denotes it
            # save unit or chapter data
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
    
            # if line is a vocab word, save it to vocabList
            # TODO doesnt play nice w/ emacs bold.
            if len(line) != 0 and line[0] != "*":  # ignore other headings
                splitLine = line.split(": ")  # TODO let this be configgable ig
                vocabList.append({
                    "UnitNum": currentUnitNum,
                    "UnitName": currentUnitName,
                    "ChapterNum": currentChapterNum + " ",  # stop looking at Chapter 12.1 as Chapter 1
                    "ChapterName":currentChapterName,
                    "Data": splitLine[0],
                    "Definition": splitLine[1] if len(splitLine) == 2 else "n/a",
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
    global definition
    global include_longform
    global starred_only
    include = config["Include"]
    unitNum = include["unitNum"] == "true"
    unitTitle = include["unitTitle"] == "true"
    chapterNum = include["chapterNum"] == "true"
    chapterTitle = include["chapterTitle"] == "true"
    term = include["term"] == "true"
    definition = include["definition"] == "true"
    include_longform = include["include_longform"] == "true"
    starred_only = include["starred_only"] == "true"


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


def processInput(i):
    if i == "":
        return

    # change IncludeChapters config if input includes only digits, commas, or spaces
    shouldChangeIncludeChapters: bool = True
    for char in i:
        if char not in string.digits + ", ":
            shouldChangeIncludeChapters = False
            continue

    if shouldChangeIncludeChapters:
        changeIncludeChapters(i)

    # TODO rewrite changeIncludeChapters() as 
    # changeIncludeChapters(section: str, key: str, value: str) # use config[section][key]
            


if __name__ == "__main__":
    updateVocabList()
    updateConfig()

    while True:
        print("\n"*50)

        cardDict = getCard()

        cardFound = False
        while not cardFound:
            cardDict = getCard()
            
            if starred_only:
                if cardDict["Data"][0:3] != "[*]":  # this denotes star. make configgable?
                    cardFound = False
                    continue
                
            if not include_longform:
                if cardDict["Data"][0] == "+":
                    cardFound = False
                    continue

            cardFound = True

        
        # cardDict = getCard()

        # # if we don't want longform questions (denoted by "+" prefix)
        # if not include_longform:
        #     # get a new card until no more "+" prefix
        #     while cardDict["Data"][0] == "+":
        #         cardDict = getCard()

        # print unit line
        if unitNum:
            print(cardDict["UnitNum"] + ": ", end="")
        if unitTitle:
            if not unitNum:
                print("Unit: ", end="")
            print(cardDict["UnitName"])

        # print chapter line
        if chapterNum:
            print(cardDict["ChapterNum"][0:-1] + ": ", end="")
        if chapterTitle:
            if not chapterNum:
                print("Chapter: ", end="")
            print(cardDict["ChapterName"])

        # print term
        if term:
            print(cardDict["Data"])
            if definition:
                input()
                print(cardDict["Definition"])

        # wait for input
        i = input()
        processInput(i)
        