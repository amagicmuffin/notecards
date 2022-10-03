# TODO [Include] gets reset on [return], weird
import curses
import configparser
import random
import string
import textwrap

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
            


def startFlashcards(stdscr):
    updateVocabList()
    updateConfig()

    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()

    k = 0
    while k != ord('q'):
        # old: print("\n"*50)
        stdscr.erase()

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

        

        scr_height, scr_width = stdscr.getmaxyx()
        
        # print unit line
        s = ""
        if unitNum:
            # print(cardDict["UnitNum"] + ": ", end="")
            s += cardDict["UnitNum"] + ": "
        else:
            # print("Unit: ", end="")
            s += "Unit: "
        if unitTitle:
            # print(cardDict["UnitName"])
            s += cardDict["UnitName"]
        stdscr.addstr(1, 2, textwrap.shorten(s, width=scr_width-6, placeholder="..."))

        # print chapter line
        s = ""
        if chapterNum:
            # print(cardDict["ChapterNum"][0:-1] + ": ", end="")
            s += cardDict["ChapterNum"][0:-1] + ": "
        else:
            # print("Chapter: ", end="")
            s += "Chapter: "
        if chapterTitle:
            # print(cardDict["ChapterName"])
            s += cardDict["ChapterName"]
        stdscr.addstr(2, 2, textwrap.shorten(s, width=scr_width-6, placeholder="..."))

        # print term
        s = ""
        if term:
            # print(cardDict["Data"])
            s = cardDict["Data"]
            stdscr.addstr(4, 2, textwrap.fill(s, width=scr_width-6))
            if definition:
                stdscr.getch()
                # print(cardDict["Definition"])
                s = cardDict["Definition"]
                stdscr.addstr(7, 2, textwrap.fill(s, width=scr_width-6))

        # wait for input TODO: this is left over from non-curses version
        # i = input()
        # processInput(i)

        stdscr.refresh()
        k = stdscr.getch()


def main():
    curses.wrapper(startFlashcards)


if __name__ == "__main__":
    main()