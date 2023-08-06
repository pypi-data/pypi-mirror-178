import os

ITEMLIST = []

def test():
    print("Good to go.")

def test2():
    print("Still good to go.")

def get_items():
    global ITEMLIST
    path = os.path.join(os.path.dirname(__file__), "items.txt")

    if os.path.exists(path) and os.path.isfile(path):
        print("path test: true")

        with open(path, "r") as file:
            ITEMLIST = [item.strip() for item in file.readlines()]
    else:
        print("failed")