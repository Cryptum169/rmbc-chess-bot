import os

path = "GameHistory/"

win = []
lose_timeout = []
lose_king = []

for filename in os.listdir(path):
    if filename[-13] == 'u':
        continue
    with open(path + filename) as file:
        result = file.readlines()[-1]
        winner = result[0:5]
        if winner == 'WHITE':
            win.append(filename)
        else:
            reason = result[-8:-1]
            if reason == 'capture':
                lose_king.append(filename)
            else:
                lose_timeout.append(filename)

print("{} matches played, {} Won, {} lose by timeout and {} lose by king capture".format((len(win) + len(lose_timeout) + len(lose_king)), len(win), len(lose_timeout), len(lose_king)))
