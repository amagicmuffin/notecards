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


def updateConfig():
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


def addStr(yPos, str, wrap, scr_width, stdscr):
    if wrap == "shorten":
        stdscr.addstr(yPos, 2, textwrap.shorten(str, width=scr_width-3, placeholder="..."))
        return
    if wrap == "fill":
        stdscr.addstr(yPos, 2, textwrap.fill(str, width=scr_width-3, subsequent_indent="  "))
        return
    raise Exception('wrap type must either be "shorten" or "fill"')


def startFlashcards(stdscr):
    updateVocabList()
    updateConfig()

    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()

    k = 0
    while k != ord('q'):
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
            s += cardDict["UnitNum"] + ": "
        else:
            s += "Unit: "
        if unitTitle:
            s += cardDict["UnitName"]
        addStr(1, s, "shorten", scr_width, stdscr)

        # print chapter line
        s = ""
        if chapterNum:
            s += cardDict["ChapterNum"][0:-1] + ": "
        else:
            s += "Chapter: "
        if chapterTitle:
            s += cardDict["ChapterName"]
        addStr(2, s, "shorten", scr_width, stdscr)

        # print term
        s = ""
        if term:
            s = cardDict["Data"]
            addStr(4, s, "fill", scr_width, stdscr)
            if definition:
                stdscr.getch()
                s = cardDict["Definition"]
                addStr(7, s, "fill", scr_width, stdscr)

        stdscr.refresh()
        k = stdscr.getch()


def main():
    curses.wrapper(startFlashcards)


if __name__ == "__main__":
    main()