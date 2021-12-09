from tkinter import *
# from mttkinter import *
from tkinter import messagebox
import time
from pygame import mixer
import threading
from chat_utils import *
from chat_client_class import *
from client_state_machine import *
import json
import argparse
import os
import pickle
import random
import runpy

parser = argparse.ArgumentParser(description='chat client argument')
parser.add_argument('-d', type=str, default=None, help='server IP addr')
args = parser.parse_args()

client = Client(args) 
client.init_chat()
print(client.socket)


window = Tk()
window.title('Login Page')
screenWidth = window.winfo_screenwidth() - 200 #get the width of the screen
screenHeight = window.winfo_screenheight() - 100 #get the height of the screen
window.geometry('%dx%d'%(screenWidth,screenHeight)) #set the size of the window
window.resizable(False, False)


canvas = Canvas(window, height=screenHeight, width=screenWidth, bg="white")
loginBackground = PhotoImage(file='cat.png') #load the image
canvas.create_image(0,0, anchor='nw', image=loginBackground)
canvas.pack(side='top')
Label(window, text='Meow! Welcome to ICS Chat System!',font=('Calibri',40), bg="white").place(x=580, y= 120)
Label(window, text='Login Page🐱',font=('Calibri',36), bg="white").place(x=40, y= 40)
Label(window, text='Already have an account? ', font=('Calibri',20), bg="lemonchiffon").place(x=790, y= 215)
Label(window, text='Enter your user name🐈: ',font=('Calibri',20), bg="white").place(x=790, y= 260)
inputUserName = StringVar()
inputUserName.set('')
entryUserName = Entry(window, textvariable=inputUserName, width=35,bg="white").place(x=790, y=290)
Label(window, text='Enter your password🐈: ',font=("Calibri",20), bg="white").place(x=790, y= 320)
inputUserPwd = StringVar()
entryUserPwd = Entry(window, textvariable=inputUserPwd, width=35,show='*',bg="white").place(x=790, y=350)
usrName=''
Label(window, text='New User? ',font=('Calibri',20), bg="lemonchiffon").place(x=790, y= 480)
def usrLogin():
    global usrName
    usrName = inputUserName.get()
    usrPwd = inputUserPwd.get()
    try:
        with open('usrs_info.pickle', 'rb') as usrFile:
            usrsInfo = pickle.load(usrFile)   
    except FileNotFoundError: #if file doesn't exist yet, create a new file
        with open('usrs_info.pickle', 'wb') as usrFile:
            usrsInfo = {'admin': 'admin'}
            pickle.dump(usrsInfo, usrFile)    
    if usrName in usrsInfo:
        if usrPwd == usrsInfo[usrName]:
            messagebox.showinfo('Successfully Login!', 'Welcome to the chat system ' + usrName+'! Have a good time!') 
            client.login(usrName)
            startChatting()
        else:
            messagebox.showinfo('Meow!','Wrong Password!')
    else:
        signedUpAlready = messagebox.askyesno('Meow!',"Oops, seems like you don't haven an account yet! Please sign up below first.")
        if signedUpAlready:
            usrSignUp()
    
def usrSignUp():
    def signUp():
        password = newPassword.get()
        passwordConfirm = newPasswordConfirm.get()
        name = signName.get()
        with open('usrs_info.pickle', 'rb') as usrFile:
            userlist = pickle.load(usrFile)
        if password != passwordConfirm:
            messagebox.showerror('Meow!', 'Passwords do not match! Please try again!')
        elif name in userlist:
            messagebox.showerror('Meow!', 'You have signed up! Please login with your username.')
        elif name == "":
            messagebox.showerror('Meow!', "Forget to enter your name?")
        elif password == "":
            messagebox.showerror('Meow!', "Forget to enter your password?")
        else:
            userlist[name] = password
            with open('usrs_info.pickle', 'wb') as usrFile:
                pickle.dump(userlist, usrFile)
            messagebox.showinfo('Hi!', 'You have successfully signed up!')
            signUpWindow.destroy()
            
    signUpWindow = Toplevel(window) #pop up the sign up window on the top
    signUpWindow.title('Sign up')
    canvas = Canvas(signUpWindow, height=screenHeight, width=screenWidth, bg = 'white')
    canvas.create_image(0,0, anchor='nw', image=loginBackground)
    canvas.pack(side='top')
    signUpWindow.geometry('%dx%d'%(screenWidth,screenHeight))
    signUpWindow.resizable(False, False)

    Label(signUpWindow, text='Create a new account: ',font=('Calibri',28), bg="white").place(x=920, y= 150)
   
    Label(signUpWindow, text='Please enter your user name🐈: ',font=('Calibri',20), bg="white").place(x=790, y= 230)
    Label(signUpWindow, text='Please enter your password🐈: ',font=("Calibri",20), bg="white").place(x=790, y= 330)
    Label(signUpWindow, text='Please confirm your password🐈: ',font=("Calibri",20), bg="white").place(x=790, y= 430)

    signName = StringVar()
    entrySignName = Entry(signUpWindow, textvariable=signName ,width=35,bg="white").place(x=790, y=270)
    newPassword = StringVar()
    entryUserPwd = Entry(signUpWindow, textvariable=newPassword, width=35,show='*',bg="white").place(x=790, y=370)
    newPasswordConfirm = StringVar()
    entryUserPwdConfirm = Entry(signUpWindow, textvariable=newPasswordConfirm, width=35,show='*',bg="white").place(x=790, y=470)

    signUpBtn2 = Button(signUpWindow, text='Ready!', command=signUp,width=13, relief=FLAT, borderwidth=0).place(x=790, y=520)

loginBtn = Button(window, text='Login', command=usrLogin, width=13, bd=0).place(x=885, y=400)
# loginBtn = Button(window, text='Login', command=usrLogin, borderwidth=0, width=10)
signUpBtn = Button(window, text='Sign up', command=usrSignUp,width=13, relief=FLAT, borderwidth=0).place(x=885, y=515)

def startChatting():
    window.destroy()
    def msgsend():
        msg = ' Me '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
        messageList.configure(state='normal')
        messageList.insert(END,msg,'myMessage') 
        messageList.insert(END,txt_msgsend.get('0.0',END))
        m = txt_msgsend.get('0.0',END).strip()
        txt_msgsend.delete('0.0',END) 
        messageList.configure(state='disabled')
        messageList.see(END)
        client.proc()
        client.console_input.append(m)            
            
    def clear():
        txt_msgsend.delete('0.0',END) 
 
    def msgsendEvent(event):
        if event.keysym == 'Return':
            msgsend()
            x=threading.Thread(target=after_return)
            x.start()
            
    def after_return():
        time.sleep(0.01)
        clear()

    def quit():
        client.quit()
        client.state = S_OFFLINE
        chatWindow.destroy()

    def who():
        client.console_input.append('who')
    
    def disconnect():
        client.console_input.append('bye')
 

    def connectTo(self):
        connectToWhom =  whoListBox.get(whoListBox.curselection())
        print("double click")
        print(connectToWhom)
        if connectToWhom != client.name:
            client.console_input.append('c ' + connectToWhom)

        if client.sm.get_state() == S_CHATTING:
            client.console_input.append('bye')
            client.console_input.append('c ' + connectToWhom)


    def X():
        runpy.run_path(path_name='playerx.py')

        

    def music():
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.play()
    
    def O():
        print('game')
        runpy.run_path(path_name='player0.py')
    def stop():
        mixer.music.pause()
    def getWhoOnline():
        client.console_input.append("who")      
        print("getWhoOnline "+client.sm.whoOnLine)   
        whoOnlineList = client.sm.whoOnLine

        whoOnlineList = whoOnlineList.split(',') 
        # print(type(whoOnlineList)) 
        whoOnline.set(whoOnlineList)


    def refresh():
        while True:
            client.proc()
            # getWhoOnline()
            #time.sleep(CHAT_WAIT)
            if client.system_msg != '':
                m = client.system_msg
                # print("m " + m[-3:])
                if m[-3:] != "who":
                    messageList.configure(state='normal')
                    messageList.insert(END,'\n' + client.system_msg + '\n')
                    messageList.configure(state='disabled')
                    messageList.see(END)
                client.system_msg = ''

            # print("refresh")

    #The main window for chatting and game function
    chatWindow = Tk()
    chatWindow.title('Main Page')
    chatWindow.configure(background='white')
    chatWindow.resizable(False, False)
    chatWindow.geometry('%dx%d'%(screenWidth,screenHeight))

    #the background image
    canvas = Canvas(chatWindow, height=screenHeight, width=screenWidth, bg="white")
    chatBackground = PhotoImage(file='sky.png') 
    canvas.create_image(0,0, anchor='nw', image=chatBackground)
    canvas.place(x=0,y=0)
 
    #create different frames (parts) in the window
    messageContainer = Frame(height = 300,width = 500,bg = 'lightblue')  
    chatBox = Frame(height = 50,width = 500,bg = 'lightblue', borderwidth=1)
    bottomButtons = Frame(height = 100,width = 300, bg = 'lightblue')   
    topMenu = Frame(height = 100,width = 500, bg = 'lightblue')  
    leftMenu = Frame(height = 700,width = 50, bg = 'lightblue')
    

    messageList = Text(messageContainer, height = 30, bg = 'white') 
    messageList.configure(state='disabled') 
    messageList.tag_config('myMessage',foreground = 'blue') 
    txt_msgsend = Text(chatBox,height = 10)
    txt_msgsend.bind('<KeyPress-Return>',msgsendEvent) 

    sendBtn = Button(bottomButtons,text = ' Send ',command = msgsend,width = 10,borderwidth=0) 
    clearBtn = Button(bottomButtons,text = ' Clear ',command = clear,width = 10, borderwidth=0)
    whoBtn = Button(topMenu,text = ' Online Users👬 ',command = who,width =10, borderwidth=0)
    DisconnectBtn = Button(topMenu,text = ' Disconnect 🤭 ',command = disconnect,width = 10, borderwidth=0)
    XBtn = Button(topMenu,text = ' Player_X ',command = X,width = 10)
    musicBtn = Button(topMenu,text = ' Music 🎵 ',command = music,width = 10)
    stopBtn = Button(topMenu,text = ' Stop Music 🔇 ',command = stop,width = 10)
    OBtn = Button(topMenu,text = ' Player_O ',command = O,width = 10)
    quitBtn = Button(topMenu,text = ' Quit 👋 ',command = quit,width = 10, borderwidth=0)
    
    
    whoOnline = StringVar()
    Label(leftMenu, text="Here are all online users! Click to chat with:",font=('Calibri',14), bg="white").grid(row=0, column=0)
    whoListBox = Listbox(leftMenu, listvariable=whoOnline)
    whoListBox.bind('<Double-Button-1>', connectTo)

    messageContainer.grid(row = 1,column = 1, padx=10 ) 
    chatBox.grid(row = 2,column = 1) 
    bottomButtons.grid(row = 3,column = 1) 
    topMenu.grid(row = 0,column = 0, columnspan=2, padx=(10,80)) 
    leftMenu.grid(row=1,column = 0, padx=(200,10))
    messageList.grid() 
    txt_msgsend.grid() 
    sendBtn.grid(row = 0,column = 0,sticky = W,padx=10, pady=20)  
    clearBtn.grid(row = 0,column = 1,sticky = W,padx=(300,10), pady=20)
    whoListBox.grid(row=1, column=0, padx=20, pady=20)
    whoBtn.grid(row = 0,column = 0,padx=(200,5),pady=20)
    
    DisconnectBtn.grid(row = 0, column = 1, padx=5, pady=10)
    XBtn.grid(row = 0,column = 4,sticky = W,padx=5,pady=10)
    musicBtn.grid(row=0,column=2,padx=5, pady=10)
    stopBtn.grid(row=0,column=3,padx=5, pady=10)
    OBtn.grid(row = 0,column = 5,padx=5,pady=10)
    quitBtn.grid(row = 0,column = 6,padx=5,pady=10)

    messageList.configure(state='normal')
    messageList.insert(END,menu)
    client.system_msg = ''
    messageList.configure(state='disabled')
     
    #code from chat_client_class
    reading_thread = threading.Thread(target = refresh)
    reading_thread.daemon = True
    reading_thread.start()
    
    def online_update(): #update
        if client.sm.get_state() != S_OFFLINE:
            onlinedict=client.sm.whoOnLine
            # print(onlinedict)
            # onlinedict = onlinedict.split(",")

        else:
            onlinedict = {}
        whoOnline.set(list(onlinedict))
        whoListBox.after(1000, online_update)

    online_update()

    # def set_interval(func, sec):
    #     def func_wrapper():
    #         set_interval(func, sec)
    #         func()
    #     t = threading.Timer(sec, func_wrapper)
    #     t.daemon = True
    #     t.start()
    #     return t

    # def getWhoOnline():
    #     client.console_input.append("who_list")      
    #     print("getWhoOnline "+client.sm.whoOnLine)   
    #     whoOnlineList = client.sm.whoOnLine
    #     whoOnlineList = whoOnlineList.split(',') 
    #     # print(type(whoOnlineList)) 
    #     whoOnline.set(whoOnlineList)

    # set_interval(getWhoOnline, 2)

    chatWindow.mainloop()

mainloop()


