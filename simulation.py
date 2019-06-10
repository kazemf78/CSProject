import numpy as np

print(np.random.exponential())

file = open('config.txt', 'r')

M, arrival_rate, alpha, mu = file.readline()[:-1].split(" ")
M = int(M)
arrival_rate = float(arrival_rate)
alpha = float(alpha)
mu = float(mu)

cores = []

for i in range(M):
    cores.append([])
    temp = file.readline()[:-1].split(" ")
    temp2 = temp[1:]
    for j in range(int(temp[0])):
        cores[i].append(float(temp2[j]))


def get_exp_sample(rate):
    assert rate != 0.0
    return np.random.exponential(1 / rate)


def BU(idx):
    while idx > 1:
        if events[idx][0] < events[idx // 2][0]:
            events[idx], events[idx // 2] = events[idx // 2], events[idx]
            idx //= 2
        else:
            break


def BD(idx):
    while 2 * idx < len(events):
        arg_min = idx
        if events[2 * idx][0] < events[arg_min][0]:
            arg_min = 2 * idx
        if 2 * idx + 1 < len(events) and events[2 * idx + 1][0] < events[arg_min][0]:
            arg_min = 2 * idx + 1
        if idx == arg_min:
            break
        events[idx], events[arg_min] = events[arg_min], events[idx]
        idx = arg_min


def remove_min():
    ret = events[1]
    events[1], events[-1] = events[-1], events[1]
    events.pop()
    BD(1)
    if events[1][0] == -2:
        inter_time = get_exp_sample(arrival_rate)
    elif events[1][0] == -1:
        inter_time = get_exp_sample(mu)
    else:
        inter_time = get_exp_sample(cores[events[1][0]][events[1][1]])
    events.append([ret[0] + inter_time, ret[1]])
    BU(len(events) - 1)
    return ret


def get_min():
    return events[1]


events = [[0, [-3, 0]]]
events.append([get_exp_sample(arrival_rate), [-2, 0]])  # arrival event specified by -2
events.append([get_exp_sample(mu), [-1, 0]])  # timer job specified by -1
for i in range(M):
    for j in range(len(cores[i])):
        events.append([get_exp_sample(cores[i][j]), [i, j]])

# make heap
for i in range(len(events) - 1, 0, -1):
    BD(i)
