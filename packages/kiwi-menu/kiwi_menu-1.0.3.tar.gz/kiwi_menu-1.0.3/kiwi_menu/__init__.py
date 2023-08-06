import keyboard
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Menu:
    def __init__(self, title:str, items:list, color="\033[1;32;40m", symbol:str=">", pre_selected:int=0, centered_texts:list=None):
        self.selected = pre_selected
        self.title = title
        self.items = items
        self.symbol = symbol
        self.color = color
        self.centered_texts = centered_texts

    def prepare(self):
        clear()
        if self.centered_texts != None:
            for i in self.centered_texts:
                print(i.center(os.get_terminal_size().columns, " "))

        print(self.title)
        for i in range(0, len(self.items)):
            print("{1} {0}. {2}".format(i + 1, "{1}{0}".format(self.symbol, self.color) if self.selected == i else " ", self.items[i] + "\x1b[0m"))
        print("\r", end="")

    def up(self):
        if self.selected == 0:
            return
        self.selected -= 1
        self.prepare()

    def down(self):
        if self.selected == len(self.items) - 1:
            return
        self.selected += 1
        self.prepare()

    def show_menu(self):
        self.prepare()
        keyboard.add_hotkey('up', self.up)
        keyboard.add_hotkey('down', self.down)
        keyboard.wait("enter")
        input()
        return self.selected