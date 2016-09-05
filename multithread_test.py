#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import threading

def loopprint():
    print('hal')

def main():
    threads = []
    nums = range(0, 10)

    for n in nums:
        t = threading.Thread(target=loopprint)
        threads.append(t)

    for n in nums:
        threads[n].start()

    for n in nums:
        threads[n].join()

    print("All Done!")

if __name__ == '__main__':
    main()
