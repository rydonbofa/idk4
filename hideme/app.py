
from tkinter import *
import tkinter as tk
import urllib
from tkscrolledframe import ScrolledFrame
import json
import urllib.request
from PIL import Image, ImageTk
import os
import subprocess
from functools import partial



def get_running_services():
    command = """systemctl list-units |grep hide\.me |grep -v "system-hide" |awk '{ print $1" " $4}'"""
    return list(filter(None,subprocess.check_output(command, shell=True).decode("UTF-8").split("\n")))

def read_servers():
    with open(os.path.dirname(os.path.realpath(__file__))+"/Servers.json", "r") as f:
        return json.load(f)["data"]

def get_images():
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/images/"):
        os.mkdir(os.path.dirname(os.path.realpath(__file__))+"/images/")
    for item in read_servers():
        if not os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/images/"+item["image"].split("/")[-1]):
            urllib.request.urlretrieve(item["image"],os.path.dirname(os.path.realpath(__file__))+"/images/"+item["image"].split("/")[-1])

def get_image_dict():
    get_images()
    images = {}
    for file in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/images/"):
        images[file.split(".")[0]] = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__))+"/images/"+file).resize((50,50)))
    return images
def set_background(buttons, highlight_button = None):
    new_bg = "#40ff46"
    new_fg = "#000000"

    default_bg = "#2a2e32"
    default_fg= "#ffffff"

    for b in buttons:
        #print(buttons[1])
        b[0]["activebackground"] = default_bg
        b[0]["bg"] = default_bg
        b[0]["fg"] = default_fg
        b[0]["activeforeground"] = default_fg

    highlight_button["activebackground"] = new_bg
    highlight_button["bg"] = new_bg
    highlight_button["fg"] = new_fg
    highlight_button["activeforeground"] = new_fg
    pass

def button_click(button, adress, buttons):
    running = get_running_services()
    if len(running) > 0:
        if adress.split(".")[0] == running[0].split("@")[1].split(".")[0]:
            stop_service()
            if len(get_running_services()) == 0:
                set_background(buttons)
            return
            
    stop_service()
    
    if len(get_running_services()) > 0:
        print("ERROR")
        return
    name = adress.split(".")[0]
    os.system(f"systemctl start hide.me@{name}")
    if len(get_running_services()) > 0:
        set_background(buttons, button)
    else:
        set_background(buttons)

def stop_service():
    running = get_running_services()
    if len(running) < 1:
        return
    print(f"Killing old process: {running}")
    name = running[0].split(" ")[0]
    os.system(f"systemctl stop {name}")

def initialize_background(buttons):
    services = get_running_services()
    if len(services) < 1:
        return
    name = services[0].split("@")[1].split(".")[0]
    for b in buttons:
        if b[1].split(".")[0] == name:
            set_background(buttons, b[0])
    print(name)

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 800
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#000000", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


root = Tk()


root.title("Hide.Me VPN Manager")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

sf = ScrolledFrame(root, width=640, height=480)
sf.pack(side="top", expand=1, fill="both")

sf.bind_arrow_keys(root)
sf.bind_scroll_wheel(root)

inner_frame = sf.display_widget(Frame)

max_cols = 4

images = get_image_dict()
buttons = []
for i,item in enumerate(read_servers()):
    button = Button(inner_frame,
                width=600,
                height=200,
                borderwidth=2,
                #relief="groove",
                anchor="center",
                justify="center",
                text=(item["Name"]),
                image = images[item["image"].split("/")[-1].split(".")[0]], compound="left",
                )
    button.grid(
            row=int(i/max_cols)+1,
            column=i%max_cols,
            padx=8,
            pady=16)
    button["command"] = partial(button_click,button,item["adress"], buttons)

    button_tooltip = CreateToolTip(button, item["adress"])
    buttons.append((button, item["adress"]))


initialize_background(buttons)
root.mainloop()




