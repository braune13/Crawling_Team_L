import threading, Crawling_L, multiprocessing, queue

def worker(urlQueue):
    while(True):
        url = urlQueue.get(block=True, timeout=60)
        jsonObject = Crawling_L.parse_webpages((url,))
    return

class threadManager:
    def __init__(self):
        self.urlQueue = queue.Queue()
        self.threads = []
        self.cpuCount = multiprocessing.cpu_count()
        for i in range(self.cpuCount):
            t = threading.Thread(target=worker(urlQueue=self.urlQueue))
            self.threads.append(t)
            t.start()
        return
    def addToQueue(self, url):
        self.urlQueue.put(url)
        return
