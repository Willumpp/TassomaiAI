import pyautogui
import pyperclip
import time
import ast
import random
from PIL import Image

time.sleep(3)

##----- START ON TAB 1 -----##
global tabNum
tabNum = 1

def AnswerFile(quizNum):
    
    with open("page.txt","r") as file:
        lines = file.readlines()
        
        if quizNum == 1:
            ansFile = str(lines[1][0:-1])+".txt"
        else:
            ansFile = str(lines[3][0:-1])+".txt"

    return ansFile

def DetermineAnswer():
    pos = ()

    #Generate random answer
    num = random.randint(1,4)
    if num == 1: pos = (570,520)
    if num == 2: pos = (970,520)
    if num == 3: pos = (570,640)
    if num == 4: pos = (970,640)
    
    pyautogui.click(pos[0],pos[1])

    #Take screenshot of answer
    time.sleep(1)
    pyautogui.screenshot("ImageAnswers.png")
    newIm = Image.open("ImageAnswers.png")

    #Get answer colours
    #1
    cropIm = newIm.crop((570,520,571,521))
    cropIm.save("CorrectNew1.png")
    #2
    cropIm = newIm.crop((970,520,971,521))
    cropIm.save("CorrectNew2.png")
    #3
    cropIm = newIm.crop((570,640,571,641))
    cropIm.save("CorrectNew3.png")
    #4
    cropIm = newIm.crop((970,640,971,641))
    cropIm.save("CorrectNew4.png")

    answerNum = 0
    if Image.open("CorrectNew1.png","r") == Image.open("Correct.png","r"): answerNum = 1
    if Image.open("CorrectNew2.png","r") == Image.open("Correct.png","r"): answerNum = 2
    if Image.open("CorrectNew3.png","r") == Image.open("Correct.png","r"): answerNum = 3
    if Image.open("CorrectNew4.png","r") == Image.open("Correct.png","r"): answerNum = 4

    return answerNum

def QuestionTotal(quizNum):
    with open("page.txt","r") as file:
        lines = file.readlines()

    qTotal = lines[2*quizNum].replace("Target ","")
    if len(qTotal)>=3: qTotal = int(qTotal[1:3])
    else: qTotal = int(qTotal[-1])

    return qTotal
    

#Copy page and paste
def CopyPage():
    newFile = []
    pyautogui.hotkey("ctrl","a")
    pyautogui.hotkey("ctrl","c")

    paste = pyperclip.paste()
    
    allowed_characters = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n"
    test = ''.join(c for c in paste if c in allowed_characters )

    #Paste to file
    with open("page.txt","w") as file:
        file.write(test)

    with open("page.txt","r") as file:
        file = file.readlines()
        newFile = file[file.index("Take a quiz\n"):-1]

    with open("page.txt","w") as file:
        for item in newFile:
            file.write(item)


#Get Question
def GetQuestion(qNum,quizNum):
    with open("page.txt", "r") as file:
        lines = file.readlines()
        
    qTotal = QuestionTotal(quizNum)
                              
    return lines[((2*qTotal)+2)+((qNum-1)*7)+9]

#Compare with blacklist
def Blacklist():
    CopyPage()
    quizNum = 1

    with open("Blacklist.txt","r") as file:
        blacklist = file.readlines()
        
    with open("page.txt","r") as file:
        lines = file.readlines()

    for name in blacklist:
        if name == lines[1]:
            quizNum = 2

    return quizNum
    
       
#Check Answer
def QuestionCheck(qNum,quizNum):
    NewQuestion = ("","")
    
    with open("page.txt","r") as file:
        lines = file.readlines()
        
    ansFile = AnswerFile(quizNum)

    question = GetQuestion(qNum,quizNum)
    qLine = lines.index(question)
    
    #Known Quiz
    try:
        with open(ansFile,"r") as file:
            dictionary = ast.literal_eval(file.read())
              
        print(question)
        
        #Known Answer
        if question[0:-1] in dictionary:
            answerNum = random.randint(1,4)
            
            answer = dictionary.get(question[0:-1])
            for i in range(0,5):
                if lines[qLine+i+1][0:-1] == answer:
                    answerNum = i

            if answerNum == 1: pyautogui.click(570,520)
            if answerNum == 2: pyautogui.click(970,520)
            if answerNum == 3: pyautogui.click(570,640)
            if answerNum == 4: pyautogui.click(970,640)

            NewQuestion = (question[0:-1],dictionary.get(question[0:-1]))
            
        #Unkown Answer            
        else:
            answerNum = DetermineAnswer()

            NewQuestion = (question[0:-1],lines[qLine+answerNum+1][0:-1])

            print (answerNum)
            print("Unknown Answer")
            
##    #Unkown Quiz 
    except: pass
##        print("Unkown Quiz")
##        ##with open(ansFile,"w") as file:
##        ##    file.write("{}")
##
##        answerNum = DetermineAnswer()
##
##        NewQuestion = (question[0:-1],lines[qLine+answerNum+1][0:-1])
##
##        print (answerNum)
##        print("Unknown Answer")
##
    return NewQuestion

def main():
    global tabNum
    
    time.sleep(1)
    #Get Quiz
    with open("page.txt","r") as file:
        lines = file.readlines()

    quizNumber = Blacklist()
    qTotal = QuestionTotal(quizNumber)

    ansFile = AnswerFile(quizNumber)
    print(ansFile)
    print(quizNumber)
    print("*************")

    #Choose quiz
    if quizNumber == 2: pyautogui.click(989,626,interval=1.25)
    else: pyautogui.click(789,626,interval=1.25)

    #Click "No Thanks"
    pyautogui.click(950,738,interval=0.5)
    #Click to de-select
    pyautogui.click(400,700,clicks=2,interval=1)
    time.sleep(0.5)
    
    CopyPage()
    for i in range(1,qTotal+1):
        new = QuestionCheck(i,quizNumber)

        #Update Answers
        with open(ansFile,"r") as file:
                dictionary = ast.literal_eval(file.read())

        if new[0] not in dictionary:
            dictionary[new[0]] = new[1]
            
            with open(ansFile,"w") as file:
                    file.write(str(dictionary))
        
        time.sleep(3)

    #Click continue
    pyautogui.click(950,700,interval=0.75)
    #Click skip
    pyautogui.click(1320,719,clicks=2,interval=0.75)

    #Switch to Will's Tab (2)
    if tabNum == 1:
        pyautogui.click(950,1050,interval=0.25)
        pyautogui.click(1000,1000,interval=0.25)
        tabNum = 2
        
    #Switch to Other Tab (1)
    else: 
        pyautogui.click(950,1050,interval=0.25)
        pyautogui.click(800,1000,interval=0.25)
        tabNum = 1
        
    main()
    

main()
