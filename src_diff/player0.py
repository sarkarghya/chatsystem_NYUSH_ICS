import socket
from tkinter import messagebox, Tk, Label, Button
from _thread import start_new_thread

host = "127.0.0.1"
port = 8080

second_player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
second_player_socket.connect((host, port))

window = Tk()
window.title("Tic Tac Toe: Second Player")
window.geometry("460x200")
label = Label(window, text="  ", font=("sans-serif", 20))
label.grid(row=0, column=0)
label = Label(window, text="Tic-Tac-Toe Game", font=("sans-serif", 20))
label.grid(row=0, column=1)

firstLabel = Label(window, text="Player1: X", font=("sans-serif", 15))
firstLabel.grid(row=2, column=1)

secondLabel = Label(window, text="Player2: O", font=("sans-serif", 15))
secondLabel.grid(row=3, column=1)
turn = True


def firstClick():
    global turn
    if turn == True and firstBtn["text"] == " ":
        firstBtn["text"] = 'O'
        value = '1'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


firstBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                  height=2, font=("sans-serif", 10), command=firstClick)
firstBtn.grid(row=1, column=6)


def secondClick():
    global turn
    if turn == True and secondBtn["text"] == " ":
        secondBtn["text"] = 'O'
        value = '2'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


secondBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                   height=2, font=("sans-serif", 10), command=secondClick)
secondBtn.grid(row=1, column=7)


def thirdClick():
    global turn
    if turn == True and thirdBtn["text"] == " ":
        thirdBtn["text"] = 'O'
        value = '3'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


thirdBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                  height=2, font=("sans-serif", 10), command=thirdClick)
thirdBtn.grid(row=1, column=8)


def fourthClick():
    global turn
    if turn == True and fourthBtn["text"] == " ":
        fourthBtn["text"] = 'O'
        value = '4'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


fourthBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                   height=2, font=("sans-serif", 10), command=fourthClick)
fourthBtn.grid(row=2, column=6)


def fifthClick():
    global turn
    if turn == True and fifthBtn["text"] == " ":
        fifthBtn["text"] = 'O'
        value = '5'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


fifthBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                  height=2, font=("sans-serif", 10), command=fifthClick)
fifthBtn.grid(row=2, column=7)


def sixthClick():
    global turn
    if turn == True and sixthBtn["text"] == " ":
        sixthBtn["text"] = 'O'
        value = '6'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


sixthBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                  height=2, font=("sans-serif", 10), command=sixthClick)
sixthBtn.grid(row=2, column=8)


def seventhClick():
    global turn
    if turn == True and seventhBtn["text"] == " ":
        seventhBtn["text"] = 'O'
        value = '7'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


seventhBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                    height=2, font=("sans-serif", 10), command=seventhClick)
seventhBtn.grid(row=3, column=6)


def eighthClick():
    global turn
    if turn == True and eighthBtn["text"] == " ":
        eighthBtn["text"] = 'O'
        value = '8'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


eighthBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                   height=2, font=("sans-serif", 10), command=eighthClick)
eighthBtn.grid(row=3, column=7)


def ninthClick():
    global turn
    if turn == True and ninthBtn["text"] == " ":
        ninthBtn["text"] = 'O'
        value = '9'
        second_player_socket.send(value.encode('utf-8'))
        turn = False
        check()


ninthBtn = Button(window, text=" ", bg="blue", fg="red", width=5,
                  height=2, font=("sans-serif", 10), command=ninthClick)
ninthBtn.grid(row=3, column=8)

flag = 1


def check():
    global flag
    b1 = firstBtn["text"]
    b2 = secondBtn["text"]
    b3 = thirdBtn["text"]
    b4 = fourthBtn["text"]
    b5 = fifthBtn["text"]
    b6 = sixthBtn["text"]
    b7 = seventhBtn["text"]
    b8 = eighthBtn["text"]
    b9 = ninthBtn["text"]

    flag = flag + 1
    winner = 0

    if ((b1 == b2 and b2 == b3 and b1 == 'O') or (b1 == b2 and b2 == b3 and b1 == 'X')):
        winner = 1
        win(b1)
    elif ((b4 == b5 and b5 == b6 and b4 == 'O') or (b4 == b5 and b5 == b6 and b4 == 'X')):
        winner = 1
        win(b4)
    elif ((b7 == b8 and b8 == b9 and b7 == 'O') or (b7 == b8 and b8 == b9 and b7 == 'X')):
        winner = 1
        win(b7)
    elif ((b1 == b4 and b4 == b7 and b1 == 'O') or (b1 == b4 and b4 == b7 and b1 == 'X')):
        winner = 1
        win(b1)
    elif ((b2 == b5 and b5 == b8 and b2 == 'O') or (b2 == b5 and b5 == b8 and b2 == 'X')):
        winner = 1
        win(b2)
    elif ((b3 == b6 and b6 == b9 and b3 == 'O') or (b3 == b6 and b6 == b9 and b3 == 'X')):
        winner = 1
        win(b3)
    elif ((b1 == b5 and b5 == b9 and b1 == 'O') or (b1 == b5 and b5 == b9 and b1 == 'X')):
        winner = 1
        win(b1)
    elif ((b3 == b5 and b5 == b7 and b3 == 'O') or (b3 == b5 and b5 == b7 and b3 == 'X')):
        winner = 1
        win(b3)

    if flag == 10 and winner != 1:
        messagebox.showinfo("Dead End!!", "no one can win now.")
        window.destroy()


def win(player):
    if player == 'X':
        playerNumber = 1
    else:
        playerNumber = 2
    messagebox.showinfo(f"CONGRATULATIONS", f"PLAYER{player}' have won the game!!")
    window.destroy()


def receive_thread(client):
    global turn
    while True:
        message = client.recv(2048).decode('utf-8')
        if message == '1' and firstBtn["text"] == " ":
            firstBtn["text"] = 'X'
            turn = True
        elif message == '2' and secondBtn["text"] == " ":
            secondBtn["text"] = 'X'
            turn = True
        elif message == '3' and thirdBtn["text"] == " ":
            thirdBtn["text"] = 'X'
            turn = True
        elif message == '4' and fourthBtn["text"] == " ":
            fourthBtn["text"] = 'X'
            turn = True
        elif message == '5' and fifthBtn["text"] == " ":
            fifthBtn["text"] = 'X'
            turn = True
        elif message == '6' and sixthBtn["text"] == " ":
            sixthBtn["text"] = 'X'
            turn = True
        elif message == '7' and seventhBtn["text"] == " ":
            seventhBtn["text"] = 'X'
            turn = True
        elif message == '8' and eighthBtn["text"] == " ":
            eighthBtn["text"] = 'X'
            turn = True
        elif message == '9' and ninthBtn["text"] == " ":
            ninthBtn["text"] = 'X'
            turn = True
        check()


start_new_thread(receive_thread, (second_player_socket,))
window.mainloop()