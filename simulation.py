import numpy as np
from math import sqrt


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
    if ret[1][0] == -2:
        inter_time = get_exp_sample(arrival_rate)
    elif ret[1][0] == -1:
        inter_time = get_exp_sample(mu)
    if inter_time >= 0.0:
        add_event([ret[0] + inter_time, ret[1]])
    return ret


def get_min():
    return events[1]


def add_event(event):
    events.append(event)
    BU(len(events) - 1)


def arrive(event):
    if event[1][0] == -2:
        dead_line = get_exp_sample(1 / alpha)
        if np.random.randint(0, 10) > 0:
            timer_queue[1].append([event[0] + dead_line, event[0]])
        else:
            timer_queue[0].append([event[0] + dead_line, event[0]])


def execute(kind, arrive_time, now, server_idx):
    # it's guaranteed that there is an event to be added to a core of this server
    if exited > 5000:
        exit_from_queue_num[kind] += 1
        sum_queue_wait[kind] += now - arrive_time
        square_queue_wait[kind] += (now - arrive_time) ** 2
        check_statistics()
    for i in range(len(cores[server_idx])):
        if not core_is_busy[server_idx][i]:
            serve_time = get_exp_sample(cores[server_idx][i])
            core_task_arrive_time[server_idx][i] = arrive_time
            add_event([now + serve_time, [server_idx, i]])
            core_task_class[server_idx][i] = kind
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
    if len(timer_queue[0]) == 0 and len(timer_queue[1]) == 0:
        return
    if len(timer_queue[0]):
        res = timer_queue[0].pop(0)
        kind = 0
    else:
        res = timer_queue[1].pop(0)
        kind = 1
    for is_busy in core_is_busy[idx]:
        if not is_busy:
            execute(kind, res[1], event[0], idx)
            return
    if kind == 0:
        cores_queue[idx][0].append(res)
    else:
        cores_queue[idx][1].append(res)


def check_accuracy(n, sum_squares, sum):
    if sum == 0 or n == 0:
        return False
    mean = sum / float(n)
    sigma = sqrt(sum_squares / float(n))
    return (1.96 * sigma) / (sqrt(float(n)) * mean) <= 0.05


def check_statistics():
    if check_accuracy(sum(exited_users), sum(square_exited_users), sum(sum_exited_users)) and is_done[0][0] == 0:
        is_done[0][0] = sum(exited_users)
        output[0][0] = sum(sum_exited_users) / sum(exited_users)
    if check_accuracy(exited_users[0], square_exited_users[0], sum_exited_users[0]) and is_done[0][1] == 0:
        is_done[0][1] = exited_users[0]
        output[0][1] = sum_exited_users[0] / exited_users[0]
        # print(sum_exited_users[0])
    if check_accuracy(exited_users[1], square_exited_users[1], sum_exited_users[1]) and is_done[0][2] == 0:
        is_done[0][2] = exited_users[1]
        output[0][2] = sum_exited_users[1] / exited_users[1]

    if check_accuracy(sum(exit_from_queue_num), sum(square_queue_wait), sum(sum_queue_wait)) and is_done[1][0] == 0:
        is_done[1][0] = sum(exit_from_queue_num)
        output[1][0] = sum(sum_queue_wait) / sum(exit_from_queue_num)
    if check_accuracy(exit_from_queue_num[0], square_queue_wait[0], sum_queue_wait[0]) and is_done[1][1] == 0:
        is_done[1][1] = exit_from_queue_num[0]
        output[1][1] = sum_queue_wait[0] / exit_from_queue_num[0]
        print("type 0 " + str(is_done[1][1]))
    if check_accuracy(exit_from_queue_num[1], square_queue_wait[1], sum_queue_wait[1]) and is_done[1][2] == 0:
        is_done[1][2] = exit_from_queue_num[1]
        output[1][2] = sum_queue_wait[1] / exit_from_queue_num[1]
        print("type 1 " + str(is_done[1][2]))

    if check_accuracy(num_of_expired_tasks[2], square_average_expired_task[2], sum_average_expired_tasks[2]) and \
            is_done[2][0] == 0:
        is_done[2][0] = num_of_expired_tasks[2]
        output[2][0] = sum_average_expired_tasks[2] / num_of_expired_tasks[2]

    if check_accuracy(num_of_expired_tasks[0], square_average_expired_task[0], sum_average_expired_tasks[0]) and \
            is_done[2][1] == 0:
        is_done[2][1] = num_of_expired_tasks[0]
        output[2][1] = sum_average_expired_tasks[0] / num_of_expired_tasks[0]

    if check_accuracy(num_of_expired_tasks[1], square_average_expired_task[1], sum_average_expired_tasks[1]) and \
            is_done[2][2] == 0:
        is_done[2][2] = num_of_expired_tasks[1]
        output[2][2] = sum_average_expired_tasks[1] / num_of_expired_tasks[1]

    # if check_accuracy(sum(num_of_expired_tasks), sum(square_average_expired_task), sum(sum_expired_tasks)) and \
    #         is_done[1][0] == 0:
    #     is_done[1][0] = sum(num_of_expired_tasks)
    #     output[1][0] = sum(sum_expired_tasks) / sum(num_of_expired_tasks)
    #
    #
    # if check_accuracy(num_of_expired_tasks[0], square_average_expired_task[0], sum_expired_tasks[0]) and is_done[1][
    #     1] == 0:
    #     is_done[1][1] = num_of_expired_tasks[0]
    #     output[1][1] = sum_expired_tasks[0] / num_of_expired_tasks[0]
    #
    # if check_accuracy(num_of_expired_tasks[1], square_average_expired_task[1], sum_expired_tasks[1]) and is_done[1][
    #     2] == 0:
    #     is_done[1][2] = num_of_expired_tasks[1]
    #     output[1][2] = sum_expired_tasks[1] / num_of_expired_tasks[1]


def core_clock(event):
    global exited_users
    global sum_exited_users
    global square_exited_users
    global exited
    core_is_busy[event[1][0]][event[1][1]] = False
    kind = core_task_class[event[1][0]][event[1][1]]
    if exited > 5000:
        exited_users[kind] += 1
        new = event[0] - core_task_arrive_time[event[1][0]][event[1][1]]
        sum_exited_users[kind] += new
        square_exited_users[kind] += new * new
        check_statistics()
    # sum_expired_tasks[kind] += event[0] - core_task_arrive_time[event[1][0]][event[1][1]]
    # sum_average_expired_tasks += su
    if len(cores_queue[event[1][0]][0]) > 0:
        execute(0, core_task_arrive_time[event[1][0]][event[1][1]], event[0], event[1][0])
        cores_queue[event[1][0]][0].pop(0)
    elif len(cores_queue[event[1][0]][1]) > 0:
        cores_queue[event[1][0]][1].pop(0)
        execute(1, core_task_arrive_time[event[1][0]][event[1][1]], event[0], event[1][0])
    exited += 1


def handle_expired_tasks(time):
    global exited_users
    global exited
    expired_tasks = []
    for i in range(2):
        j = 0
        while j < len(timer_queue[i]):
            if timer_queue[i][j][0] < time:
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
        if exited > 5000:
            num_of_expired_tasks[2] += 1
            num_of_expired_tasks[expired_tasks[i][1]] += 1
            exited_users[expired_tasks[i][1]] += 1
            exit_from_queue_num[expired_tasks[i][1]] += 1
            sum_average_expired_tasks[2] += (num_of_expired_tasks[2]) / sum(exited_users)
            sum_average_expired_tasks[expired_tasks[i][1]] += (num_of_expired_tasks[expired_tasks[i][1]]) / \
                                                              exited_users[expired_tasks[i][1]]
            square_average_expired_task[2] += ((num_of_expired_tasks[2]) / sum(exited_users)) ** 2
            square_average_expired_task[expired_tasks[i][1]] = ((num_of_expired_tasks[expired_tasks[i][1]]) /
                                                                exited_users[expired_tasks[i][1]]) ** 2

        if expired_tasks[i][0] == -1:
            # print(expired_tasks)
            # print(i)
            # print(timer_idx)
            # print(expired_tasks)
            # print(timer_queue)
            # print(expired_tasks[i][2] - timer_idx[expired_tasks[i][1]])
            # print()
            if exited > 5000:
                sum_queue_wait[expired_tasks[i][1]] += time - timer_queue[expired_tasks[i][1]][
                    expired_tasks[i][2] - timer_idx[expired_tasks[i][1]]][1]
                square_queue_wait[expired_tasks[i][1]] += (time - timer_queue[expired_tasks[i][1]][
                    expired_tasks[i][2] - timer_idx[expired_tasks[i][1]]][1]) ** 2
                sum_exited_users[expired_tasks[i][1]] += time - timer_queue[expired_tasks[i][1]][
                    expired_tasks[i][2] - timer_idx[expired_tasks[i][1]]][1]
                square_exited_users[expired_tasks[i][1]] += (time - timer_queue[expired_tasks[i][1]][
                    expired_tasks[i][2] - timer_idx[expired_tasks[i][1]]][1]) ** 2
            timer_queue[expired_tasks[i][1]].pop(expired_tasks[i][2] - timer_idx[expired_tasks[i][1]])
            timer_idx[expired_tasks[i][1]] += 1
        else:
            if exited > 5000:
                sum_queue_wait[expired_tasks[i][1]] += time - cores_queue[
                    expired_tasks[i][2] - server_idxs[expired_tasks[i][0]][expired_tasks[i][1]]]
                square_queue_wait[expired_tasks[i][1]] += (time - cores_queue[
                    expired_tasks[i][2] - server_idxs[expired_tasks[i][0]][expired_tasks[i][1]]]) ** 2
                sum_exited_users[expired_tasks[i][1]] += time - cores_queue[
                    expired_tasks[i][2] - server_idxs[expired_tasks[i][0]][expired_tasks[i][1]]]
                square_exited_users[expired_tasks[i][1]] += (time - cores_queue[
                    expired_tasks[i][2] - server_idxs[expired_tasks[i][0]][expired_tasks[i][1]]]) ** 2
            cores_queue[expired_tasks[i][0]][expired_tasks[i][1]].pop(
                expired_tasks[i][2] - server_idxs[expired_tasks[i][0]][expired_tasks[i][1]])
            server_idxs[expired_tasks[i][0]][expired_tasks[i][1]] += 1
        if exited > 5000:
            check_statistics()

        exited += 1


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
    core_task_arrive_time = []
    core_task_class = []

    # quality properties
    exited = 0
    sum_exited_users = [0, 0]
    queue_time = []
    num_of_expired_tasks = [0, 0, 0]
    square_average_expired_task = [0, 0, 0]
    sum_average_expired_tasks = [0, 0, 0]
    # sum_expired_tasks = [0, 0]
    average_timer_queue_len = 0
    average_servers_queue_len = [0] * M
    task_needed_service_time = 0
    task_needed_queue_time = 0
    task_needed_average_timer_queue_len = 0
    task_needed_average_servers_queue_len = [0] * M
    served_users = 0
    intered_users = 0
    exited_users = [0, 0]
    square_exited_users = [0, 0]
    sum_queue_wait = [0, 0]
    square_queue_wait = [0, 0]
    exit_from_queue_num = [0, 0]
    limit = 50000000

    for i in range(M):
        cores.append([])
        core_is_busy.append([])
        core_task_arrive_time.append([])
        core_task_class.append([])
        cores_queue.append([[], []])
        temp = file.readline()[:-1].split(" ")
        temp2 = temp[1:]
        core_is_busy[i] = [False] * int(temp[0])
        core_task_arrive_time[i] = [-1] * int(temp[0])
        core_task_class[i] = [-1] * int(temp[0])
        for j in range(int(temp[0])):
            cores[i].append(float(temp2[j]))

    events = [[0, [-3, 0]]]
    events.append([get_exp_sample(arrival_rate), [-2, 0]])  # arrival event specified by -2
    events.append([get_exp_sample(mu), [-1, 0]])  # timer job specified by -1

    # make heap
    for i in range(len(events) - 1, 0, -1):
        BD(i)

    output = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    is_done = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    while served_users < 50000000:
        # print(events)
        e = remove_min()
        handle_expired_tasks(e[0])
        if e[1][0] == -2:
            arrive(e)
        elif e[1][0] == -1:
            timer_pass(e)
        else:
            core_clock(e)
