import fileinput
import os

lol = "lol"

xd = "xd"

# for line in fileinput.input("test.txt", inplace=True):
#     if line == lol:
#         print('{}'.format(xd), end='')
#     else:
#         print('{}'.format(line), end='')

with fileinput.input("test.txt", inplace=True) as f:
    for line in f:
        if line == lol:
            print('{}'.format(xd), end='')
        else:
            print('{}'.format(line), end='')