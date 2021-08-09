'''
Built by See Toh Jin Wei
Available at https://github.com/seetohjinwei/Typing-Game
'''

from os.path import isfile
from queue import PriorityQueue
import random
import re
import requests
from sys import argv, exit
from threading import Thread
from time import sleep
import tkinter as tk
from typing import Union

WIDTH: int = 500
HEIGHT: int = 200
if len(argv) == 2 and re.match(r"^\d+$", argv[1]):
    TIME: int = int(argv[1])
else:
    TIME: int = 30

class Scores():
    '''
    Keep track of scores and highscore.
    '''
    
    def __init__(self) -> None:
        '''
        Initialises Scores Class.
        Uses PriorityQueue from queue module.
        Reads scores from scores file (creates one if not there).
        '''
        self.scores: PriorityQueue[int] = PriorityQueue()
        
        if not isfile("scores"):
            f = open("scores", "x")
            f.close()
        
        with open("scores", "r") as f:
            data: str = f.read()
            for value in data.split("\n"):
                if value:
                    self.scores.put(-int(value))
        
        self.highscore: int = -self.scores.queue[0] if self.scores.queue else 0
        print("Scores:", self.scores.queue)
    
    def insert(self, value: int) -> None:
        '''
        Function to add values into the queue.
        Updates highscore.
        Updates score.
        '''
        if not value:
            return
        self.scores.put(-value)
        self.highscore = -self.scores.queue[0]
        line: str = f"{value}\n"
        with open("scores", "a") as f:
            f.write(line)


class Words():
    
    def __init__(self) -> None:
        '''
        Initialises Words Class.
        Calls the url to get a list of words for choosing.
        '''
        url: str = "https://www.mit.edu/~ecprice/wordlist.10000"
        response: requests.Response = requests.get(url)
        self.WORDS = response.content.splitlines()
        self.curr: str = None
        self.next()

    def next(self) -> None:
        '''
        Changes self.curr
        '''
        word: str = ""
        while len(word) < 5:
            bytestring: bytes = random.choice(self.WORDS)
            word = bytestring.decode("utf-8")
        self.curr = word


class App(tk.Frame):
    
    def __init__(self, master) -> None:
        '''
        Initialises App Class.
        Sets up the various instance variables for the game.
        '''
        super().__init__(master)
        self.scores: Scores = Scores()
        self.words: Words = Words()
        self.in_game: bool = False
        self.running: bool = True
        self.score: int = None
        
        # GUI
        high_score_message: str = f"High Score: {self.scores.highscore}"
        self.high_score = tk.Message(text=high_score_message, width=WIDTH)
        self.high_score.pack()
        self.curr_score = tk.Message(text=None, width=WIDTH)
        self.curr_score.pack()
        self.messageDisplay = tk.Message(text="Get Ready!", width=WIDTH)
        self.messageDisplay.pack()
        self.timeDisplay = tk.Message(text=None, width=WIDTH)
        self.timeDisplay.pack()
        self.wordDisplay = tk.Message(text=None, width=WIDTH)
        self.wordDisplay.pack()
        self.buttonStart = tk.Button(text="Start!", command=self.start_game)
        self.buttonStart.pack()
        self.text_field = tk.Entry(width=20)
        self.text_field.pack()
    
    def start_game(self) -> None:
        '''
        Called when start button is pressed.
        Starts the game and updates the displays accordingly.
        Starts the timer.
        '''
        if self.in_game:
            self.end_game()
            return
        self.in_game = True
        self.score = 0
        self.words.next()
        
        self.display(self.curr_score, "Current Score: 0")
        self.display(self.buttonStart, "Stop!")
        self.display(self.messageDisplay, "Good luck!")
        self.display(self.wordDisplay, self.words.curr)
        self.text_field.delete(0, "end")
        self.text_field.focus()
        
        # called in a separate thread so that the app doesn't freeze!
        Thread(target=self.timer).start()
    
    def timer(self) -> None:
        '''
        Called when the game starts.
        Timer function.
        Responsible for updating the on-screen timer.
        Calls the end_game function when the time is up.
        '''
        for x in range(1, TIME + 1):
            message: str = f"{TIME - x}s"
            self.display(self.timeDisplay, message)
            sleep(1)
            if not self.in_game:
                exit()
        self.end_game()
        
    def end_game(self) -> None:
        '''
        Called when the timer is up.
        Ends the game and updates the score and displays accordingly.
        '''
        self.in_game = False
        self.scores.insert(self.score)
        self.display(self.buttonStart, "Start!")
        self.display(self.messageDisplay, "Time's up!")
        self.display(self.wordDisplay, "")
        self.display(self.high_score, f"High Score: {self.scores.highscore}")
    
    def check_word(self) -> None:
        '''
        Called when Enter/Return is pressed.
        Checks if user typed the word correctly.
        If correct, move on to the next word.
        Else, do nothing.
        '''
        if not self.in_game:
            return
        user_input: str = self.text_field.get()
        print(user_input, correct := user_input == self.words.curr)
        if correct:
            self.score += 1
            self.text_field.delete(0, "end")
            self.words.next()
            self.display(self.curr_score, f"Current Score: {self.score}")
            self.display(self.wordDisplay, self.words.curr)

    def display(self, Message: Union[tk.Message, tk.Button], message: str) -> None:
        '''
        Updates display messages for various tkinter elements.
        '''
        Message.configure(text=message)


def main(window: tk.Tk, app: App) -> None:
    '''
    Main Function
    '''
    def key_pressed(press: tk.Event) -> None:
        '''
        Calls check_word when Return/Enter is pressed.
        '''
        value: str = press.keysym
        if value == "Return" or value == "KP_Enter":
            app.check_word()
    
    def window_closed() -> None:
        '''
        Intercepts when the window is closed.
        Sets in_game = False to allow the timer Thread to exit.
        This is to prevent RuntimeError.
        '''
        app.in_game = False  # exit timer safely
        app.running = False  # exit cheat safely
        print("Shutting down...")
        exit()
    
    window.bind("<Key>", key_pressed)
    window.protocol("WM_DELETE_WINDOW", window_closed)
    
    window.mainloop()

if __name__ == "__main__":
    print("... booting up")
    window = tk.Tk()
    window.title("Typing Game")
    # geometry can be used to set width and height of the window.
    # window.geometry(f"{WIDTH}x{HEIGHT}")
    app = App(window)
    main(window, app)
