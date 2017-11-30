import threading, Crawling_L, multiprocessing, queue, Crawling_L_Sockets

def worker(urlQueue):
    while(True):
        url = urlQueue.get(block=True, timeout=60)
        jsonObject = Crawling_L.parse_webpages((url,))
        Crawling_L_Sockets.send_crawled_json(json_data=jsonObject)
    return

class threadManager:
    def __init__(self):
        self.urlQueue = queue.Queue()
        self.threads = []
        self.cpuCount = 0
    def createThreads(self):
        self.cpuCount = multiprocessing.cpu_count()
        for i in range(self.cpuCount):
            t = threading.Thread(target=worker(urlQueue=self.urlQueue))
            self.threads.append(t)
            t.start()
        return
    def addToQueue(self, url):
        self.urlQueue.put(url)
        return
