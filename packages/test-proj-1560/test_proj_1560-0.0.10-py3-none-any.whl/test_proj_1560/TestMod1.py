import os

ITEMLIST = []

def test():
    print("Good to go.")

def test2():
    print("Still good to go.")

def get_items():
    path = os.path.join(os.path.dirname(__file__), "items.txt")

    if os.path.exists(path) and os.path.isfile(path):
        with open(path, "r") as file:
            global ITEMLIST
            ITEMLIST = [item.strip() for item in file.readlines()]
    else:
        print("failed")