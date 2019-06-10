import numpy as np


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
    inter_time = -1.0
    if events[1][1][0] == -2:
        inter_time = get_exp_sample(arrival_rate)
    elif events[1][1][0] == -1:
        inter_time = get_exp_sample(mu)
    if inter_time >= 0.0:
        add_event([ret[0] + inter_time, ret[1]])
    return ret


def get_min():
    return events[1]


def add_event(event):
    events.append(event)
    BU(len(events))  # todo check if it's true (because events list starts from 1)


def arrive(event):
    if event[1][0] == -2:
        dead_line = get_exp_sample(1 / alpha)
        if np.random.randint(0, 10) > 0:
            timer_queue[1].append(event[0] + dead_line)
        else:
            timer_queue[0].append(event[0] + dead_line)


def execute(now, server_idx):
    # it's guaranteed that there is an event to be added to a core of this server
    for i in range(len(cores[server_idx])):
        if not core_is_busy[server_idx][i]:
            serve_time = get_exp_sample(cores[server_idx][i])
            events.append([now + serve_time, [server_idx, i]])
            return


def server_queue_length(queues):
    return len(queues[0]) + len(queues[1])


def timer_pass(event):
    queues_length = list(map(server_queue_length, cores_queue))
    min_length = min(queues_length)
    tmp_idxs = list()
    for i in range(len(queues_length)):
        if min_length == queues_length[i]:
            tmp_idxs.append(i)
    rand_num = np.random.randint(0, len(tmp_idxs))
    idx = tmp_idxs[rand_num]
    if server_queue_length(cores_queue[idx]) == 0:
        for is_busy in core_is_busy[idx]:
            if not is_busy:
                execute(event[0], idx)
                return
    if len(timer_queue[0]) == 0 and len(timer_queue[1]) == 0:
        return
    if len(timer_queue[0]):
        res = timer_queue[0].pop(0)
        cores_queue[idx][0].append(res)
    else:
        res = timer_queue[1].pop(0)
        cores_queue[idx][1].append(res)


def core_clock(event):
    core_is_busy[event[1][0]][event[1][1]] = False
    if len(cores_queue[event[1][0]][0]) > 0:
        cores_queue[event[1][0]][0].pop(0)
        execute(event[1][0])
    elif len(cores_queue[event[1][0]][1]) > 0:
        cores_queue[event[1][0]][1].pop(0)
        execute(event[1][0])


def handle_expired_tasks(time):
    expired_tasks = []
    for i in range(2):
        j = 0
        while j < len(timer_queue[i]):
            if timer_queue[i][j] < time:
                expired_tasks.append([-1, i, j])
            j += 1
        for k in range(M):
            j = 0
            while j < len(cores_queue[k][i]):
                if cores_queue[k][i][j] < time:
                    expired_tasks.append([k, i, j])
                j += 1
    expired_tasks = sorted(expired_tasks, key=lambda tup: tup[2])
    # print(timer_queue)
    timer_idx = [0, 0]
    server_idxs = [[[0, 0]] * M]
    # print(server_idxs)
    for i in range(len(expired_tasks)):
        if expired_tasks[i][0] == -1:
            timer_queue[expired_tasks[i][1]].pop(expired_tasks[i][2] - timer_idx[expired_tasks[i][1]])
            timer_idx[expired_tasks[i][1]] += 1
        else:
            cores_queue[expired_tasks[i][0]][expired_tasks[i][1]].remove(
                expired_tasks[i][2] - server_idxs[expired_tasks[i][0]][expired_tasks[i][1]])
            server_idxs[expired_tasks[i][0]][expired_tasks[i][1]] += 1


if __name__ == '__main__':
    file = open('config.txt', 'r')

    M, arrival_rate, alpha, mu = file.readline()[:-1].split(" ")
    M = int(M)
    arrival_rate = float(arrival_rate)
    alpha = float(alpha)
    mu = float(mu)

    timer_queue = [[], []]
    cores_queue = []

    cores = []
    core_is_busy = []

    # quality properties
    service_time = []
    queue_time = []
    num_of_expired_tasks = []
    average_timer_queue_len = 0
    average_servers_queue_len = [0] * M
    task_needed_service_time = 0
    task_needed_queue_time = 0
    task_needed_expired_average = 0
    task_needed_average_timer_queue_len = 0
    task_needed_average_servers_queue_len = [0] * M
    served_users = 0
    intered_users = 0
    limit = 50000000

    for i in range(M):
        cores.append([])
        core_is_busy.append([])
        cores_queue.append([[], []])
        temp = file.readline()[:-1].split(" ")
        temp2 = temp[1:]
        core_is_busy[i] = [False] * int(temp[0])
        for j in range(int(temp[0])):
            cores[i].append(float(temp2[j]))

    events = [[0, [-3, 0]]]
    events.append([get_exp_sample(arrival_rate), [-2, 0]])  # arrival event specified by -2
    events.append([get_exp_sample(mu), [-1, 0]])  # timer job specified by -1

    # make heap
    for i in range(len(events) - 1, 0, -1):
        BD(i)

    while served_users < 50000000:
        e = remove_min()
        handle_expired_tasks(e[0])
        if e[1][0] == -2:
            arrive(e)
        elif e[1][0] == -1:
            timer_pass(e)
        else:
            core_clock(e)
