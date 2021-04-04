from threading import RLock
import heapq
from collections import deque
from concurrent.futures import ThreadPoolExecutor,wait
import asyncio
import time

class Process:

    def __init__(self,pid,start):
        self.id=pid
        self.start=start
        self.end=None

    def endProcess(self,end):
        self.end=end


class Logger:

    def __init__(self,):
        self.__process_lookup={}
        self.__heap=[]
        self.__lock=RLock()
        self.__heap_lock=RLock()
        self.__lookup_lock=RLock()
        self.__event_queue=deque()
        self.__executors=[]
        for i in range(10):
            self.__executors.append(ThreadPoolExecutor(1))



    def __start_util(self,pid,start):
        new_process = Process(pid, start)
        with self.__lookup_lock:
            self.__process_lookup[new_process.id] = new_process
        with self.__heap_lock:
            heapq.heappush(self.__heap, (start, pid))

    async def start(self,pid,start):
        tid=self.__executors[int(pid)%10].submit(self.__start_util,pid,start)
        wait([tid])

    def __end_util(self,pid):
        with self.__lock:
            self.__process_lookup[pid].end = round(time.time()*1000)
            while len(self.__event_queue) and len(self.__heap)>0 and self.__process_lookup[self.__heap[0][1]].end is not None:
                polled_pid=self.pollNow()
                future_object = self.__event_queue.popleft()
                try:
                    future_object.set_result(polled_pid)
                except Exception as e:
                    raise e

    async def end(self,pid):
        tid=self.__executors[int(pid)%10].submit(self.__end_util,pid)
        wait([tid])

    def pollNow(self):
        start,pid=heapq.heappop(self.__heap)
        del self.__process_lookup[pid]
        return pid

    async def poll(self):
        with self.__lock:
            if len(self.__heap)>0 and self.__process_lookup[self.__heap[0][1]].end is not None:
                pid=self.pollNow()
                return pid
            future_object = asyncio.Future()
            self.__event_queue.append(future_object)
        await asyncio.wait_for(future_object,timeout=30)
        result=future_object.result()
        return result
