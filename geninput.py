from itertools import permutations
from sys import argv
import random

FILENAME = "testinput.txt"

N=7

def generate(cond):
    perms = permutations('TILJSZO'[:N])
    formatted_perms = map(lambda x: "".join(x), perms)
    filtered_perms = filter(cond, formatted_perms)
    return list(filtered_perms)

def endTSZ(queue: str):
    earliest = min(queue.index('T'), queue.index('S'), queue.index('Z'))
    return earliest == N-3

def allButTILJSZO(queue: str):
    return queue != "TILJSZO"[:N]

def ibl(queue: str):
    f = lambda x:queue.index(x)
    return (f('I')<f('J') and
            f('I')<f('L') or
            f('T')<f('S'))

def simple(queue):
    return queue.index('I')<queue.index('T')

def format(queueList: list[str], sep='\n'):
    return sep.join(queueList)

def rando(queue):
    return random.random()<0.05

d={
    "sim":simple,
    "notTILJSZ":allButTILJSZO,
    "bil":ibl,
    "endsTSZ":endTSZ,
    "ran":rando
}

with open(FILENAME, 'w') as f:
    func = d[argv[1]]
    queues = generate(func)
    print(format(queues,sep="|"))
    f.write(format(queues))