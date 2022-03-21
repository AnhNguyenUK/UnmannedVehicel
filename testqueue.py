from queue import Queue




if __name__ == '__main__':
    q = Queue()
    for i in range(1):
        print(q.empty())
        q.put(i)
        print(q.empty())
        print(q.get())
        print(q.empty())
        