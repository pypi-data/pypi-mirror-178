import os

def filePath(fileName):
    return f"./{fileName}"

def display():
    print('1. Puzzle 2. bfs 3. A star')
    choice = int(input())

    if choice == 1:
        with open(filePath('puzzle.py')) as f:
            print("===================Puzzle====================")
            for line in f:
                print(line, end='')
    elif choice == 2:
        with open(filePath('bfs.py')) as f:
            print("===================BFS====================")
            for line in f:
                print(line, end='')
    elif choice == 3:
        with open(filePath('A_star.py')) as f:
            print("===================A Star====================")
            for line in f:
                print(line, end='')
    else:
        print("wrong choice")