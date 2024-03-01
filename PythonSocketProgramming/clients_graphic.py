#import libraries to create socket, gui, threads and error handling
import socket
import errno
import sys
import threading
import tkinter as ui

#creating the ui
window = ui.Tk()
window.title("Whats Up Doc")

Button_Colour = "#8B8B45"
BG_Colour = "#FFFFE4"
Text_Colour = "#8F8FBC"
 
Font = ("Times New Roman", 16)
Font_Bold = ("Times New Roman", 14, "bold")

text = ui.Text(window, bg=BG_Colour, fg=Text_Colour, font=Font, width=60)
text.grid(row=0, column=0, columnspan=2)
text.config(state=ui.DISABLED)

enter = ui.Entry(window, bg="#FFFFD7", fg=Text_Colour, font=Font, width=55)
enter.grid(row=1, column=0)

#creating a function to receive messages
def receiving():
    while True:
        try:
                usrname_hdr = client_socket.recv(HEADERL)
                if not len(usrname_hdr):
                    print("Connection closed by server")
                    sys.exit()
                usrname_len = int(usrname_hdr.decode("utf-8").strip())
                usrname = client_socket.recv(usrname_len).decode("utf-8")

                msg_hdr = client_socket.recv(HEADERL)
                msg_len = int(msg_hdr.decode("utf-8").strip())
                message = client_socket.recv(msg_len).decode("utf-8")

                text.config(state=ui.NORMAL)
                text.insert(ui.END, usrname + '->' + message + '\n')
                text.config(state=ui.DISABLED)
                text.see(ui.END)
        
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
            continue
        
        except Exception as e:
            print('General error',str(e))
            sys.exit()



#creating function to send messages
def sending(event=None):
 message = enter.get()
 if message:
         message = message.encode("utf-8")
         msg_hdr = f"{len(message):<{HEADERL}}".encode("utf-8")
         client_socket.send(msg_hdr + message)
 enter.delete(0, ui.END)


def when_close():
     client_socket.close()
     window.destroy()

#creating socket, header, conditions for app to exist
window.bind('<Return>', sending)
HEADERL = 10

IP = "192.168.53.212"#LAN "192.168.1.105/192.168.53.212" Local "127.0.0.1"WAN "102.132.241.217, 102.65.52.100"
PORT = 1234

my_usrname = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

usrname = my_usrname.encode("utf-8")
usrname_hdr = f"{len(usrname):<{HEADERL}}".encode("utf-8")
client_socket.send(usrname_hdr + usrname)

window.protocol("WM_DELETE_WINDOW", when_close)

thread_to_receive = threading.Thread(target=receiving)
thread_to_receive.start()

window.mainloop()
