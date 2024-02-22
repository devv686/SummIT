from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
import webbrowser
import requests
import json


# create window
window = Tk()
window.title("SummIT Browser")
window.geometry("1000x700")
window.configure(bg="#ffe5b4")
window.iconphoto(False, PhotoImage(file="summitSurfersLogo.png"))

# globals
newURL = ""
flag = False


# make api request
def scrapeLink():
    global newURL

    link.config(text="loading...", fg="black")
    window.update()

    inputURL = textBox.get().strip()

    if len(inputURL) > 8 and (inputURL.startswith("https://") or inputURL.startswith("http://")):
        response = requests.get('https://showcase.zebrarobotics.com/node/api/getHTML', json={"url": inputURL}, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
        newURL = response.json()["resultLink"]
        link.config(text="Your Scraped Link!", fg="blue")
        
    else:
        messagebox.showerror("Error", "Input must be a link (starts with 'http(s)://')")    


def deleteText(e):
    global flag
    if not flag:
        textBox.delete(0, "end")
        flag = True
    

# corners
cornerPic = PhotoImage(file="corner2.png")
corner = Label(image=cornerPic, bg="#ffe5b4")
corner.pack(side=TOP, anchor=NE)

cornerPic2 = PhotoImage(file="corner.png")
corner2 = Label(image=cornerPic2, bg="#ffe5b4")
corner2.pack(side=BOTTOM, anchor=SW)


# create title
title = Label(window, text="SummIT", fg="#6a2e6b", bg="#ffe5b4", font=("Courier", 100, "bold"))
title.pack()
title.place(relx = 0.5, rely=0.35, anchor=CENTER)


# create input box
textBox = Entry(window, width=60, bd=1, relief="solid", bg="white", fg="black", font=("Futura", 17, "bold"))
textBox.insert(0, "Enter full URL here")
textBox.pack()
textBox.place(relx = 0.5, rely=0.5, anchor=CENTER)
textBox.bind("<FocusIn>", deleteText)


# create button
buttonEnter = Button(window, height=1, width=20, borderwidth=0, text="ENTER", bg="#8b328c", font=("Futura", 20, "bold"), command=lambda: scrapeLink())
buttonEnter.bind("<Enter>", lambda e: buttonEnter.config(background="#582659"))
buttonEnter.bind("<Leave>", lambda e: buttonEnter.config(background="#8b328c"))
buttonEnter.pack()
buttonEnter.place(relx = 0.5, rely = 0.6, anchor=CENTER)


# words
words = Label(window, text="Access link will appear here:", fg="#d17b64", bg="#ffe5b4", font=('Lato', 23))
words.pack()
words.place(relx = 0.5, rely = 0.75, anchor=CENTER)


# link
link = Label(window, text="", fg="blue", bg="#ffe5b4", cursor="hand2", font=('Helveticabold', 21))
link.pack()
link.place(relx = 0.5, rely = 0.8, anchor=CENTER)
link.bind("<Button-1>", lambda e: webbrowser.open_new_tab(newURL))


window.mainloop()
