def main() -> None:
    '''
    Responsible for checking for word changes.
    Exits script when the game is closed.
    '''
    prev: str = app.words.curr
    while app.running:
        if prev != app.words.curr:
            prev = app.words.curr
            simulate_type(prev)
    exit()

def simulate_type(word: str) -> None:
    '''
    Simulates typing out the words.
    Calls the game's check word when done "typing".
    '''
    for i, char in enumerate(word):
        app.text_field.insert(i, char)
        sleep(0.05)
        if not app.in_game:
            return
    app.check_word()    

def checks() -> None:
    if not isfile("game.py"):
        print("game.py not found!\nExiting!")
        return
    with open("game.py", "r") as f:
        script: list[str] = f.readlines()
        if any("import cheat" in line for line in script):
            print("Already injected!\nExiting!")
            return
    inject(script)

def inject(lines: list[str]) -> None:
    for i, line in enumerate(lines):
        if "app = " in line:
            lines.insert(i + 1, "        import cheat\n")
            lines.insert(i + 1, "    if len(argv) == 2 and argv[1] == \"cheat\":\n")
            break
    else:
        print("game.py is invalid. Please update.")
        return
    print("Injecting...")
    with open("game.py", "w") as f:
        f.writelines(lines)
    print("Done!")

if __name__ == "__main__":
    '''
    Executes when you run this script as a standalone.
    This will inject the import into the main module.
    '''
    
    from os.path import isfile
    
    checks()

else:
    '''
    Execute when cheat client is being run by the game.
    '''
    
    from __main__ import app
    from threading import Thread
    from time import sleep
    
    # run in separate thread
    print("Cheat Client Activated!")
    Thread(target=main).start()
