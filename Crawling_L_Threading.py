import threading, Crawling_L, multiprocessing, queue

def worker(url):
    return

class threadManager:
    def __init__(self):
        self.urlQueue = queue.Queue()
        self.threads = []
        self.cpuCount = 0
    def createThreads(self):
        cpuCount = multiprocessing.cpu_count()
        for i in range(cpuCount):
            t = threading.Thread(target=worker)
            self.threads.append(t)
            t.start()
