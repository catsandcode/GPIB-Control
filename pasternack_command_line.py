import time
import numpy as np
import os

devpath = '/dev/usbtmc0'
dev = open(devpath,'w+')
timeout = 1.0
lineender = '\n'

def r():
    return dev.read()

def rn(n):
    s = ''
    t0 = time.time()
    while len(s) < n:
        t1 = time.time()
        if(t1 - t0 > timeout):
            break
        s += dev.read(n)
    return s

def w(s):
    dev.write(s+lineender)
    dev.flush()

def ask(s):
    dev.write(s+lineender)
    dev.flush()
    return dev.read().strip()

def askn(s,n):
    dev.write(s+lineender)
    dev.flush()
    return dev.read(n).strip()

def enable(en):
    assert en in [0,1]
    w('POWE:RF %d'%en)
def setfreq(f):
    assert (9.9 < f) & (f < 20.1)
    w('FREQ:SET %f'%f)
def setpow(p):
    w('POWE:SET %f'%p)

def query():
    print ask('FREQ:LOCK?')
    print ask('FREQ:PLLM?')
    print ask('FREQ:REF:EXT?')
    print ask('FREQ:REF:FREQ?')
    print ask('FREQ:RETACT?')
    print ask('POWE:RF?')

    w('POWE:RF 1')

    print ask('POWE:RF?')

while True:
    inp_str = raw_input('"Q" for query, "W" for write, "E" for end\n')
    inp_str = inp_str.upper()
    if len(inp_str) < 1:
        print 'Invalid input'
    else:
        qwe = inp_str[:1]
        command = inp_str[1:]
        if qwe == 'Q':
            print ask(command)
        elif qwe == 'W':
            w(command)
        elif qwe == 'E':
            break
        else:
            print 'Invalid input'
