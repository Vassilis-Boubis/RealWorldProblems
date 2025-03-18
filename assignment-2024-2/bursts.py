import argparse
import math

parse = argparse.ArgumentParser()
parse.add_argument('-s', type=float, help='an optional float parameter S')
parse.add_argument('-g', '--gamma', type=float, help='an optional float parameter GAMMA')
parse.add_argument('-d', action='store_true', help='an optional boolean flag D')
parse.add_argument('mode', choices=['viterbi', 'trellis'], help='the mode of operation')
parse.add_argument('offsets_file', help='the offsets file')

args = parse.parse_args()

with open(args.offsets_file, 'r') as sms:
    m = sms.read()
    messages = m.split()

messages = [float(item)for item in messages]

s = args.s
g = args.gamma
if s == None:
    s = 2
if g == None:
    g = 1
d = args.d
mode = args.mode

X = []
for i in range(1, len(messages)):
    X.append(messages[i] - messages[i-1])

minx = min(X)
T = messages[-1] - messages[0]
k = 1 + math.log(T, s) + math.log(1 / minx, s)
k = math.ceil(k)
n = len(X)

def viterbi():

    C = [[math.inf for j in range(k)] for i in range(n + 1)]
    C[0][0] = 0

    P = [[0 for a in range(n + 1)] for bS in range(k)]

    taf = [[0 for a in range(n + 1)] for b in range(n + 1)]
    taf = [[g * (j - i) * math.log(n) if j > i else 0 for j in range(n + 1)] for i in range(n + 1)]

    if d == True:
        print(C[0])
    for t in range(1, n + 1):
        for i in range(k):
            lmin = 0
            cmin = C[t-1][0] + taf[0][i]
            for l in range(1, k):
                c = C[t - 1][l] + taf[l][i]
                if c < cmin:
                    cmin = c
                    lmin = l
            g1 = T/n
            lamda = (s**i) / g1
            r =  math.exp(-lamda * X[t - 1])
            threshold = 1e-300
            if r < threshold:
                r = threshold
            fi = lamda * r
            C[t][i] = (cmin - math.log(fi))
            P[i][0:t] = P[lmin][0:t]
            P[i][t] = i
        if d == True:
            print([round(a, 2) for a in C[t]])
    cmin = C[n][0]
    smin = 0

    for i in range(1, k):
        if C[n][i] < cmin:
            cmin = C[n][i]
            smin = i

    if d == True:        
        print(len(P[smin]), P[smin])
    
    return(P[smin])


def trellis():
    dist = [[math.inf for j in range(k)] for i in range(n + 1)]
    dist[0][0] = 0

    pred = [[0 for a in range(n + 1)] for b in range(k)]

    taf = [[0 for a in range(n + 1)] for b in range(n + 1)]
    taf = [[g * (j - i) * math.log(n) if j > i else 0 for j in range(n + 1)] for i in range(n + 1)]


    edges = []
    for i in range(k):
        edges.append([0, 0, i, 1])
    for t in range(2, n + 1):
        for j in range(k):
            for w in range(k):
                edges.append([j, t - 1, w, t])


    for i in range(k*(n+1)):
        for u, time_u, v, time_v in edges:
            g1 = T/n
            lamda = (s**v) / g1
            r =  math.exp(-lamda * (messages[time_v] - messages[time_u]))
            threshold = 1e-300
            if r < threshold:
                r = threshold
            fi = lamda * r
            costmes =(- math.log(fi))
            cost = dist[time_u][u] + taf[u][v] + costmes
            if dist[time_v][v] > cost:
                if d == True:
                    print(f'({time_v}, {v}) {round(dist[time_v][v], 2)} -> {round(cost, 2)} from ({time_u}, {u}) {round(dist[time_u][u], 2)} + {round(taf[u][v], 2)} + {round(costmes, 2)}')
                dist[time_v][v] = cost
                pred[v][time_v] = u   


    cmin = dist[n][0]
    smin = 0
    for i in range(1, k):
        if dist[n][i] < cmin:
            cmin = dist[n][i]
            smin = i


    res = [-1 for a in range(n + 1)]
    res[0] = 0
    res[n] = smin
    temp = res[n]
    for i in range(n, 0, -1):
        res[i - 1] = pred[temp][i]
        temp = res[i - 1]
    
    return res


if mode == 'viterbi':
    results = viterbi()
elif mode == 'trellis':
    results = trellis()
before = results[0]
point = messages[0]
for i in range(1, len(results)):
    if before != results[i]:
        print(f'{before} [{point} {messages[i - 1]})')
        before = results[i]
        point = messages[i - 1]
print(f'{before} [{point} {messages[i]})')
