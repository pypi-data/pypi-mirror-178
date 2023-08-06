import pyfiglet # used for banner
from colorama import Fore as colour, Back as back # used for text functions 
import itertools, threading # used for waiting stuff
from time import sleep as Time # used for waiting...
import sys # used for stdout
import asyncio # used for app class, as well as async functions 
from playsound import playsound # its morbin time
from datetime import datetime # for clock function
from .errors import *
from .colors import *
from .logs import *
import os
from getpass import getpass

DEFAULT_FONT = 'standard' # pyfiglet banner font

class tests():
    def error(text, stripped: bool = True):
        """makes an error print"""
        if stripped == False:
            print(f"❌ details: {text}")
        else:
            print(f"❌ {text}")

    def passed(text, stripped: bool = True):
        """makes a pass print"""
        if stripped == False:
            print(f"✅ details: {text}")
        else:
            print(f"✅ {text}")

def clearscreen():
    """clears the screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def prompt(text = "press enter to continue...", color = terminal,*, background = back_terminal):
    """creates a no-input continue prompt."""
    value = getpass(prompt = f"{background} {color} {text} {terminal} {back_terminal}")
    if value == "":
        return
    else:
        print("No input required!")
        prompt(color, text=text)

def banner(text = "CopperHead", color = green, *, font=DEFAULT_FONT, background = back_terminal, end="\n"):
    """creates a banner for your application"""
    banner = pyfiglet.figlet_format(text, font)
    print(background + color + banner)
    print(terminal + back_terminal, end='\n')

def color_print(text, color, background = back_terminal):
    """makes colored text"""
    print(background + color + text + white + back_terminal)

def loading(text = "loading...", color=terminal, time=1, background = back_terminal):
    """makes a little loading icon next to your inputed text, for however long you'd like it to wait."""
    done = False
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write(background + color + f'\r{text} ' + c)
            sys.stdout.flush()
            Time(0.1)
        sys.stdout.write(color + '\rDone!')

    t = threading.Thread(target=animate)
    t.daemon=True   # allows program to be stopped upon KeyboardInterrupt
    t.start()
    Time(int(time))
    done = True
    print(terminal + back_terminal + "\ndone")

def rainbow_print(text="colors", time=5):
    """prints with **flare**"""
    done = False
    def animate():
        for c in itertools.cycle([f"{red+text}", f"{yellow+text}", f"{green+text}", f"{blue+text}", f"{magenta+text}", f"{black+text}"]):
            if done:
                break
            sys.stdout.write(f'\r'+c)
            sys.stdout.flush()
            Time(0.1)

    t = threading.Thread(target=animate)
    t.daemon=True   # allows program to be stopped upon KeyboardInterrupt
    t.start()
    Time(int(time))
    done = True
    print(terminal + back_terminal +"\r")

def clock(format=24, color = terminal, background = back_terminal):
    """creates a clock
    args:
        format: this decides if you want to print with the 12 or 24 hour time format
    """
    if format == 24:
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            sys.stdout.write(str(background + color + current_time) + '\r')
            sys.stdout.flush()
    if format == 12:
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            hours, minutes = current_time.split(':')
            hours = int(hours); minutes = int(minutes)
            if hours > 12:
                sys.stdout.write(background + color + f"{hours-12}:{minutes}" + '\r')
                sys.stdout.flush()
    else:
        raise ArgumentError("you must use either the 12 or 24 hour time formats.")

class CopperApp():
    """App organization functions"""
    def run(func, persistent: bool = False, startsound: str = None):
        """Runs the app. this has the benefit of cleaning up app structuring, such as exiting cleanly with KeyboardInterupt
        runs with asyncio. for single eventloop apps, use start.
        if you use run, make sure to define with async. otherwise, use start. 
        if you dont need async, start is probably your best option.
        Args:
            func: this is where your main menu should be defined. add the menu's function name here. this is what will run upon starting your app
            persistent: this is a true/false arg. this decides if your app will loop.
            startsound: this is where you put the path to a sound file you want to play on startup
        """

        async def run_app() -> None:
            try:
                if persistent == True:
                    while persistent == True:
                        if startsound != None:
                            playsound(startsound)
                        await func()
                else: 
                    if startsound != None:
                        playsound(startsound)
                    await func()
            except KeyboardInterrupt:
                print(back_terminal + terminal +"\nexiting... ")

        asyncio.run(run_app())

    def start(func, persistent: bool = False, startsound: str = None):
        """single eventloop processing for CopperApp processes
        
        *not async*

        Args:
            func: this is where your main menu should be defined. add the menu's function name here. this is what will run upon starting your app
            persistent: this is a true/false arg. this decides if your app will loop.
            startsound: this is where you put the path to a sound file you want to play on startup"""
        try:
            if persistent == True:
                while persistent == True:
                    if startsound != None:
                        playsound(startsound)
                    func()
            else:
                if startsound != None:
                        playsound(startsound)
                func()
                
        except KeyboardInterrupt:
            print(back_terminal + terminal + "\nexiting... ")