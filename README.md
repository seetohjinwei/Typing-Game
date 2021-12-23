# Typing-Game

How fast can you type?

Requirements:
- Python 3.8 and up
- Tkinter module
- Right click and save as: <a href="https://raw.githubusercontent.com/seetohjinwei/Typing-Game/main/game.py">game.py file</a>

Just run the following command: `python3 game.py`

Notes:

- You can add a number like "python3 game.py 60" to make the games last 60 seconds instead of 30.
- This script will create a file called "scores". Just keeps track of your scores between sessions.
- There is a way to activate cheat mode.

Cheat mode instructions:

1. Right click and save as: <a href="https://raw.githubusercontent.com/seetohjinwei/Typing-Game/main/cheat.py">cheat.py file</a>
2. Make sure "game.py" and "cheat.py" are in the same folder
3. Run "cheat.py" by itself to inject the cheat: `python3 cheat.py`
4. Run with `python3 game.py cheat` when you want to activate cheat mode.
5. If you want to modify the cheat speed, you can edit the interval timing at line 21 of "cheat.py"

List of words pulled from: https://www.mit.edu/~ecprice/wordlist.10000 but filtered for words of length 5 and above.
