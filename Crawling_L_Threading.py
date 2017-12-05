import threading, multiprocessing, queue #,Crawling_L

def worker(urlQueue):
    while(True):
        try:
            url = urlQueue.get(block=True, timeout=3)
        except:
            print(threading.current_thread().getName(), ": The Q is empty")
            continue
        #jsonObject = Crawling_L.parse_webpages((url,))
        #crawled_id = Crawling_L.insert_webpage(jsonObject)
    return

class threadManager:
    def __init__(self):
        self.urlQueue = queue.Queue()
        self.threads = []
        self.cpuCount = multiprocessing.cpu_count()
        for i in range(self.cpuCount):
            t = threading.Thread(target=worker, args=(self.urlQueue,))
            self.threads.append(t)
            t.start()
        return
    def addToQueue(self, url):
        self.urlQueue.put(url)
        return

'''if __name__ == "__main__":
    man = threadManager()
    print("hello there\n")
    man.addToQueue(url="www.google.com")
    while(True):
        x = 1
'''