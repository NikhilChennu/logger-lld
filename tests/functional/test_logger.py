import unittest
from logger.logger import Logger
import asyncio
import random

class TestLogger(unittest.TestCase):
    def test_manual(self):
        async def process():
            logger_client = Logger()
            x = await asyncio.gather(logger_client.start(1, 1), logger_client.poll(), logger_client.start(2, 3),
                                     logger_client.end(2), logger_client.poll(), logger_client.end(1))
            return  x

        x=asyncio.run(process())
        expected=[None,1,None,None,2,None]
        self.assertListEqual(x,expected)

    def test_automated(self):
        tasks_list=[]
        end_tasks_list=[]
        n=2
        for i in  range(n):
            tasks_list.append("start "+str(i))
            end_tasks_list.append("end "+str(i))
            end_tasks_list.append("poll")

        random.shuffle(end_tasks_list)

        tasks_list=tasks_list+end_tasks_list

        result=[]
        class_tasks=[]
        logger_client=Logger()
        index=0
        for i in range(len(tasks_list)):
            if tasks_list[i]=="poll":
                result.append(str(index))
                index+=1
                class_tasks.append(logger_client.poll())
            elif 'end' in tasks_list[i]:
                result.append(None)
                id=tasks_list[i].split(" ")[1]
                class_tasks.append(logger_client.end(id))
            else:
                id = tasks_list[i].split(" ")[1]
                result.append(None)
                class_tasks.append(logger_client.start(id,int(id)))


        loop = asyncio.get_event_loop()
        x=loop.run_until_complete(asyncio.gather(*class_tasks))
        self.assertListEqual(x, result)