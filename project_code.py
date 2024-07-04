from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import os
from gtts import gTTS
import time
from googletrans import Translator, constants

# global vars
text = ""
fileText = ""
fileName = ""
isfileSelected = False

# "root" is an instance variable of TKinter
# Starting of the TKinter application
root = Tk()

# setting the board size and colour of background
root.geometry("1000x700")
root.configure(background="white")

# setting the title of app
root.title('Text to Speech')


## Text Box Frame(folder)
# create a frame
textFrame = Frame(root, background="#fff")
# place it on grid
textFrame.grid(column=1,row=0,padx=20,pady=20,sticky= "w")
# make a text label
textLabel = Label(textFrame, text = "\t\tText to Speech", font= ("Times", 20),background="#fff", foreground="#455a64")
# place it
textLabel.grid(column=0,row=0,padx=20,pady=8,sticky= "w")
# make a text label
textLabel = Label(textFrame, text = "Enter text here", font= ("Helvetica", 16),background="#fff", foreground="#283832")
# place it
textLabel.grid(column=0,row=1,padx=20,pady=4,sticky= "w")
# make an input text field
textInput = Text(textFrame, font= ("Helvetica", 12),background="#fff", height= 5, width= 60, pady=3, padx=3, foreground="#283832", highlightthickness=0)
# place it
textInput.grid(column=0,row=2,padx=20,pady=4,sticky= "w")


## Languages List Frame(folder)
# make frame
langFrame = Frame(root, background="#fff")
# place it
langFrame.grid(column=0,row=0,padx=20,pady=30,sticky= "w")
# make scrollbar
scroll = Scrollbar(root, orient="vertical", troughcolor="#fff", bd=0, elementborderwidth=0)
# place it
scroll.grid(column=0,row=0,padx= 0,pady=0,sticky="w")
# make a text label
textLabel = Label(langFrame, text = "Languages", font= ("Helvetica", 10), background="#fff")
# place it
textLabel.grid(column=0,row=0,padx=0,pady=0,sticky= "nw")
# make a list box for languages
langListBox = Listbox(langFrame, width=20, height= 10, borderwidth=0, highlightbackground="#fff", highlightthickness=0)
c = 1
# for making list of languages
for code in constants.LANGUAGES:
    langListBox.insert(c, constants.LANGUAGES[code])
    if code=="en":
        langListBox.select_set(c-1)
    c += 1


# place the list on grid and configure it
langListBox.grid(column=0,row=1,padx= 0,pady=10,sticky="w")
scroll.config(command=langListBox.yview)
langListBox.config(yscrollcommand=scroll.set)
langSelected = langListBox.get(langListBox.curselection())


# Miscelaneous functions
def langCode(lang):
    for i in constants.LANGUAGES:
        if constants.LANGUAGES[i]==lang:
            return i
    return "en"


# Button Events
def addFileButtonEvent():
    global text
    global fileText
    global isfileSelected
    global fileName
    # code for picking up the file
    if not isfileSelected:
        fileName = askopenfilename()
        if fileName[-3:] == "txt":
            file = open(fileName, "r")
            fileText = file.read()
            file.close()
            isfileSelected = True
            fileLabel.configure(text = fileName)
            addFileButton.configure(background="#455a64", foreground="#fff", text="Selected")
    print("add file ->"+fileName + " "+ fileText)

def playButtonEvent():
    global text
    global fileText
    global isfileSelected
    global fileName
    global  langSelected
    langSelected = langListBox.get(langListBox.curselection())

    # code for play button
    print(fileText)
    outText = ""
    text = textInput.get("1.0",END)
    if isfileSelected:
        if fileText == "":
            messagebox.showerror("Error", "No text in the file selected")
        else:
            outText = fileText
    else:
        if text == '':
            messagebox.showerror("Error", "Nothing entered in the text field")
        else:
            outText = text
    langCodeName = "en"
    if not outText == "":
        if langSelected != "english":
            langCodeName = langCode(langSelected)
            # outText = convertLang("en", langCodeName, outText)
        currtime = round(time.time()*1000)
        obj = gTTS(outText, lang=langCodeName, slow=False)
        fileAddress = f"output{currtime}.mp3"
        obj.save(fileAddress)
        os.system("start "+fileAddress + " tempo 1.9")
    print("play ->"+ langSelected + "->" + fileAddress)


def resetButtonEvent():
    global text
    global fileText
    global isfileSelected
    global fileName
    # code for reset button
    key = messagebox.askokcancel("Reset","You will lose all text.", icon= "error")
    if key:
        textInput.delete("1.0", END)
        text = ""
        fileName = ""
        fileText = ""
        isfileSelected = ""
        fileLabel.configure(text="")
        addFileButton.configure(background="#eceff1", foreground="#000000", text="Add File")
        
    print("reset")

def colorBackground(key):
    if key:
        return "#455a64"
    else:
        return "#eceff1"

## Buttons Frame(folder)
# make frame
buttonFrame = Frame(root, background="#fff")
# place it
buttonFrame.grid(column=1,row=1,padx=20,pady=20,sticky= "w")
# make add file button
addFileButton = Button(buttonFrame,text="Add File", font= ("Helvetica", 10), background="#eceff1", borderwidth=1, bd=0,padx=16,pady=4, command= addFileButtonEvent)
# place it
addFileButton.grid(column=0,row=0,padx=20,pady=0,sticky= "w")
# make reset button
resetButton = Button(buttonFrame,text="Reset", font= ("Helvetica", 10), background="#eceff1", borderwidth=1, bd=0,padx=16,pady=4, command= resetButtonEvent)
# place it
resetButton.grid(column=1,row=0,padx=20,pady=0,sticky= "w")
# make play button
playButton = Button(buttonFrame,text="Play", font= ("Arial Bold", 10),foreground="#fff", background="#455a64",highlightbackground="#90a4ae", borderwidth=1, bd=0,padx=16,pady=4, command= playButtonEvent)
# place it
playButton.grid(column=2,row=0,padx=20,pady=0,sticky= "w")
# make text label
fileLabel = Label(root, text = "", font= ("Helvetica", 9), background="#fff", foreground="#90a4ae")
# place it
fileLabel.grid(column=1,row=3,padx=40,pady=0,sticky= "w")


# application is ready to run
root.mainloop()